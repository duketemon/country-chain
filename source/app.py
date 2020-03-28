import os
import logging

from collections import defaultdict
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from game import Game


TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GAME = Game('countries.txt')
USED_WORDS = defaultdict(list)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def clear_user_data(user_id: int):
    USED_WORDS[user_id].clear()


def is_valid_move(update, user_id: int, user_country: str):
    user_country_id = GAME.get_country_id(user_country)

    if user_country_id is None:
        update.message.reply_text(f'Never heard about "{user_country}". Try again.')
        return False

    last_used_country = GAME.get_country(USED_WORDS[user_id][-1]) if USED_WORDS[user_id] else None
    if last_used_country is not None and user_country[0].lower() != last_used_country[-1].lower():
        update.message.reply_text(
            f'Nooope. The country should starts with the "{last_used_country[-1].upper()}" letter.'
        )
        return False

    if user_country_id in USED_WORDS[user_id]:
        update.message.reply_text(f'Nooope. {user_country} have been used before.')
        return False

    USED_WORDS[user_id].append(user_country_id)
    return True


def move_handler(update, context):
    if update.message:  # your bot can receive updates without messages
        user_id = update.effective_user['id']
        user_country = update.message.text

        if is_valid_move(update, user_id, user_country):
            candidate_country_id, candidate_country = GAME.next_move(user_country, USED_WORDS[user_id])
            if candidate_country_id is None:
                clear_user_data(user_id)
                update.message.reply_text(
                    f'There is no more countries starts with "{user_country[-1]}" letter.\n'
                    'Congratulations! You won.'
                )
            else:
                USED_WORDS[user_id].append(candidate_country_id)
                if GAME.have_candidates(candidate_country, USED_WORDS[user_id]):
                    update.message.reply_text(candidate_country)
                else:
                    update.message.reply_text(
                        candidate_country +
                        f'\nI won. There is no more countries starts with "{candidate_country[-1]}" letter.'
                    )
                    clear_user_data(user_id)


def start_handler(update, context):
    update.message.reply_text('Start')


def restart_handler(update, context):
    update.message.reply_text('Restart')


def error(update, context):
    """Log Errors caused by Updates."""
    LOGGER.warning('Update "%s" caused error "%s"', update, context.error)


if __name__ == '__main__':
    """Run bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("restart", restart_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, move_handler))
    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", start))
    # dp.add_handler(CommandHandler("set", set_timer,
    #                               pass_args=True,
    #                               pass_job_queue=True,
    #                               pass_chat_data=True))

    # log all errors
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()
