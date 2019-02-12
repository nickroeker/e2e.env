"""Exceptions raised by e2e.env."""


class EnvError(Exception):
    """Base class for exceptions raised by e2e.env."""


class NoSuchVariableError(EnvError):
    """Raised when a requested variable does not exist in the environment."""
