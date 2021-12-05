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
condensed_list = {}

# stages of ordering
ORDER_LIST, RESTAURANTS, RONGLIANG, MRBEAN, RONG_LIANG_ONE_MEAT_DISH, RONG_LIANG_TWO_MEATS_DISH, PANCAKE, EGGWICH, DRINKS = range(9)

# callback data
RESTART = 0

# Rong Liang
ONE_MEAT, TWO_MEATS = range(1,3)
CHARSIEW_RICE, ROASTEDPORK_RICE, DUCK_RICE = range(1,4) 
CHARSIEW_ROASTEDPORK_RICE, CHARSIEW_DUCK_RICE, ROASTEDPORK_DUCK_RICE = range(1,4)

charsiew_rice = "Char Siew rice"
roastedpork_rice = "Roasted Pork rice"
duck_rice = "Duck rice"
charsiewroastedpork_rice = "Char Siew + Roasted Pork rice"
charsiewduck_rice = "Char Siew + Duck rice"
roastedporkduck_rice = "Roasted Pork + Duck rice"

# Mr Bean
PEANUTBUTTER_PANCAKE, REDBEAN_PANCAKE, TUNA_PANCAKE, CHICKENMAYO_PANCAKE = range(1,5)
KAYACHEESE_PANCAKE, HAZELNUT_PANCAKE, CHOCOLATE_PANCAKE, EGGMAYO_PANCAKE = range(5,9)
CHEESE_PANCAKE = 9
CHICKENHAMANDEGG_EGGWICH, MUSHROOMSAUSAGEANDCHEESE_EGGWICH = range(1,3)
HOT_SOYAMILK, COLD_SOYAMILK, COLD_GRASSJELLY = range(1,4)

peanutbutter_pancake = "Peanut Butter pancake"
redbean_pancake = "Red Bean pancake"
tuna_pancake = "Tuna pancake"
chickenmayo_pancake = "Chicken Mayo pancake"
kayacheese_pancake = "Kaya Cheese pancake"
hazelnut_pancake = "Hazelnut pancake"
chocolate_pancake = "Chocolate pancake"
eggmayo_pancake = "Egg Mayo pancake"
cheese_pancake = "Cheese pancake"

chickenhamandegg_eggwich = "Chicken Ham & Egg eggwich"
mushroomsausageandcheese_eggwich = "Mushroom Sausage & Cheese eggwich"

hot_soyamilk = "Hot soya milk"
cold_soyamilk = "Cold soya milk"
cold_grassjelly = "Cold grass jelly drink"

