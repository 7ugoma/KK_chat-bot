import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

user_data = {}
EMAIL_ADDRESS = ""
PASSWORD = ""


def send_email(subject, body, to_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(EMAIL_ADDRESS, PASSWORD)
        smtpObj.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        smtpObj.quit()

        return True
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        return False


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


def contact_channel_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Телефон"))
    markup.add(KeyboardButton("WhatsApp"))
    markup.add(KeyboardButton("Telegram"))
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
    user_data[message.chat.id] = {"step": "full_name"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name")
def get_full_name(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date")
def get_birth_date(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "education"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "education")
def get_education(message):
    user_data[message.chat.id]["education"] = message.text
    user_data[message.chat.id]["step"] = "profession"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "profession")
def get_profession(message):
    user_data[message.chat.id]["profession"] = message.text
    user_data[message.chat.id]["step"] = "course"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "course")
def get_course(message):
    user_data[message.chat.id]["course"] = message.text
    user_data[message.chat.id]["step"] = "practice_duration"
    bot.send_message(message.chat.id, "Сроки практики?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "practice_duration")
def get_practice_duration(message):
    user_data[message.chat.id]["practice_duration"] = message.text
    user_data[message.chat.id]["step"] = "previous_practice"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "previous_practice")
def get_previous_practice(message):
    user_data[message.chat.id]["previous_practice"] = message.text
    user_data[message.chat.id]["step"] = "same_department"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "same_department")
def get_same_department(message):
    user_data[message.chat.id]["same_department"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel")
def get_contact_channel(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number")
def get_phone_number(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key != "step"])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "confirm_send")
def confirm_send(message):
    if message.text.lower() == "отправить":
        application_text = "\n".join(
            [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key != "step"])
        subject = "Новая анкета для практики"
        to_email = EMAIL_ADDRESS
        if send_email(subject, application_text, to_email):
            bot.send_message(message.chat.id, "Анкета успешно отправлена по электронной почте.")
        else:
            bot.send_message(message.chat.id, "Ошибка при отправке анкеты по электронной почте.")
        bot.send_message(message.chat.id, f"Анкета отправлена:\n\n{application_text}")
        bot.send_message(message.chat.id, "Спасибо! Ваша анкета отправлена.", reply_markup=main_menu())

        del user_data[message.chat.id]
    elif message.text.lower() == "редактировать":
        user_data[message.chat.id]["step"] = "full_name"
        bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.")


bot.polling(none_stop=True)
