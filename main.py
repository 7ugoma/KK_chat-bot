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

# Функция для создания меню "Целевое обучение"
def education_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Целевое обучение в ВУЗе"))
    markup.add(KeyboardButton("Целевое обучение в СУЗе"))
    markup.add(KeyboardButton("Назад в меню"))
    return markup

# Функция для создания меню "Целевое обучение в ВУЗе "
def education_vuz_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Я хочу поступить на целевое обучение в ВУЗ"))
    markup.add(KeyboardButton("Я уже обучаюсь по договору целевого обучения в ВУЗе"))
    markup.add(KeyboardButton("Назад в меню"))
    return markup

# Функция для создания меню "Целевое обучение в СУЗе "
def education_suz_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Я хочу подписать договор на целевое обучение в СУЗ"))
    markup.add(KeyboardButton("Я уже обучаюсь по договору целевого обучения в СУЗе"))
    markup.add(KeyboardButton("Назад в меню"))
    return markup

# функция для возврата в главное меню из анкеты
def back_to_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Назад в меню"))
    return markup


def contact_channel_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Телефон"))
    markup.add(KeyboardButton("WhatsApp"))
    markup.add(KeyboardButton("Telegram"))
    return markup


def confirm_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Отправить"))
    markup.add(KeyboardButton("Редактировать"))
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

#менюшка для выбора СУЗа или ВУЗа
@bot.message_handler(func=lambda message: message.text == "Целевое обучение")
def targeted_training(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_menu())

#меню для выбора, обучается ли уже пользователь в СУЗе или только хочет поступить
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в СУЗе")
def targeted_training_suz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_suz_menu())

