import os
import pytest

def test_config_fail_fast():
    if "POSTGRES_PASSWORD" in os.environ:
        del os.environ["POSTGRES_PASSWORD"]
    
    os.environ["APP_ENV"] = "production"
    from core.config.settings import get_settings
    
    with pytest.raises(ValueError, match="CRITICAL ERROR"):
        get_settings()