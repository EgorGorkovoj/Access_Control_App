class PermissionProviderError(Exception):
    """Base error for permission provider communication issues."""


class PermissionProviderHTTPError(PermissionProviderError):
    """HTTP-level error (timeout, 5xx, connection issues)."""


class PermissionProviderResponseError(PermissionProviderError):
    """Invalid or unexpected response format from provider."""
