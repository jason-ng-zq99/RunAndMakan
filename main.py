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
ORDER_LIST, RESTAURANTS, RONGLIANG, RONG_LIANG_ONE_MEAT_DISH, RONG_LIANG_TWO_MEATS_DISH = range(5)
# callback data
RESTART = 0
ONE_MEAT, TWO_MEATS = range(1,3)
CHARSIEW_RICE, ROASTEDPORK_RICE, DUCK_RICE = range(1,4) 
CHARSIEW_ROASTEDPORK_RICE, CHARSIEW_DUCK_RICE, ROASTEDPORK_DUCK_RICE = range(1,4)

charsiew_rice = "Char Siew rice"
roastedpork_rice = "Roasted Pork rice"
duck_rice = "Duck rice"
charsiewroastedpork_rice = "Char Siew + Roasted Pork rice"
charsiewduck_rice = "Char Siew + Duck rice"
roastedporkduck_rice = "Roasted Pork + Duck rice"

def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
        [
            InlineKeyboardButton("Rong Liang", callback_data=str(RONGLIANG)),
        ],
        [
            InlineKeyboardButton("Refresh order list", callback_data=str(RESTART)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    order_string = "=====Current orders=====\n"
    for i in sorted (order_list):
        order_string += f'{i}:\n'
        for j in sorted (order_list[i]): 
            order_string += f'{order_list[i][j]}x {j}\n'

    update.message.reply_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
        reply_markup=reply_markup,
    )

    return RESTAURANTS

def rongliang(update: Update, context: CallbackContext) -> int:
    """Rong Liang ordering menu"""
    user = update.effective_user
    query = update.callback_query
    query.answer()
    logger.info("User %s has selected Rong Liang.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
        [
            InlineKeyboardButton("One meat", callback_data=str(ONE_MEAT)),
            InlineKeyboardButton("Two meats", callback_data=str(TWO_MEATS)), 
        ],
        [
            InlineKeyboardButton("Restart", callback_data=str(RESTART)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'You have selected Rong Liang. Choose your selection now.',
        reply_markup=reply_markup,
    )

    return RONGLIANG

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
        ],
        [
            InlineKeyboardButton("Refresh order list", callback_data=str(RESTART)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    order_string = "=====Current orders=====\n"
    for i in sorted (order_list):
        order_string += f'{i}:\n'
        for j in sorted (order_list[i]): 
            order_string += f'{order_list[i][j]}x {j}\n'


    query.edit_message_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
        reply_markup=reply_markup,
    )

    return RONGLIANG

def help_command(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def one_meat(update: Update, context: CallbackContext) -> int:
    """Ordering form for one meat options"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton(charsiew_rice, callback_data=str(CHARSIEW_RICE)),
      ],
      [
        InlineKeyboardButton(roastedpork_rice, callback_data=str(ROASTEDPORK_RICE)),
      ],
      [
        InlineKeyboardButton(duck_rice, callback_data=str(DUCK_RICE)),
      ],
      [
        InlineKeyboardButton("Restart", callback_data=str(RESTART)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with ONE meat.\n Choose your dish.", reply_markup=reply_markup
    )

    return RONG_LIANG_ONE_MEAT_DISH

def two_meats(update: Update, context: CallbackContext) -> int:
    """Ordering form for one meat options"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
      [
        InlineKeyboardButton(charsiewroastedpork_rice, callback_data=str(CHARSIEW_ROASTEDPORK_RICE)),
      ],
      [
        InlineKeyboardButton(charsiewduck_rice, callback_data=str(CHARSIEW_DUCK_RICE)),
      ],
      [
        InlineKeyboardButton(roastedporkduck_rice, callback_data=str(ROASTEDPORK_DUCK_RICE)),
      ],
      [
        InlineKeyboardButton("Restart", callback_data=str(RESTART)),
      ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        text="You chose to order a dish with TWO meats.\n Choose your dish.", reply_markup=reply_markup
    )

    return RONG_LIANG_TWO_MEATS_DISH

def rongliang_dish(input_name):
    def func(update: Update, context: CallbackContext) -> int:
        """Orders dish_name"""
        dish_name = input_name
        query = update.callback_query
        query.answer()
        keyboard = [
            [
                InlineKeyboardButton("See orders", callback_data=str(RESTART)),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        user = update.effective_user

        if user.first_name in order_list:
            if dish_name in order_list[user.first_name]:
                order_list[user.first_name][dish_name] += 1
            else: 
                order_list[user.first_name][dish_name] = 1
        else:
            order_list[user.first_name] = {}
            order_list[user.first_name][dish_name] = 1

        query.edit_message_text(
            text=f"Confirmed order: {dish_name}", reply_markup=reply_markup
        )

        return ORDER_LIST
    return func


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
            RESTAURANTS: [
                CallbackQueryHandler(rongliang, pattern='^' + str(RONGLIANG) + '$'),
            ],
            RONGLIANG: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(one_meat, pattern='^' + str(ONE_MEAT) + '$'),
                CallbackQueryHandler(two_meats, pattern='^' + str(TWO_MEATS) + '$'),
            ],
            RONG_LIANG_ONE_MEAT_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(rongliang_dish(charsiew_rice), pattern='^' + str(CHARSIEW_RICE) + '$'),
                CallbackQueryHandler(rongliang_dish(roastedpork_rice), pattern='^' + str(ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(rongliang_dish(duck_rice), pattern='^' + str(DUCK_RICE) + '$'), 
            ],
            RONG_LIANG_TWO_MEATS_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(rongliang_dish(charsiewroastedpork_rice), pattern='^' + str(CHARSIEW_ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(rongliang_dish(charsiewduck_rice), pattern='^' + str(CHARSIEW_DUCK_RICE) + '$'),
                CallbackQueryHandler(rongliang_dish(roastedporkduck_rice), pattern='^' + str(ROASTEDPORK_DUCK_RICE) + '$'),
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