import html
import json
import logging
import requests
import traceback

from io import BytesIO
from PIL import Image
from telegram import ParseMode, Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from photo_process import photo_proc
from settings import (
    BOT_TOKEN,
    DEVELOPER_CHAT_ID,
)


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def error_handler(update: Update, context: CallbackContext):
    """Log the error and send a telegram message to notify the developer."""
    # Log the error before we do anything else, so we can see it even if something breaks.
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

    # traceback.format_exception returns the usual python message about an exception, but as a
    # list of strings rather than a single string, so we have to join them together.
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = ''.join(tb_list)

    # Build the message with some markup and additional information about what happened.
    # You might need to add some logic to deal with messages longer than the 4096 character limit.
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message = (
        f'An exception was raised while handling an update\n'
        f'<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}'
        '</pre>\n\n'
        f'<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n'
        f'<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n'
        f'<pre>{html.escape(tb_string)}</pre>'
    )

    # Finally, send the message
    context.bot.send_message(chat_id=DEVELOPER_CHAT_ID, text=message, parse_mode=ParseMode.HTML)


def help_command(update: Update, _: CallbackContext):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def photo_command(update: Update, context: CallbackContext):
    try:
        if context.args:
            argument = context.args[0]
            response = requests.get(argument, stream=True).raw
            img = Image.open(response)
            top_answers = photo_proc(img)
            update.message.reply_text(str(top_answers))
        else:
            update.message.reply_text("Send photo")

    except (IndexError, ValueError):
        update.message.reply_text('There is no link or wrong format')


def photo_message(update: Update, context: CallbackContext):
    file = context.bot.get_file(update.message.photo[-1].file_id)
    img = Image.open(BytesIO(file.download_as_bytearray()))
    top_answers = photo_proc(img)
    update.message.reply_text(str(top_answers))


def launch_bot():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(CommandHandler("photo", photo_command))
    dp.add_handler(MessageHandler(Filters.photo, photo_message))

    dp.add_error_handler(error_handler)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    launch_bot()
