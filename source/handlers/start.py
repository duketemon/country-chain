import logging

from .help import get_help


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def start_handler(update, context):
    LOGGER.info(f'User with id={update.effective_user["id"]} connected to the bot.')
    update.message.reply_text(get_help() + "\n\nIf you want to start a game send me any country name you want")
