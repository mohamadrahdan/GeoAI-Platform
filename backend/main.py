from backend.app import create_app
from core.logger import setup_logging
import logging

# Initialize production-grade logging at the absolute process entry point
setup_logging()
logger = logging.getLogger(__name__)

# Bootstrapping the FastAPI application via the custom application factory
app = create_app()

logger.info("GeoAI Platform backend application factory executed successfully")
