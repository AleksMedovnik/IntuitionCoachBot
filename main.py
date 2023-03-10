import telebot
from telebot import types
from random import randint
from time import sleep
import config

# '5385053839:AAF9RePzgHFRXi-1xdivy82OJj9cObwbPKY'
bot = telebot.TeleBot('5385053839:AAF9RePzgHFRXi-1xdivy82OJj9cObwbPKY')
STICKER_WIN = 'CAACAgIAAxkBAAIDoGO0jZYS_ER-OChh_h69KUWB8FYkAAIVAAPANk8TzVamO2GeZOctBA'
STICKER_LOOSE = 'CAACAgIAAxkBAAID1WO1a3JS9a5B3QABQdhh_JmjFSonmwACGgADwDZPE4LbsLU8BkFXLQQ'

button_list = [
    types.InlineKeyboardButton(text='1', callback_data='1'),
    types.InlineKeyboardButton(text='2', callback_data='2'),
    types.InlineKeyboardButton(text='3', callback_data='3'),
    types.InlineKeyboardButton(text='4', callback_data='4'),
    types.InlineKeyboardButton(text='5', callback_data='5'),
]


def build_menu(lst, cols):
    return [lst[i:i + cols] for i in range(0, len(lst), cols)]


def play_again(message):
    bot.send_message(
        message.chat.id, 'Если хочешь продолжить тренировку, нажми на кнопку /train')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton('/train'))
    file = open('message.txt', 'r', encoding='UTF-8')
    text = f'Привет!, {message.from_user.username}! {file.read()}' 
    file.close()
    bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=['train'])
def train(message):
    markup = types.InlineKeyboardMarkup(build_menu(button_list, 2))
    bot.send_message(
        message.chat.id,
        f'Я загадал число от 1 до 5, а ты расслабься, включи интуицию и отгадай его!',
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    value_bot = randint(1, 5)
    value_user = int(call.data)

    if value_user == value_bot:
        text = 'Твоя интуиция сработала. Оставайся на этой волне дальше'
        sticker = STICKER_WIN
    else:
        text = f'Я загадал число {value_bot}. Расслабься и включи интуицию'
        sticker = STICKER_LOOSE

    bot.send_sticker(call.message.chat.id, sticker)
    bot.send_message(call.message.chat.id, text)
    play_again(call.message)

# for production
# if __name__ == '__main__':
#     while True:
#         try:
#             bot.polling(none_stop=True)
#         except:
#             sleep(0.3)

# for debug mode
bot.polling(non_stop=True)
