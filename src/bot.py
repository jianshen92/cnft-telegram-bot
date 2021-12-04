# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

from tbot.utils import format_message, get_price_data, replace_dash

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

load_dotenv()


def price(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    if len(context.args) == 0:
        update.message.reply_text("/price {project_name} {search_query}")
        return

    if len(context.args) > 2:
        update.message.reply_text("/price {project_name} {search_query}")
        return

    if len(context.args) == 2:
        query = replace_dash(context.args[1])
    else:
        query = ""
    project = replace_dash(context.args[0])

    data = get_price_data(project, query)
    update.message.reply_markdown_v2(
        format_message(data), disable_web_page_preview=True
    )


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ["token"])

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(
        CommandHandler(command="price", callback=price, pass_args=True)
    )
    dispatcher.add_handler(CommandHandler(command="p", callback=price, pass_args=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
