import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, CallbackContext, ConversationHandler, CallbackQueryHandler, callbackqueryhandler

load_dotenv()
API_KEY = os.getenv('API_KEY')

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# stages of ordering
NUMBER_OF_MEATS, DISH = range(2)
# callback data
ONE_MEAT, TWO_MEATS, CHARSIEW_RICE, ROASTEDPORK_RICE, DUCK_RICE, CHARSIEW_ROASTPORK_RICE = range(6)

def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton("One meat", callback_data=str(NUMBER_OF_MEATS)),
        InlineKeyboardButton("Two meats", callback_data=str(NUMBER_OF_MEATS)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        f'Hi {user.name}. Start ordering now!',
        reply_markup=reply_markup,
    )

    return NUMBER_OF_MEATS

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def one_meat(update: Update, context: CallbackContext) -> None:
    """Ordering form for one meat options"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton("Char Siew rice", callback_data=str(CHARSIEW_RICE)),
      ],
      [
        InlineKeyboardButton("Roasted pork rice", callback_data=str(ROASTEDPORK_RICE)),
      ],
      [
        InlineKeyboardButton("Duck rice", callback_data=str(DUCK_RICE))
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with ONE meat.\n Choose your dish.", reply_markup=reply_markup
    )

    return DISH

def charsiew_rice(update: Update, context: CallbackContext) -> None:
    """Orders Char Siew rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirm order", callback_data="confirm"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Confirm your order: Charsiew rice", reply_markup=reply_markup
    )

    return DISH

def roastedpork_rice(update: Update, context: CallbackContext) -> None:
    """Orders Roasted Pork rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirm order", callback_data="confirm"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Confirm your order: Roasted Pork rice", reply_markup=reply_markup
    )

    return DISH

def duck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Confirm order", callback_data="confirm"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Confirm your order: Duck rice", reply_markup=reply_markup
    )

    return DISH


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            NUMBER_OF_MEATS: [
                CallbackQueryHandler(one_meat, pattern='^' + str(ONE_MEAT) + '$'),
            ],
            DISH: [
                CallbackQueryHandler(charsiew_rice, pattern='^' + str(CHARSIEW_RICE) + '$'),
                CallbackQueryHandler(roastedpork_rice, pattern='^' + str(ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(duck_rice, pattern='^' + str(DUCK_RICE) + '$'),
            ]
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()