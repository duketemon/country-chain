import os

from data_access import get_used_countries, set_used_countries, clear_user_data
from game import Game


GAME = Game(os.getenv('COUNTRIES_DATA_LOCATION'))


def next_move_handler(update, context):
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
