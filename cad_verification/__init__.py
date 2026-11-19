"""Reusable CAD/model verification library."""

from .errors import (
    ArtifactError,
    CommandError,
    CommandFailed,
    CommandTimedOut,
    VerificationConfigError,
    VerificationError,
    VerificationFailure,
)
from .model import (
    CheckOutcome,
    CommandResult,
    VerificationCheck,
    VerificationContext,
)
from .process import run_command
from .verification import verify

__all__ = [
    "ArtifactError",
    "CheckOutcome",
    "CommandError",
    "CommandFailed",
    "CommandResult",
    "CommandTimedOut",
    "VerificationCheck",
    "VerificationConfigError",
    "VerificationContext",
    "VerificationError",
    "VerificationFailure",
    "run_command",
    "verify",
]
