from logger import *
import binance
from telegram.ext import *
from mode import *


API_KEY = '5697862962:AAFUlNNJtJFijeJtanxCWSSFapZ79HHSI6E'
MAIN_TEXT = 'Choose command:\n/price\n/watch\n/stop_watch\n/show_watches\n/help'
_mode = Mode.NORMAL


logging.info('Starting Bot...')


def start_command(update, context):
    global MAIN_TEXT, _mode
    _mode = Mode.NORMAL
    update.message.reply_text(MAIN_TEXT)


def help_command(update, context):
    update.message.reply_text(MAIN_TEXT)


def watch_command(update, context):
    global _mode
    _mode = Mode.WATCH
    update.message.reply_text('symbol > or < level_price -->')


def stop_watch_command(update, context):
    global _mode
    _mode = Mode.STOPWATCH
    update.message.reply_text('symbol -->')


def show_watches_command(update, context):
    update.message.reply_text(binance.show_watches(update.message.chat.username))


def price_command(update, context):
    global _mode
    _mode = Mode.PRICE
    update.message.reply_text('symbol -->')


def handle_message(update, context):
    global _mode
    text = str(update.message.text).split()
    symbol = text[0]
    logging.info(f'User ({update.message.chat.id}) texts: {text}')
    userid = update.message.chat.username

    try:
        if _mode == Mode.PRICE:
            response = binance.get_price(symbol)
        elif _mode == Mode.WATCH:
            is_greater = text[1] == '>'
            level = float(text[2])
            response = binance.watch_instrument(symbol, is_greater, level, userid)
        elif _mode == Mode.STOPWATCH:
            response = binance.stop_watch(symbol, userid)
        else:
            response = MAIN_TEXT
    except binance.InvalidSymbolException as e:
        response = 'Invalid symbol'
    update.message.reply_text(response)


def error(update, context):
    logging.error(f'Update {update} \n caused error {context.error}')


# Run the programme
if __name__ == '__main__':

    updater = Updater(API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('watch', watch_command))
    dp.add_handler(CommandHandler('stop_watch', stop_watch_command))
    dp.add_handler(CommandHandler('show_watches', show_watches_command))
    dp.add_handler(CommandHandler('price', price_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()