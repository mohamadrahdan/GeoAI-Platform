from __future__ import annotations


class GeoAIError(Exception):
    "Base exception for all GeoAI core errors"



class ConfigurationError(GeoAIError):
    "Raised when configuration is invalid or missing"



class DataAccessError(GeoAIError):
    "Raised when data cannot be accessed or resolved"



class ExecutionError(GeoAIError):
    "Raised during execution failures (non-plugin-specific)"



class InferenceTimeoutError(ExecutionError):
    "Raised when model prediction exceeds the allowed timeout"
