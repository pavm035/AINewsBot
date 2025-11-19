import logging

from newsbot.core.logger import setup_logger
from newsbot.app import BasicChatBotApp

setup_logger()

# Get logger for this module
logger = logging.getLogger(__name__)

logger.info("main.py has started.")

if __name__ == "__main__":
    app = BasicChatBotApp()
    app.run()
