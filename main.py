import telebot
from telebot import types
import random
from database import Database

bot = telebot.TeleBot("7552632953:AAHkhCDydlXxytzBM96FgZ5M4gAU15pn5D4")
bot_name="aero33_bot"
db = Database()

user_data = {}

def generate_capcha():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    return num1, num2, num1 + num2

def require_captcha(func):
    def wrapper(message):
        user_id = message.chat.id

        # Проверяем, прошел ли пользователь капчу
        if user_id not in user_data or not user_data[user_id].get('capcha_solved', False):
            num1, num2, answer = generate_capcha()
            user_data[user_id] = {
                'capcha_answer': answer,
                'capcha_solved': False,
                'user_id':str(message.text[7:])
            }
            bot.send_message(user_id, f'Для продолжения работы пройдите проверку: {num1} + {num2} = ?')
            return  # Прекращаем выполнение, не вызывая оригинальную функцию
        print("Капча пройдена")  # Уведомление, если капча пройдена
        return func(message)  # Если капча пройдена, вызываем оригинальную функцию
    return wrapper

def menu(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text="Условия работы", callback_data="work")
    btn2 = types.InlineKeyboardButton(text="Баланс", callback_data="balance")
    btn3 = types.InlineKeyboardButton(text="Реферальная система", callback_data="ref")
    btn4 = types.InlineKeyboardButton(text="Задания", callback_data="tasks")
    btn5 = types.InlineKeyboardButton(text="Смена языка", callback_data="language")
    btn6 = types.InlineKeyboardButton(text="Вывод средств", callback_data="withdrawal")
    btn7 = types.InlineKeyboardButton(text="Веб-сайт", callback_data="web-site")

    markup.row(btn1, btn2)
    markup.row(btn3, btn4)
    markup.row(btn5, btn6)
    markup.row(btn7)
    bot.send_message(message.chat.id, "Выберите опцию", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "work":
        bot.send_message(call.message.chat.id, "Вы выбрали работу!")
    elif call.data == "balance":
        ...
    elif call.data == "ref":
        bot.send_message(call.message.chat.id, f" Ваша реферальная ссылка : \nhttps://t.me/{bot_name}?start={call.from_user.id}\nКол-во рефералов - {db.count_referers(call.from_user.id)}")
    elif call.data == "tasks":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Скачать игру", callback_data="download")
        btn2 = types.InlineKeyboardButton(text="Подписаться на соцсети", callback_data="subscribe")
        btn3 = types.InlineKeyboardButton(text="Выложить пост в соцсетях", callback_data="repost")
        btn4 = types.InlineKeyboardButton(text="Назад в меню", callback_data="back")
        markup.row(btn1)
        markup.row(btn2)
        markup.row(btn3)
        markup.row(btn4)
        bot.send_message(call.message.chat.id, "Список заданий", reply_markup=markup)
    elif call.data == "withdrawal":
        ...
    elif call.data == "language":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="Английский", callback_data="en")
        btn2 = types.InlineKeyboardButton(text="Русский", callback_data="ru")
        btn3 = types.InlineKeyboardButton(text="Назад в меню", callback_data="back")
        markup.row(btn1, btn2)
        markup.row(btn3)
        bot.send_message(call.message.chat.id, "Выберите язык", reply_markup=markup)
    elif call.data == "web-site":
        bot.send_message(call.message.chat.id, "ВЕБ-САЙТ")
    elif call.data == "back":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        menu(call.message)



@bot.message_handler(commands=['start'])
@require_captcha
def start(message):
    print(message.from_user.first_name)
    print(message.text)
    # user_id = message.chat.id
    # referer_id=user_data[user_id]['user_id']
    # if not db.user_exists(message.from_user.id):
    #     print(user_data[user_id]['user_id'])
    #     if referer_id != '':
    #         if str(referer_id) != str(message.from_user.id):
    #             db.add_user(message.from_user.id, referer_id)
    #             try:
    #                 bot.send_message(referer_id, "По вашей ссылке зарегистрировался новый пользователь")
    #             except:
    #                 pass
    #         else:
    #             bot.send_message(message.from_user.id,"Регистрироваться по своей реферальной ссылке нельзя")
    #     else:
    #         db.add_user(message.from_user.id)
    menu(message)

@bot.message_handler(commands=['menu'])
@require_captcha
def handle_menu(message):
    menu(message)

@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_id = message.chat.id
    if user_id in user_data and not user_data[user_id]['capcha_solved']:
        if message.text.isdigit():
            user_answer = int(message.text)
            correct_answer = user_data[user_id]['capcha_answer']
            if user_answer == correct_answer:
                user_data[user_id]['capcha_solved'] = True

                bot.send_message(user_id, "Капча пройдена! Добро пожаловать в меню.")
                user_id = message.chat.id
                referer_id = user_data[user_id]['user_id']
                if not db.user_exists(message.from_user.id):
                    print(user_data[user_id]['user_id'])
                    if referer_id != '':
                        if str(referer_id) != str(message.from_user.id):
                            db.add_user(message.from_user.id, referer_id)
                            try:
                                bot.send_message(referer_id, f"По вашей ссылке зарегистрировался новый пользователь {message.from_user.first_name}")
                            except:
                                pass
                        else:
                            bot.send_message(message.from_user.id,
                                             "Регистрироваться по своей реферальной ссылке нельзя")
                    else:
                        db.add_user(message.from_user.id)
                start(message)


            else:
                bot.send_message(user_id, "Неправильный ответ. Попробуйте снова.")
                num1, num2, answer = generate_capcha()
                user_data[user_id]['capcha_answer'] = answer
                bot.send_message(user_id, f'{num1} + {num2} = ?')
        else:
            bot.send_message(user_id, "Пожалуйста, введите числовой ответ.")
    else:
        if user_id in user_data and user_data[user_id]['capcha_solved']:
            menu(message)

bot.polling()