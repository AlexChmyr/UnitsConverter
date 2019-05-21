from pathlib import Path
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from converter.controller import calculate

TOKEN_FILE = "token.txt"
DATA_URL = 'http://resources.finance.ua/ru/public/currency-cash.json'
TOKEN = Path(TOKEN_FILE).read_text().strip()


#handlers
def start(update, context):
    """Command /start"""
    print("Command /start received")
    update.message.reply_text('Hello! What can I do for you?')


def convert(update, context):
    """Convert values"""
    msg = update.message
    response = calculate(msg["text"])
    msg.bot.send_message(msg.chat_id, response)


updater = Updater(token=TOKEN, use_context=True)
dp = updater.dispatcher


# handler
dp.add_handler(CommandHandler('start',start))
dp.add_handler(MessageHandler(Filters.regex('[С|с]колько .*'),convert))

# run
updater.start_polling()
updater.idle()