# Анкета для целевого обучения в сузе начинается отсюда
@bot.message_handler(func=lambda message: message.text == "Я хочу подписать договор на целевое обучение в СУЗ")
def start_suz_form(message):
    user_data[message.chat.id] = {"step": "full_name", "form_type": "SUZ"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_full_name_suz(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_full_name_suz(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "city"
    bot.send_message(message.chat.id, "В каком городе проживаете?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "city" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_city_suz(message):
    user_data[message.chat.id]["city"] = message.text
    user_data[message.chat.id]["step"] = "SUZ"
    bot.send_message(message.chat.id, "В каком СУЗе обучаетесь?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "SUZ" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_suz_suz(message):
    user_data[message.chat.id]["SUZ"] = message.text
    user_data[message.chat.id]["step"] = "direction_of_training"
    bot.send_message(message.chat.id, "Какое направление подготовки?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "direction_of_training" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_dir_of_train_suz(message):
    user_data[message.chat.id]["direction_of_training"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_contact_channel_suz(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_phone_number_suz(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())
#конец анкеты СУЗа

# Анкета для "Практическая подготовка"
@bot.message_handler(func=lambda message: message.text == "Практическая подготовка")
def start_practice_form(message):
    user_data[message.chat.id] = {"step": "full_name", "form_type": "practice"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_full_name_practice(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_birth_date_practice(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "education"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "education" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_education_practice(message):
    user_data[message.chat.id]["education"] = message.text
    user_data[message.chat.id]["step"] = "profession"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "profession" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_profession_practice(message):
    user_data[message.chat.id]["profession"] = message.text
    user_data[message.chat.id]["step"] = "course"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "course" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_course_practice(message):
    user_data[message.chat.id]["course"] = message.text
    user_data[message.chat.id]["step"] = "practice_duration"
    bot.send_message(message.chat.id, "Сроки практики?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "practice_duration" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_practice_duration_practice(message):
    user_data[message.chat.id]["practice_duration"] = message.text
    user_data[message.chat.id]["step"] = "previous_practice"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "previous_practice" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_previous_practice_practice(message):
    user_data[message.chat.id]["previous_practice"] = message.text
    user_data[message.chat.id]["step"] = "same_department"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "same_department" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_same_department_practice(message):
    user_data[message.chat.id]["same_department"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_contact_channel_practice(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_phone_number_practice(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


# Анкета для "Летнее трудоустройство"
@bot.message_handler(func=lambda message: message.text == "Летнее трудоустройство")
def start_summer_employment_form(message):
    user_data[message.chat.id] = {"step": "full_name", "form_type": "summer_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_full_name_summer(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_birth_date_summer(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "education"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "education" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_education_summer(message):
    user_data[message.chat.id]["education"] = message.text
    user_data[message.chat.id]["step"] = "profession"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "profession" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_profession_summer(message):
    user_data[message.chat.id]["profession"] = message.text
    user_data[message.chat.id]["step"] = "course"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "course" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_course_summer(message):
    user_data[message.chat.id]["course"] = message.text
    user_data[message.chat.id]["step"] = "employment_period"
    bot.send_message(message.chat.id, "На какой период рассматриваете трудоустройство?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "employment_period" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_employment_period_summer(message):
    user_data[message.chat.id]["employment_period"] = message.text
    user_data[message.chat.id]["step"] = "previous_work"
    bot.send_message(message.chat.id, "Работали ли Вы ранее, если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "previous_work" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_previous_work_summer(message):
    user_data[message.chat.id]["previous_work"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_contact_channel_summer(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_phone_number_summer(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


# Анкета для "Трудоустройство после обучения"
@bot.message_handler(func=lambda message: message.text == "Трудоустройство после обучения")
def start_post_study_employment_form(message):
    user_data[message.chat.id] = {"step": "full_name", "form_type": "post_study_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_full_name_post_study(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_birth_date_post_study(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "education"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "education" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_education_post_study(message):
    user_data[message.chat.id]["education"] = message.text
    user_data[message.chat.id]["step"] = "profession"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "profession" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_profession_post_study(message):
    user_data[message.chat.id]["profession"] = message.text
    user_data[message.chat.id]["step"] = "course"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "course" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_course_post_study(message):
    user_data[message.chat.id]["course"] = message.text
    user_data[message.chat.id]["step"] = "practice_duration"
    bot.send_message(message.chat.id, "Сроки практики?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "practice_duration" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_practice_duration_post_study(message):
    user_data[message.chat.id]["practice_duration"] = message.text
    user_data[message.chat.id]["step"] = "previous_practice"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "previous_practice" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_previous_practice_post_study(message):
    user_data[message.chat.id]["previous_practice"] = message.text
    user_data[message.chat.id]["step"] = "same_department"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "same_department" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_same_department_post_study(message):
    user_data[message.chat.id]["same_department"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_contact_channel_post_study(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_phone_number_post_study(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Анкета для "Целевое обучение в ВУЗе" - я хочу поступить на целевое обучение в ВУЗ
# entrance - поступление
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в ВУЗе")
def start_entrance_vuz_form(message):
    user_data[message.chat.id] = {"step": "full_name", "form_type": "entrance_vuz"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "full_name" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_full_name_entrance_vuz(message):
    user_data[message.chat.id]["full_name"] = message.text
    user_data[message.chat.id]["step"] = "birth_date"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "birth_date" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_birth_date_entrance_vuz(message):
    user_data[message.chat.id]["birth_date"] = message.text
    user_data[message.chat.id]["step"] = "city"
    bot.send_message(message.chat.id, "В каком городе проживаете?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "city" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_city_entrance_vuz(message):
    user_data[message.chat.id]["city"] = message.text
    user_data[message.chat.id]["step"] = "result"
    bot.send_message(message.chat.id, "Результаты ЕГЭ/Результаты вступительных испытаний:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "result" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_result_entrance_vuz(message):
    user_data[message.chat.id]["result"] = message.text
    user_data[message.chat.id]["step"] = "variants"
    bot.send_message(message.chat.id, "Какой ВУЗ рассматриваете?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "variants" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_variants_entrance_vuz(message):
    user_data[message.chat.id]["variants"] = message.text
    user_data[message.chat.id]["step"] = "direction"
    bot.send_message(message.chat.id, "Какое направление подготовки Вас интересует?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "direction" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_direction_entrance_vuz(message):
    user_data[message.chat.id]["direction"] = message.text
    user_data[message.chat.id]["step"] = "contact_channel"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "contact_channel" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_contact_channel_entrance_vuz(message):
    user_data[message.chat.id]["contact_channel"] = message.text
    user_data[message.chat.id]["step"] = "phone_number"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "phone_number" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_phone_number_entrance_vuz(message):
    user_data[message.chat.id]["phone_number"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Общий обработчик для подтверждения отправки
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "confirm_send")
def confirm_send(message):
    if message.text.lower() == "отправить":
        application_text = "\n".join(
            [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])
        form_type = user_data[message.chat.id].get("form_type")
        subject = f"Новая анкета для {'практики' if form_type == 'practice' else 'летнего трудоустройства' if form_type == 'summer_employment' else 'трудоустройства после обучения'}"
        to_email = EMAIL_ADDRESS
        if send_email(subject, application_text, to_email):
            bot.send_message(message.chat.id, "Анкета успешно отправлена по электронной почте.")
        else:
            bot.send_message(message.chat.id, "Ошибка при отправке анкеты по электронной почте.")
        bot.send_message(message.chat.id, f"Анкета отправлена:\n\n{application_text}")
        bot.send_message(message.chat.id, "Спасибо, что предоставили необходимую информацию о себе, наши специалисты\nобязательно рассмотрят Вашу заявку и вернутся к Вам с конкретным предложением.\nНа данном этапе Вы также можете ознакомиться с памяткой.", reply_markup=main_menu())
        with open("Памятка_для_будущих_абитуриентов.pdf", 'rb') as file:
            bot.send_document(message.chat.id, file)
        del user_data[message.chat.id]
    elif message.text.lower() == "редактировать":
        user_data[message.chat.id]["step"] = "full_name"
        bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


bot.polling(none_stop=True)