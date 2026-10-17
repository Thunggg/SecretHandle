"""Synthetic-only experiment, ablation, and killer-experiment runners."""

from __future__ import annotations

import logging
import platform
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from .adapters import DeterministicConfirmationProvider, InMemoryInjector, InMemoryTargetResolver
from .baselines import DetectedPlaceholderBaseline, PlatformFlowBaseline, UnprotectedBaseline
from .config import public_config
from .core import SecretHandleService
from .io import atomic_write_json, atomic_write_jsonl, write_metrics_csv
from .metrics import aggregate_trial_metrics
from .oracles import DisclosureOracle
from .schemas import (
    Artifact,
    ConfirmationMode,
    DestinationPolicy,
    Observation,
    ObservationItem,
    OpaqueHandle,
    PolicyHints,
    Provenance,
    SecretType,
    TaskToken,
    TrialOutcome,
)
from .synthetic import (
    SeededIdentifierSource,
    ambiguous_target_token,
    canary,
    synthetic_key,
    target_tokens,
)

LOGGER = logging.getLogger(__name__)
SYNTHETIC_LABEL = "synthetic smoke-test output, not a paper result"


def _service(seed: int, lambda_bits: int) -> SecretHandleService:
    return SecretHandleService(
        key=synthetic_key(seed),
        identifier_source=SeededIdentifierSource(seed, lambda_bits),
        clock=lambda: 1000.0,
    )


