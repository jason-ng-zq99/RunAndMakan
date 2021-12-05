import logging
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, ConversationHandler, CallbackQueryHandler

load_dotenv()
API_KEY = os.getenv('API_KEY')

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

order_list = {}

# stages of ordering
ORDER_LIST, NUMBER_OF_MEATS, ONE_MEAT_DISH, TWO_MEATS_DISH = range(4)
# callback data
RESTART = 0
ONE_MEAT, TWO_MEATS = range(1,3)
CHARSIEW_RICE, ROASTEDPORK_RICE, DUCK_RICE = range(1,4) 
CHARSIEW_ROASTEDPORK_RICE, CHARSIEW_DUCK_RICE, ROASTEDPORK_DUCK_RICE = range(1,4)

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
        InlineKeyboardButton("Restart", callback_data=str(RESTART)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with ONE meat.\n Choose your dish.", reply_markup=reply_markup
    )

    return ONE_MEAT_DISH

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
        InlineKeyboardButton("Restart", callback_data=str(RESTART)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with TWO meats.\n Choose your dish.", reply_markup=reply_markup
    )

    return TWO_MEATS_DISH

def charsiew_rice(update: Update, context: CallbackContext) -> None:
    """Orders Char Siew rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Char Siew rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew rice", reply_markup=reply_markup
    )

    return ORDER_LIST

def roastedpork_rice(update: Update, context: CallbackContext) -> None:
    """Orders Roasted Pork rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Roasted Pork rice"

    query.edit_message_text(
        text="Confirmed order: Roasted Pork rice", reply_markup=reply_markup
    )

    return ORDER_LIST

def duck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Duck rice"

    query.edit_message_text(
        text="Confirmed order: Duck rice", reply_markup=reply_markup
    )

    return ORDER_LIST

def charsiewroastedpork_rice(update: Update, context: CallbackContext) -> None:
    """Orders Charsiew + Roasted Pork rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    user = update.effective_user
    order_list[user.first_name] = "Char Siew + Roasted Pork rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew + Roasted Pork rice", reply_markup=reply_markup
    )
   
    return ORDER_LIST

def charsiewduck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Charsiew + Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Char Siew + Duck rice"

    query.edit_message_text(
        text="Confirmed order: Charsiew + Duck rice", reply_markup=reply_markup
    )

    return ORDER_LIST

def roastedporkduck_rice(update: Update, context: CallbackContext) -> None:
    """Orders Roasted Pork + Duck rice"""
    query = update.callback_query
    query.answer()
    keyboard = [
        [
            InlineKeyboardButton("See orders", callback_data=str(RESTART)),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    user = update.effective_user
    order_list[user.first_name] = "Roasted Pork + Duck rice"

    query.edit_message_text(
        text="Confirmed: Roasted Pork + Duck rice", reply_markup=reply_markup
    )

    return ORDER_LIST

def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(API_KEY)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ORDER_LIST: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
            ],
            NUMBER_OF_MEATS: [
                CallbackQueryHandler(one_meat, pattern='^' + str(ONE_MEAT) + '$'),
                CallbackQueryHandler(two_meats, pattern='^' + str(TWO_MEATS) + '$'),
            ],
            ONE_MEAT_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(charsiew_rice, pattern='^' + str(CHARSIEW_RICE) + '$'),
                CallbackQueryHandler(roastedpork_rice, pattern='^' + str(ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(duck_rice, pattern='^' + str(DUCK_RICE) + '$'), 
            ],
            TWO_MEATS_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(charsiewroastedpork_rice, pattern='^' + str(CHARSIEW_ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(charsiewduck_rice, pattern='^' + str(CHARSIEW_DUCK_RICE) + '$'),
                CallbackQueryHandler(roastedporkduck_rice, pattern='^' + str(ROASTEDPORK_DUCK_RICE) + '$'),
            ],
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