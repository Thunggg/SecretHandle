"""SecretHandle reference model.

This package is a testable specification and synthetic evaluation harness. It is not an
Android/AOSP enforcement implementation.
"""

from .core import SecretHandleService
from .schemas import OpaqueHandle, SecretType, TargetContext

__all__ = ["SecretHandleService", "OpaqueHandle", "SecretType", "TargetContext"]
__version__ = "0.1.0"