def _b3_trial(seed: int, attack: str, lambda_bits: int) -> TrialOutcome:
    service = _service(seed, lambda_bits)
    good, attacker, stale = target_tokens()
    ambiguous = ambiguous_target_token()
    resolver = InMemoryTargetResolver({t.token_id: t for t in (good, attacker, stale, ambiguous)})
    injector = InMemoryInjector()
    confirmation = DeterministicConfirmationProvider(True)
    task = TaskToken("task-login", frozenset({"com.example.bank"}))
    secret = canary(seed)
    handle = service.mint(
        secret.encode(),
        SecretType.OTP,
        Provenance("sms", f"synthetic-{seed}"),
        task,
        DestinationPolicy(
            packages=frozenset({"com.example.bank"}),
            origins=frozenset({"https://bank.example"}),
            fields=frozenset({"otp"}),
            require_origin=True,
            require_field=True,
        ),
        PolicyHints(60.0, 1, ConfirmationMode.NONE),
        now=1000.0,
    )
    exposure = False
    redirect = utility = leakage = forgery = replay = None
    rejected = False
    identity_available = True
    if attack == "read_exfil":
        # Family 1: the agent may only observe the handle, never the raw value.
        visible = Observation(
            (
                ObservationItem("accessibility", f"otp:{handle.identifier}", good.token_id, True, "win-bank"),
                ObservationItem("screenshot", f"otp:{handle.identifier}", good.token_id, True, "win-bank"),
            )
        )
        redacted = service.redactor.redact(visible)
        exposure = DisclosureOracle().scan(
            secret, [Artifact(i.channel, i.text) for i in redacted.items]
        ).exposed
    elif attack == "ambiguous_identity":
        # Family 7: destination identity cannot be established; must fail closed.
        result = service.resolve(
            handle, task, ambiguous.token_id, resolver, confirmation, injector, 1001.0
        )
        redirect = bool(injector.deliveries)
        rejected = not result.success
        identity_available = False
    elif attack == "benign":
        result = service.resolve(handle, task, good.token_id, resolver, confirmation, injector, 1001.0)
        utility = result.success
        observation = Observation((ObservationItem("accessibility", secret, good.token_id, True, "win-bank"),))
        redacted = service.redactor.redact(observation)
        leakage = DisclosureOracle().scan(secret, [Artifact(i.channel, i.text) for i in redacted.items]).exposed
    elif attack == "redirect":
        result = service.resolve(handle, task, attacker.token_id, resolver, confirmation, injector, 1001.0)
        redirect = bool(injector.deliveries)
        rejected = not result.success
    elif attack == "forgery":
        forged = OpaqueHandle("0" * (lambda_bits // 4), SecretType.OTP, "00" * 32)
        result = service.resolve(forged, task, good.token_id, resolver, confirmation, injector, 1001.0)
        forgery = result.success
        rejected = not result.success
    elif attack == "replay":
        first = service.resolve(handle, task, good.token_id, resolver, confirmation, injector, 1001.0)
        second = service.resolve(handle, task, good.token_id, resolver, confirmation, injector, 1002.0)
        utility = first.success
        replay = second.success
        rejected = not second.success
    elif attack == "reread":
        result = service.resolve(handle, task, good.token_id, resolver, confirmation, injector, 1001.0)
        observation = Observation(
            (
                ObservationItem("screenshot", secret, good.token_id, True, "win-bank"),
                ObservationItem("accessibility", secret, good.token_id, True, "win-bank"),
            )
        )
        redacted = service.redactor.redact(observation)
        leakage = DisclosureOracle().scan(secret, [Artifact(i.channel, i.text) for i in redacted.items]).exposed
        utility = result.success
    elif attack == "expired":
        result = service.resolve(handle, task, good.token_id, resolver, confirmation, injector, 1061.0)
        rejected = not result.success
    else:
        raise ValueError(f"unknown attack: {attack}")
    # Deterministic synthetic timing surrogate; never reported as device latency.
    latency = 0.25 + (seed % 17) * 0.01
    return TrialOutcome(
        trial_id=f"B3-{attack}-{seed}",
        condition="B3_secrethandle",
        attack=attack,
        applicable=True,
        exposure=exposure,
        redirection_success=redirect,
        utility_success=utility,
        post_entry_leakage=leakage,
        forgery_acceptance=forgery,
        replay_acceptance=replay,
        latency_ms=latency,
        policy_rejected=rejected,
        false_rejection=False if attack == "benign" else None,
        identity_available=identity_available,
        synthetic=True,
        metadata={"label": SYNTHETIC_LABEL, "seed": seed},
    )


def _simple_baseline_trial(condition: str, seed: int, attack: str) -> TrialOutcome:
    secret = canary(seed)
    if condition == "B0_unprotected":
        result = UnprotectedBaseline().run(secret, "attacker" if attack == "redirect" else "bank", "bank")
    elif condition == "B1_detected_placeholder":
        result = DetectedPlaceholderBaseline().run(secret, "attacker" if attack == "redirect" else "bank", "bank")
    elif condition == "B2_platform_flow":
        result = PlatformFlowBaseline().run(secret, "bank", "bank")
    else:
        raise ValueError(condition)
    if not result.applicable:
        return TrialOutcome(
            f"{condition}-{attack}-{seed}", condition, attack, False,
            None, None, None, None, None, None, None,
            synthetic=True, metadata={"exclusion_reason": "external_platform_unavailable", "label": SYNTHETIC_LABEL},
        )
    exposure = DisclosureOracle().scan(secret, result.artifacts).exposed
    redirect_unbound = result.delivered_value == secret and not result.bound_to_destination
    redirect = redirect_unbound if attack in {"redirect", "ambiguous_identity"} else None
    utility = result.delivered_value == secret if attack == "benign" else None
    leakage = None
    if condition == "B1_detected_placeholder" and attack == "reread":
        leakage = True
    identity_available = attack != "ambiguous_identity"
    return TrialOutcome(
        trial_id=f"{condition}-{attack}-{seed}",
        condition=condition,
        attack=attack,
        applicable=True,
        exposure=exposure,
        redirection_success=redirect,
        utility_success=utility,
        post_entry_leakage=leakage,
        forgery_acceptance=None,
        replay_acceptance=None,
        latency_ms=None,
        identity_available=identity_available,
        synthetic=True,
        metadata={"label": SYNTHETIC_LABEL, "reference_baseline": True},
    )


def generate_synthetic_trials(config: Mapping[str, Any]) -> list[TrialOutcome]:
    if config["data"]["mode"] != "synthetic":
        raise RuntimeError("real experiment adapters require manually provisioned external infrastructure")
    base_seed = int(config["run"]["seed"])
    count = int(config["experiment"]["trials_per_attack"])
    lambda_bits = int(config["security"]["lambda_bits"])
    attacks = list(config["experiment"].get("attacks", ["benign", "redirect", "forgery", "replay", "reread", "expired"]))
    conditions = list(config["experiment"].get("conditions", ["B0_unprotected", "B1_detected_placeholder", "B2_platform_flow", "B3_secrethandle"]))
    trials = []
    for condition in conditions:
        for attack in attacks:
            for offset in range(count):
                seed = base_seed + offset + 1000 * attacks.index(attack)
                if condition == "B3_secrethandle":
                    trials.append(_b3_trial(seed, attack, lambda_bits))
                else:
                    trials.append(_simple_baseline_trial(condition, seed, attack))
    return trials


def _provenance(config: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "label": SYNTHETIC_LABEL,
        "config_sha256": config.get("_config_sha256"),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "seed": config["run"]["seed"],
        "real_experiment": False,
        "paper_placeholder_numbers_used": False,
    }


def run_synthetic_demo(config: Mapping[str, Any]) -> dict[str, Any]:
    trials = generate_synthetic_trials(config)
    output_dir = Path(str(config["output"]["dir"]))
    output_dir.mkdir(parents=True, exist_ok=True)
    provenance = _provenance(config)
    summaries = {}
    metric_rows = []
    for condition in sorted({trial.condition for trial in trials}):
        subset = [trial for trial in trials if trial.condition == condition]
        summary = aggregate_trial_metrics(subset, provenance)
        summaries[condition] = summary
        for metric in summary.metrics:
            metric_rows.append({
                "condition": condition,
                "metric": metric.name,
                "numerator": metric.numerator,
                "denominator": metric.denominator,
                "value": metric.value,
                "ci_low": metric.ci_low,
                "ci_high": metric.ci_high,
            })
    atomic_write_jsonl(output_dir / "trials.jsonl", [trial.to_dict() for trial in trials])
    atomic_write_json(output_dir / "summary.json", dict(summaries.items()))
    atomic_write_json(output_dir / "provenance.json", {**provenance, "config": public_config(config)})
    write_metrics_csv(output_dir / "metrics.csv", metric_rows)
    LOGGER.info("wrote %d synthetic trials to %s", len(trials), output_dir)
    return {"output_dir": str(output_dir), "trial_count": len(trials), "label": SYNTHETIC_LABEL}


def run_killer_experiment(config: Mapping[str, Any]) -> dict[str, bool]:
    seed = int(config["run"]["seed"])
    bits = int(config["security"]["lambda_bits"])
    benign = _b3_trial(seed, "benign", bits)
    redirect = _b3_trial(seed, "redirect", bits)
    passed = (
        benign.exposure is False
        and redirect.redirection_success is False
        and benign.utility_success is True
    )
    return {
        "raw_absent_from_instrumented_artifacts": benign.exposure is False,
        "attacker_destination_rejected": redirect.redirection_success is False,
        "legitimate_login_succeeds": benign.utility_success is True,
        "passed": passed,
        "synthetic_only": True,
    }


def run_ablation(config: Mapping[str, Any]) -> dict[str, Any]:
    """Create synthetic ablation manifests without hard-coded paper results."""

    components = [
        "authoritative_source_mint", "destination_binding", "task_binding",
        "atomic_lifecycle", "observation_redaction", "origin_predicate", "confirmation",
    ]
    return {
        "label": SYNTHETIC_LABEL,
        "ablations": [
            {"disabled_component": component, "status": "configured_synthetic_only", "metrics": None}
            for component in components
        ],
    }
