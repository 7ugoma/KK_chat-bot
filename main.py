import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

TOKEN = '7612088428:AAHeC5GaCqe7m3EUER3tiNgDr2V0EvQ5FxI'
state_storage = StateMemoryStorage()
bot = telebot.TeleBot(TOKEN, state_storage=state_storage)


user_data = {}

class Form(StatesGroup):
    full_name = State()
    birth_date = State()
    education = State()
    profession = State()
    course = State()
    practice_duration = State()

def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Трудоустройство/практика"))
    markup.add(KeyboardButton("Целевое обучение"))
    markup.add(KeyboardButton("Мероприятия"))
    markup.add(KeyboardButton("Другое"))
    return markup


def job_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Практическая подготовка"))
    markup.add(KeyboardButton("Летнее трудоустройство"))
    markup.add(KeyboardButton("Трудоустройство после обучения"))
    markup.add(KeyboardButton("Назад в меню"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выберите нужный раздел:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def back_to_main(message):
    bot.send_message(message.chat.id, "Вы вернулись в главное меню:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "Трудоустройство/практика")
def employment_practice(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=job_menu())

@bot.message_handler(func=lambda message: message.text == "Практическая подготовка")
def start_form(message):
    bot.set_state(message.chat.id, Form.full_name, message.from_user.id)
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")

@bot.message_handler(state=Form.full_name)
def get_full_name(message):
    user_data[message.from_user.id] = {}
    user_data[message.from_user.id]["full_name"] = message.text

    bot.set_state(message.chat.id, Form.birth_date, message.from_user.id)
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")

@bot.message_handler(state=Form.birth_date)
def get_birth_date(message):
    user_data[message.from_user.id]["birth_date"] = message.text

    bot.set_state(message.chat.id, Form.education, message.from_user.id)
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")

@bot.message_handler(state=Form.education)
def get_education(message):
    user_data[message.from_user.id]["education"] = message.text

    bot.set_state(message.chat.id, Form.profession, message.from_user.id)
    bot.send_message(message.chat.id, "По какой профессии/специальности?")

@bot.message_handler(state=Form.profession)
def get_profession(message):
    user_data[message.from_user.id]["profession"] = message.text

    bot.set_state(message.chat.id, Form.course, message.from_user.id)
    bot.send_message(message.chat.id, "Какой курс?")

@bot.message_handler(state=Form.course)
def get_course(message):
    user_data[message.from_user.id]["course"] = message.text

    bot.set_state(message.chat.id, Form.practice_duration, message.from_user.id)
    bot.send_message(message.chat.id, "Сроки практики?")

@bot.message_handler(state=Form.practice_duration)
def get_practice_duration(message):
    user_data[message.from_user.id]["practice_duration"] = message.text

    application_text = "\n".join([f"{key}: {value}" for key, value in user_data[message.from_user.id].items()])

    bot.send_message(message.chat.id, f"Анкета заполнена:\n\n{application_text}")
    bot.send_message(message.chat.id, "Спасибо! Ваша анкета отправлена.", reply_markup=main_menu())

    bot.delete_state(message.chat.id, message.from_user.id)

bot.polling(none_stop=True)
