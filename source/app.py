import os
import json
import logging
import redis

from string import Template
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from game import Game


with open('resources/service.config') as json_file:
    CONFIG = json.load(json_file)


REDIS_CLIENT = redis.Redis(host=CONFIG["redis-host"], port=CONFIG["redis-port"], db=0)
USED_COUNTRIES_BY_USER = Template(CONFIG["redis-used-countries-template"])
COUNTRIES_SEPARATOR = CONFIG["redis-countries-separator"]

TELEGRAM_TOKEN = CONFIG["telegram-bot-token"]
GAME = Game(CONFIG["data-location"])
RULES_TEXT = CONFIG["game-rules"]
SESSION_LIFETIME = CONFIG["session-lifetime"]

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def get_used_countries(user_id: int):
    used_countries = REDIS_CLIENT.get(USED_COUNTRIES_BY_USER.substitute(user_id=user_id))
    if used_countries is not None:
        return [int(c) for c in used_countries.decode("utf-8").split(COUNTRIES_SEPARATOR)]
    return []


def set_used_countries(user_id: int, used_countries: [int]):
    REDIS_CLIENT.set(
        name=USED_COUNTRIES_BY_USER.substitute(user_id=user_id),
        value=COUNTRIES_SEPARATOR.join([str(c) for c in used_countries]).encode("utf-8"),
        ex=SESSION_LIFETIME
    )


def clear_user_data(user_id: int):
    REDIS_CLIENT.delete(USED_COUNTRIES_BY_USER.substitute(user_id=user_id))


def is_valid_move(update, user_country: str, used_countries: [str]):
    user_country_id = GAME.get_country_id(user_country)

    if user_country_id is None:
        update.message.reply_text(f'Never heard about "{user_country}". Try again.')
        return False

    last_used_country = GAME.get_country(used_countries[-1]) if used_countries else None
    if last_used_country is not None and user_country[0].lower() != last_used_country[-1].lower():
        update.message.reply_text(
            f'Nooope. The country should starts with the "{last_used_country[-1].upper()}" letter.'
        )
        return False

    if user_country_id in used_countries:
        update.message.reply_text(f'Nooope. {user_country} have been used before.')
        return False

    used_countries.append(user_country_id)
    return True


def move_handler(update, context):
    if update.message:  # your bot can receive updates without messages
        user_id = update.effective_user['id']
        user_country = update.message.text
        used_countries = get_used_countries(user_id)

        if is_valid_move(update, user_country, used_countries):
            candidate_country_id, candidate_country = GAME.next_move(user_country, used_countries)
            if candidate_country_id is not None:
                used_countries.append(candidate_country_id)
                if GAME.have_candidates(candidate_country, used_countries):
                    update.message.reply_text(candidate_country)
                    set_used_countries(user_id, used_countries)
                else:
                    update.message.reply_text(
                        candidate_country +
                        f'\nI won. There is no more countries starts with "{candidate_country[-1]}" letter.\n'
                        'If you want to play a new game send me a country name.'
                    )
                    clear_user_data(user_id)
            else:
                update.message.reply_text(
                    'Congratulations! You won.'
                    f'There is no more countries starts with "{user_country[-1]}" letter.\n'
                    'If you want to play a new game send me a country name.'
                )
                clear_user_data(user_id)


def get_help():
    intro = "Hi! I'm CountryChainBot and I can play a country chain game."
    commands = ' - /restart - restart current game\n - /help - get help\n'

    return intro + '\n\nRules:\n' + RULES_TEXT + '\n\nCommands:\n' + commands


def start_handler(update, context):
    update.message.reply_text(get_help() + "\n\nIf you want to start a game send me any country name you want")


def restart_handler(update, context):
    clear_user_data(update.effective_user['id'])
    update.message.reply_text("I cleaned my memory. We're starting from scratch.\nNow it's your turn")


def help_handler(update, context):
    update.message.reply_text(get_help())


def error(update, context):
    LOGGER.warning(f'The error "{context.error}" occurred in update "{str(update)}"')


def run_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start_handler))
    dispatcher.add_handler(CommandHandler("restart", restart_handler))
    dispatcher.add_handler(CommandHandler("help", help_handler))
    dispatcher.add_handler(MessageHandler(Filters.text, move_handler))
    dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    print('Service started...')
    updater.idle()


run_bot()
