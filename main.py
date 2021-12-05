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

order_list = {}

# stages of ordering
NUMBER_OF_MEATS, DISH, CONFIRM = range(3)
# callback data
ONE_MEAT, TWO_MEATS, CHARSIEW_RICE, ROASTEDPORK_RICE, DUCK_RICE, CHARSIEW_ROASTEDPORK_RICE, CHARSIEW_DUCK_RICE, ROASTEDPORK_DUCK_RICE = range(8)

def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton("One meat", callback_data=str(ONE_MEAT)),
        InlineKeyboardButton("Two meats", callback_data=str(TWO_MEATS)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    order_string = "=====Current orders=====\n"
    for i in sorted (order_list):
        order_string += f'{i}: {order_list[i]}\n'

    update.message.reply_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
        reply_markup=reply_markup,
    )

    return NUMBER_OF_MEATS

def restart(update: Update, context: CallbackContext) -> int:
    """Restarts ordering process."""
    user = update.effective_user
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton("One meat", callback_data=str(ONE_MEAT)),
        InlineKeyboardButton("Two meats", callback_data=str(TWO_MEATS)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    order_string = "=====Current orders=====\n"
    for i in sorted (order_list):
        order_string += f'{i}: {order_list[i]}\n'

    query.edit_message_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
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
        InlineKeyboardButton("Duck rice", callback_data=str(DUCK_RICE)),
      ],
      [
        InlineKeyboardButton("Restart", callback_data=str(NUMBER_OF_MEATS)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with ONE meat.\n Choose your dish.", reply_markup=reply_markup
    )

    return DISH

def two_meats(update: Update, context: CallbackContext) -> None:
    """Ordering form for one meat options"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton("Char Siew + Roast Pork rice", callback_data=str(CHARSIEW_ROASTEDPORK_RICE)),
      ],
      [
        InlineKeyboardButton("Char Siew + Duck rice", callback_data=str(CHARSIEW_DUCK_RICE)),
      ],
      [
        InlineKeyboardButton("Roasted Pork + Duck rice", callback_data=str(ROASTEDPORK_DUCK_RICE)),
      ],
      [
        InlineKeyboardButton("Restart", callback_data=str(NUMBER_OF_MEATS)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with TWO meats.\n Choose your dish.", reply_markup=reply_markup
    )

    return DISH

def charsiew_rice(update: Update, context: CallbackContext) -> None:
    """Orders Char Siew rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Go back to the start", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Char Siew rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew rice", reply_markup=reply_markup
    )

    return CONFIRM

def roastedpork_rice(update: Update, context: CallbackContext) -> None:
    """Orders Roasted Pork rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Go back to the start", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Roasted Pork rice"

    query.edit_message_text(
        text="Confirmed order: Roasted Pork rice", reply_markup=reply_markup
    )

    return CONFIRM

def duck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Go back to the start", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Duck rice"

    query.edit_message_text(
        text="Confirmed order: Duck rice", reply_markup=reply_markup
    )

    return CONFIRM

def charsiewroastedpork_rice(update: Update, context: CallbackContext) -> None:
    """Orders Charsiew + Roasted Pork rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Go back to the start", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user = update.effective_user
    order_list[user.first_name] = "Char Siew + Roasted Pork rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew + Roasted Pork rice", reply_markup=reply_markup
    )
   
    return CONFIRM

def charsiewduck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Charsiew + Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Restart", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Char Siew + Duck rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew + Duck rice", reply_markup=reply_markup
    )

    return CONFIRM

def roastedporkduck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Roasted Pork + Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Go back to the start", callback_data=str(NUMBER_OF_MEATS)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Roasted Pork + Duck rice"

    query.edit_message_text(
        text="Confirmed: Roasted Pork + Duck rice", reply_markup=reply_markup
    )

    return CONFIRM

def confirm(update: Update, context: CallbackContext) -> None:
    """Confirms the order."""
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text="Your order has been confirmed."
    )
    return CONFIRM

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
                CallbackQueryHandler(two_meats, pattern='^' + str(TWO_MEATS) + '$'),
            ],
            DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(NUMBER_OF_MEATS) + '$'),
                CallbackQueryHandler(charsiew_rice, pattern='^' + str(CHARSIEW_RICE) + '$'),
                CallbackQueryHandler(roastedpork_rice, pattern='^' + str(ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(duck_rice, pattern='^' + str(DUCK_RICE) + '$'),
                CallbackQueryHandler(charsiewroastedpork_rice, pattern='^' + str(CHARSIEW_ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(charsiewduck_rice, pattern='^' + str(CHARSIEW_DUCK_RICE) + '$'),
                CallbackQueryHandler(roastedporkduck_rice, pattern='^' + str(ROASTEDPORK_DUCK_RICE) + '$'),
            ],
            CONFIRM: [
                CallbackQueryHandler(restart, pattern='^' + str(NUMBER_OF_MEATS) + '$'),
                CallbackQueryHandler(restart, pattern='^' + str(CONFIRM) + '$'),
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