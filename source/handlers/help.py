import os


RULES_TEXT = os.getenv('RULES_TEXT')


def help_handler(update, context):
    update.message.reply_text(get_help())


def get_help():
    intro = "Hi! I'm CountryChainBot and I can play a country chain game."
    commands = ' - /restart - restart current game\n - /help - get help\n'
    return intro + '\n\nRules:\n' + RULES_TEXT + '\n\nCommands:\n' + commands
