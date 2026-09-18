"""VALID / INVALID results with explicit reason codes (P0 spec §37, §51)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.contracts import reasons


@dataclass(frozen=True)
class ValidationResult:
    status: str
    reason_codes: tuple[str, ...] = ()
    message: str = ""
    system: str = "CORE"
    entity: str | None = None
    operation: str | None = None
    data_id: str | None = None

    @property
    def valid(self) -> bool:
        return self.status == reasons.VALID

    def to_error_record(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "entity": self.entity,
            "operation": self.operation,
            "data_id": self.data_id,
            "reason": ",".join(self.reason_codes) if self.reason_codes else None,
            "message": self.message,
        }


def ok(*, operation: str | None = None, entity: str | None = None, data_id: str | None = None) -> ValidationResult:
    return ValidationResult(
        status=reasons.VALID,
        operation=operation,
        entity=entity,
        data_id=data_id,
    )


def fail(
    *codes: str,
    message: str,
    operation: str | None = None,
    entity: str | None = None,
    data_id: str | None = None,
    system: str = "CORE",
) -> ValidationResult:
    if not codes:
        raise ValueError("invalid results require at least one reason code")
    return ValidationResult(
        status=reasons.INVALID,
        reason_codes=codes,
        message=message,
        system=system,
        entity=entity,
        operation=operation,
        data_id=data_id,
    )


@dataclass(frozen=True)
class OpResult:
    """Outcome of a runtime operation that may legally fail (e.g. consume)."""

    ok: bool
    reason_code: str | None = None
    value: float | None = None
    validation: ValidationResult | None = None
