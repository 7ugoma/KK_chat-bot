import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Токен для доступа к боту и учетные данные для отправки email
TOKEN = ''  # Замените на ваш токен Telegram бота
bot = telebot.TeleBot(TOKEN)

# Словарь для хранения данных пользователей
user_data = {}
EMAIL_ADDRESS = ""  # Замените на ваш email
PASSWORD = ""  # Замените на ваш пароль от email

# Функция для отправки email
def send_email(subject, body, to_email):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)  # Используем SMTP сервер Gmail
        smtpObj.starttls()  # Шифруем соединение
        smtpObj.login(EMAIL_ADDRESS, PASSWORD)  # Авторизуемся на сервере
        smtpObj.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())  # Отправляем email
        smtpObj.quit()  # Закрываем соединение

        return True
    except Exception as e:
        print(f"Ошибка при отправке email: {e}")
        return False

# Функция для создания главного меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Трудоустройство/практика"))
    markup.add(KeyboardButton("Целевое обучение"))
    markup.add(KeyboardButton("Мероприятия"))
    markup.add(KeyboardButton("Другое"))
    return markup

# Функция для создания меню "Трудоустройство/практика"
def job_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Практическая подготовка"))
    markup.add(KeyboardButton("Летнее трудоустройство"))
    markup.add(KeyboardButton("Трудоустройство после обучения"))
    markup.add(KeyboardButton("Назад в меню"))
    return markup

# Функция для создания меню выбора канала связи
def contact_channel_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Телефон"))
    markup.add(KeyboardButton("WhatsApp"))
    markup.add(KeyboardButton("Telegram"))
    return markup

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Выберите нужный раздел:", reply_markup=main_menu())

# Обработчик для возврата в главное меню
@bot.message_handler(func=lambda message: message.text == "Назад в меню")
def back_to_main(message):
    bot.send_message(message.chat.id, "Вы вернулись в главное меню:", reply_markup=main_menu())

# Обработчик для раздела "Трудоустройство/практика"
@bot.message_handler(func=lambda message: message.text == "Трудоустройство/практика")
def employment_practice(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=job_menu())

# Обработчик для пункта "Практическая подготовка"
@bot.message_handler(func=lambda message: message.text == "Практическая подготовка")
def start_form(message):
    user_data[message.chat.id] = {"step": "full_name"}  # Инициализация данных пользователя
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")

# Обработчик для получения Ф.И.О
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name")
def get_full_name(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")

# Обработчик для получения даты рождения
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date")
def get_birth_date(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "education"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")

# Обработчик для получения места обучения
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "education")
def get_education(message):
    user_data[message.chat.id]["education"] = message.text
    user_data[message.chat.id]["step"] = "profession"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")

# Обработчик для получения профессии/специальности
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "profession")
def get_profession(message):
    user_data[message.chat.id]["profession"] = message.text
    user_data[message.chat.id]["step"] = "course"
    bot.send_message(message.chat.id, "Какой курс?")

# Обработчик для получения курса
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "course")
def get_course(message):
    user_data[message.chat.id]["course"] = message.text
    user_data[message.chat.id]["step"] = "practice_duration"
    bot.send_message(message.chat.id, "Сроки практики?")

# Обработчик для получения сроков практики
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "practice_duration")
def get_practice_duration(message):
    user_data[message.chat.id]["practice_duration"] = message.text
    user_data[message.chat.id]["step"] = "previous_practice"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")

# Обработчик для получения информации о предыдущей практике
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "previous_practice")
def get_previous_practice(message):
    user_data[message.chat.id]["previous_practice"] = message.text
    user_data[message.chat.id]["step"] = "same_department"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")

# Обработчик для получения ответа о желании пройти практику в том же подразделении
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "same_department")
def get_same_department(message):
    user_data[message.chat.id]["same_department"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

# Обработчик для получения предпочтительного канала связи
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel")
def get_contact_channel(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")

# Обработчик для получения номера телефона
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number")
def get_phone_number(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    # Формируем текст анкеты
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key != "step"])

    # Отправляем пользователю анкету для подтверждения
    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.")

# Обработчик для подтверждения отправки анкеты
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
        bot.send_message(message.chat.id, "Спасибо, что предоставили необходимую информацию о себе, наши специалисты\nобязательно рассмотрят Вашу заявку и вернутся к Вам с конкретным предложением.\nНа данном этапе Вы также ознакомиться с памяткой.", reply_markup=main_menu())
        with open("Памятка_для_будущих_абитуриентов.pdf",'rb') as file:
            bot.send_document(message.chat.id, file)  # Отправляем памятку
        del user_data[message.chat.id]  # Удаляем данные пользователя после отправки
    elif message.text.lower() == "редактировать":
        user_data[message.chat.id]["step"] = "full_name"
        bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.")

# Запуск бота
bot.polling(none_stop=True)