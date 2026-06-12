from core.logger import setup_logging
import logging

print("Starting logger test...")

# 1. Call the setup function directly
setup_logging()
# 2. Try to log a message
logger = logging.getLogger(__name__)
logger.info("This is a direct test log. If you see this, the logger works perfectly!")
print("Test finished.")