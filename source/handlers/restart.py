import logging

from data_access import clear_user_data


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def restart_handler(update, context):
    LOGGER.info(f'User with id={update.effective_user["id"]} restarted a game.')
    clear_user_data(update.effective_user['id'])
    update.message.reply_text("I cleaned my memory. We're starting from scratch.\nNow it's your turn - tell me a country")
