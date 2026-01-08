from __future__ import annotations



class GeoAIError(Exception):
    "Base exception for all GeoAI core errors."
    pass

class ConfigurationError(GeoAIError):
    "Raised when configuration is invalid or missing."
    pass



class DataAccessError(GeoAIError):
    "Raised when data cannot be accessed or resolved."
    pass

class ExecutionError(GeoAIError):
    "Raised during execution failures (non-plugin-specific)."
    pass
