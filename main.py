import requests
from io import BytesIO

from PIL import Image
import validators
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)

from parse_wiki import extract_first_paragraph
from photo_process import photo_classifier
from settings import BOT_TOKEN


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Send a photo or a link to jpg or png photo!')


def get_data_from_link(update: Update, _: CallbackContext) -> None:
    """Reply to url to image"""
    photo_url = update.message.text
    suffix = photo_url.split('.')[-1]
    if validators.url(photo_url) and (suffix == 'jpg' or suffix == 'png'):
        response = requests.get(photo_url, stream=True)
        img = Image.open(response.raw)
        top_model_label = photo_classifier(img)
        first_paragraph, wiki_url = extract_first_paragraph(top_model_label)
        update.message.reply_text(f'{wiki_url}\n{first_paragraph}')
    else:
        update.message.reply_text("Wrong url format. Use /help!")


def get_data_from_photo(update: Update, context: CallbackContext) -> None:
    """Reply to image sent as 'Send in a quick way' via telegram UI"""
    file = context.bot.get_file(update.message.photo[-1].file_id)
    img = Image.open(BytesIO(file.download_as_bytearray()))
    top_model_label = photo_classifier(img)
    first_paragraph, wiki_url = extract_first_paragraph(top_model_label)
    update.message.reply_text(f'{wiki_url}\n{first_paragraph}')


def launch_bot():
    """Start the bot."""
    updater = Updater(BOT_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.photo, get_data_from_photo))
    dp.add_handler(MessageHandler(Filters.text, get_data_from_link))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    launch_bot()