def start(update: Update, context: CallbackContext) -> int:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    logger.info("User %s started the conversation.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
        [
            InlineKeyboardButton("Rong Liang", callback_data=str(RONGLIANG)),
            InlineKeyboardButton("Mr Bean", callback_data=str(MRBEAN)),
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

    order_string += "\n====Condensed orders====\n"
    for k in sorted (condensed_list):
        order_string += f'{condensed_list[k]}x {k}\n'

    update.message.reply_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
        reply_markup=reply_markup,
    )

    return RESTAURANTS

# def clear(update: Update, context: CallbackContext) -> int:
#     """Clears all existing orders"""
#     for i in sorted (order_list):
#         order

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
            InlineKeyboardButton("Rong Liang", callback_data=str(RONGLIANG)),
            InlineKeyboardButton("Mr Bean", callback_data=str(MRBEAN)),
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

    order_string += "\n====Condensed orders====\n"
    for k in sorted (condensed_list):
        order_string += f'{condensed_list[k]}x {k}\n'

    query.edit_message_text(
        f'Hi {user.first_name}. Start ordering now!\n{order_string}',
        reply_markup=reply_markup,
    )

    return RESTAURANTS

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

def mrbean(update: Update, context: CallbackContext) -> int:
    """Mr Bean ordering menu"""
    user = update.effective_user
    query = update.callback_query
    query.answer()
    logger.info("User %s has selected Mr Bean.", user.first_name)

    # build InlineKeyboard for food ordering
    keyboard = [
        [
            InlineKeyboardButton("Pancake", callback_data=str(PANCAKE)),
            InlineKeyboardButton("Eggwich", callback_data=str(EGGWICH)),
            InlineKeyboardButton("Drinks", callback_data=str(DRINKS)), 
        ],
        [
            InlineKeyboardButton("Restart", callback_data=str(RESTART)),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'You have selected Mr Bean. Choose your selection now.',
        reply_markup=reply_markup,
    )

    return MRBEAN

def pancake(update: Update, context: CallbackContext) -> int:
    """Mr Bean pancakes ordering menu"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
        [InlineKeyboardButton(peanutbutter_pancake, callback_data=str(PEANUTBUTTER_PANCAKE))],
        [InlineKeyboardButton(redbean_pancake, callback_data=str(REDBEAN_PANCAKE))],
        [InlineKeyboardButton(tuna_pancake, callback_data=str(TUNA_PANCAKE))], 
        [InlineKeyboardButton(chickenmayo_pancake, callback_data=str(CHICKENMAYO_PANCAKE))], 
        [InlineKeyboardButton(kayacheese_pancake, callback_data=str(KAYACHEESE_PANCAKE))], 
        [InlineKeyboardButton(hazelnut_pancake, callback_data=str(HAZELNUT_PANCAKE))], 
        [InlineKeyboardButton(chocolate_pancake, callback_data=str(CHOCOLATE_PANCAKE))], 
        [InlineKeyboardButton(eggmayo_pancake, callback_data=str(EGGMAYO_PANCAKE))], 
        [InlineKeyboardButton(cheese_pancake, callback_data=str(CHEESE_PANCAKE))],
        [InlineKeyboardButton("Restart", callback_data=str(RESTART))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'You have selected Mr Bean pancakes. Choose your selection now.',
        reply_markup=reply_markup,
    )

    return PANCAKE

def eggwich(update: Update, context: CallbackContext) -> int:
    """Mr Bean eggwich ordering menu"""
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
        [InlineKeyboardButton(chickenhamandegg_eggwich, callback_data=str(CHICKENHAMANDEGG_EGGWICH))],
        [InlineKeyboardButton(mushroomsausageandcheese_eggwich, callback_data=str(MUSHROOMSAUSAGEANDCHEESE_EGGWICH))],
        [InlineKeyboardButton("Restart", callback_data=str(RESTART))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'You have selected Mr Bean eggwiches. Choose your selection now.',
        reply_markup=reply_markup,
    )

    return EGGWICH

def drinks(update: Update, context: CallbackContext) -> int:
    """Mr Bean drinks ordering menu"""
    user = update.effective_user
    query = update.callback_query
    query.answer()

    # build InlineKeyboard for food ordering
    keyboard = [
        [InlineKeyboardButton(hot_soyamilk, callback_data=str(HOT_SOYAMILK))],
        [InlineKeyboardButton(cold_soyamilk, callback_data=str(COLD_SOYAMILK))],
        [InlineKeyboardButton(cold_grassjelly, callback_data=str(COLD_GRASSJELLY))], 
        [InlineKeyboardButton("Restart", callback_data=str(RESTART))],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        f'You have selected Mr Bean drinks. Choose your selection now.',
        reply_markup=reply_markup,
    )

    return DRINKS

def dish(input_name):
    def func(update: Update, context: CallbackContext) -> int:
        """Orders dish_name"""
        dish_name = input_name
        query = update.callback_query
        query.answer()
        keyboard = [
            [
                InlineKeyboardButton("See orders/Order more", callback_data=str(RESTART)),
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
        
        if dish_name in condensed_list:
            condensed_list[dish_name] += 1
        else:
            condensed_list[dish_name] = 1

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
                CallbackQueryHandler(mrbean, pattern='^' + str(MRBEAN) + '$')
            ],
            RONGLIANG: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(one_meat, pattern='^' + str(ONE_MEAT) + '$'),
                CallbackQueryHandler(two_meats, pattern='^' + str(TWO_MEATS) + '$'),
            ],
            RONG_LIANG_ONE_MEAT_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(dish(charsiew_rice), pattern='^' + str(CHARSIEW_RICE) + '$'),
                CallbackQueryHandler(dish(roastedpork_rice), pattern='^' + str(ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(dish(duck_rice), pattern='^' + str(DUCK_RICE) + '$'), 
            ],
            RONG_LIANG_TWO_MEATS_DISH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(dish(charsiewroastedpork_rice), pattern='^' + str(CHARSIEW_ROASTEDPORK_RICE) + '$'),
                CallbackQueryHandler(dish(charsiewduck_rice), pattern='^' + str(CHARSIEW_DUCK_RICE) + '$'),
                CallbackQueryHandler(dish(roastedporkduck_rice), pattern='^' + str(ROASTEDPORK_DUCK_RICE) + '$'),
            ],
            MRBEAN: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(pancake, pattern='^' + str(PANCAKE) + '$'),
                CallbackQueryHandler(eggwich, pattern='^' + str(EGGWICH) + '$'),
                CallbackQueryHandler(drinks, pattern='^' + str(DRINKS) + '$'),
            ],
            PANCAKE: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(dish(peanutbutter_pancake), pattern='^' + str(PEANUTBUTTER_PANCAKE) + '$'),
                CallbackQueryHandler(dish(redbean_pancake), pattern='^' + str(REDBEAN_PANCAKE) + '$'),
                CallbackQueryHandler(dish(tuna_pancake), pattern='^' + str(TUNA_PANCAKE) + '$'),
                CallbackQueryHandler(dish(chickenmayo_pancake), pattern='^' + str(CHICKENMAYO_PANCAKE) + '$'),
                CallbackQueryHandler(dish(kayacheese_pancake), pattern='^' + str(KAYACHEESE_PANCAKE) + '$'),
                CallbackQueryHandler(dish(hazelnut_pancake), pattern='^' + str(HAZELNUT_PANCAKE) + '$'),
                CallbackQueryHandler(dish(chocolate_pancake), pattern='^' + str(CHOCOLATE_PANCAKE) + '$'),
                CallbackQueryHandler(dish(eggmayo_pancake), pattern='^' + str(EGGMAYO_PANCAKE) + '$'),
                CallbackQueryHandler(dish(cheese_pancake), pattern='^' + str(CHEESE_PANCAKE) + '$'),
            ],
            EGGWICH: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(dish(chickenhamandegg_eggwich), pattern='^' + str(CHICKENHAMANDEGG_EGGWICH) + '$'),
                CallbackQueryHandler(dish(mushroomsausageandcheese_eggwich), pattern='^' + str(MUSHROOMSAUSAGEANDCHEESE_EGGWICH) + '$'),
            ],
            DRINKS: [
                CallbackQueryHandler(restart, pattern='^' + str(RESTART) + '$'),
                CallbackQueryHandler(dish(hot_soyamilk), pattern='^' + str(HOT_SOYAMILK) + '$'),
                CallbackQueryHandler(dish(cold_soyamilk), pattern='^' + str(COLD_SOYAMILK) + '$'),
                CallbackQueryHandler(dish(cold_grassjelly), pattern='^' + str(COLD_GRASSJELLY) + '$'),
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