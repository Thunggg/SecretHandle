# Baseline adapters

## B0: unprotected

Implemented for isolated synthetic canaries. It exposes the raw value to the agent artifact and allows ordinary typing. Never run it with a real credential, production OTP, address, or payment value.

## B1: detected placeholder

Implemented as a deterministic reference detector that replaces a known synthetic value with a typed placeholder and resolves it without destination binding. This code is **not** the implementation of Zhao et al. or AutoDroid and makes no claim about their detector accuracy, APIs, or measured behavior.

## B2: Android platform flow

`PlatformFlowAdapter` is an abstract contract. A real adapter must report whether Autofill, OTP Autofill, or Credential Manager was invoked, whether the app cooperated, authenticated app/origin identity, user selection, delivery, and task outcome. Unsupported workflows are `not_applicable`, not failures. No fake Android API is supplied.

## B3: SecretHandle

The Python service implements reference semantics. A real B3 adapter must bridge mint, target-token resolution, private input, redaction, lifecycle journal, protected confirmation, audit export, and device security-level reporting to the AOSP implementation.

## Agent and benchmark adapters

`AgentRunnerAdapter` and `BenchmarkAdapter` define intentionally small abstract contracts. Concrete adapters belong in a separate provisioned EC2/device integration layer and must record external repository commits and model identifiers. Tests may use dummy subclasses but outputs must identify them as dummy/synthetic.
