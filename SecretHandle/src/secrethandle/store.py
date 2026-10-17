"""Thread-safe in-memory reference store for Equation (1) and lifecycle invariants."""

from __future__ import annotations

import copy
import threading

from .schemas import LifecycleState, SecretRecord


class StoreError(RuntimeError):
    pass


class SecretStore:
    """Linearizable reference store.

    This lock models atomic state changes but is not a substitute for AOSP durable storage.
    """

    def __init__(self) -> None:
        self._records: dict[str, SecretRecord] = {}
        self._lock = threading.RLock()

    def insert(self, record: SecretRecord) -> None:
        with self._lock:
            identifier = record.metadata.identifier
            if identifier in self._records:
                raise StoreError("identifier collision")
            self._records[identifier] = copy.deepcopy(record)

    def load(self, identifier: str) -> SecretRecord | None:
        with self._lock:
            record = self._records.get(identifier)
            return None if record is None else copy.deepcopy(record)

    def reserve(self, identifier: str, nonce: str, now: float) -> SecretRecord | None:
        """Atomic live-to-reserved transition used by Proposition 1.

        Decision D4: the use budget is decremented here, at reservation, so a
        concurrent or crashed attempt cannot replay the gap before delivery.
        """

        with self._lock:
            record = self._records.get(identifier)
            if record is None:
                return None
            if record.state is LifecycleState.LIVE and now >= record.metadata.expires_at:
                record.state = LifecycleState.EXPIRED
                record.version += 1
                return None
            if record.state is not LifecycleState.LIVE or record.remaining_uses <= 0:
                return None
            record.state = LifecycleState.RESERVED
            record.reservation_nonce = nonce
            record.remaining_uses -= 1
            record.version += 1
            return copy.deepcopy(record)

    def commit(self, identifier: str, nonce: str, uncertain: bool = False) -> SecretRecord:
        with self._lock:
            record = self._require_reserved(identifier, nonce)
            record.state = (
                LifecycleState.CONSUMED
                if uncertain or record.remaining_uses <= 0
                else LifecycleState.LIVE
            )
            record.reservation_nonce = None
            record.version += 1
            return copy.deepcopy(record)

    def rollback(self, identifier: str, nonce: str, delivery_impossible: bool) -> SecretRecord:
        if not delivery_impossible:
            raise StoreError("rollback requires proof that delivery was impossible")
        with self._lock:
            record = self._require_reserved(identifier, nonce)
            record.state = LifecycleState.LIVE
            record.remaining_uses += 1  # refund the reservation; delivery never happened
            record.reservation_nonce = None
            record.version += 1
            return copy.deepcopy(record)

    def revoke(self, identifier: str) -> bool:
        with self._lock:
            record = self._records.get(identifier)
            if record is None or record.state in {LifecycleState.CONSUMED, LifecycleState.EXPIRED}:
                return False
            record.state = LifecycleState.REVOKED
            record.reservation_nonce = None
            record.version += 1
            return True

    def revoke_task(self, task_id: str) -> int:
        with self._lock:
            count = 0
            for record in self._records.values():
                if record.metadata.task_id == task_id and record.state in {
                    LifecycleState.LIVE,
                    LifecycleState.RESERVED,
                }:
                    record.state = LifecycleState.REVOKED
                    record.reservation_nonce = None
                    record.version += 1
                    count += 1
            return count

    def expire(self, now: float) -> int:
        """Monotonic expiry transition from Proposition 2."""

        with self._lock:
            count = 0
            for record in self._records.values():
                if record.state in {LifecycleState.LIVE, LifecycleState.RESERVED} and now >= record.metadata.expires_at:
                    record.state = LifecycleState.EXPIRED
                    record.reservation_nonce = None
                    record.version += 1
                    count += 1
            return count

    def recover_reserved(self) -> int:
        """Conservatively consume single-use reservations after an uncertain restart."""

        with self._lock:
            count = 0
            for record in self._records.values():
                if record.state is LifecycleState.RESERVED:
                    record.state = LifecycleState.CONSUMED
                    record.reservation_nonce = None
                    record.version += 1
                    count += 1
            return count

    def states(self) -> dict[str, str]:
        with self._lock:
            return {key: value.state.value for key, value in self._records.items()}

    def _require_reserved(self, identifier: str, nonce: str) -> SecretRecord:
        record = self._records.get(identifier)
        if record is None:
            raise StoreError("unknown handle")
        if record.state is not LifecycleState.RESERVED or record.reservation_nonce != nonce:
            raise StoreError("reservation mismatch")
        return record
