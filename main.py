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

# Функция для создания меню "Другое"
def another_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Задайте свой вопрос"))
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

#меню для целевого обучения для получения памятки, стипендии и др. вопроса
def alr_studying_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Получить памятку студента целевого обучения"))
    markup.add(KeyboardButton("Узнать, когда придет стипендия"))
    markup.add(KeyboardButton("Задать другой вопрос"))
    return markup



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Текст-заглушка, потом тут будет приветствие:", reply_markup=main_menu())


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
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "SUZ another question"}


#меню ветки другое
@bot.message_handler(func=lambda message: message.text == "Другое")
def ask_question_other(message):
    bot.send_message(message.chat.id, "Задайте свой вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id] = {"step": "Вопрос", "form_type": "Another Question"}

#начало другого вопроса
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Вопрос" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_another_quest_suz(message):
    user_data[message.chat.id]["Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id,{}).get("form_type") == "Another Question")
def get_name_another_quest(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id,{}).get("form_type") == "Another Question")
def get_name_another_quest_suz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_contact_channel_suz(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_phone_number_suz(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())
 #конец другого вопроса

#меню для выбора, обучается ли уже пользователь в СУЗе или только хочет поступить
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в СУЗе")
def targeted_training_suz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_suz_menu())


#суз уже идет обучение
@bot.message_handler(func=lambda message: message.text == "Я уже обучаюсь по договору целевого обучения в СУЗе")
def alr_studying_suz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=alr_studying_menu())
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "SUZ another question"}


#выдача памятки по СУЗу
@bot.message_handler(func=lambda message: message.text == "Получить памятку студента целевого обучения" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_memo_suz(message):
    bot.send_message(message.chat.id, "Вот ваша памятка:", reply_markup=back_to_main_menu())
    with open("Буклет СУЗ.pdf", 'rb') as file:
        bot.send_document(message.chat.id, file)


#анкета другого вопроса
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def start_another_quest_suz(message):
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id]["step"] = "question"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "question" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_another_quest_suz(message):
    user_data[message.chat.id]["Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_name_another_quest_suz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_contact_channel_suz(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_phone_number_suz(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())
#конец анкеты СУЗа


# Анкета для целевого обучения в сузе начинается отсюда
@bot.message_handler(func=lambda message: message.text == "Я хочу подписать договор на целевое обучение в СУЗ")
def start_suz_form(message):
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "SUZ"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_full_name_suz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_full_name_suz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Город"
    bot.send_message(message.chat.id, "В каком городе проживаете?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Город" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_city_suz(message):
    user_data[message.chat.id]["Город"] = message.text
    user_data[message.chat.id]["step"] = "СУЗ"
    bot.send_message(message.chat.id, "В каком СУЗе обучаетесь?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "СУЗ" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_suz_suz(message):
    user_data[message.chat.id]["СУЗ"] = message.text
    user_data[message.chat.id]["step"] = "Направление подготовки"
    bot.send_message(message.chat.id, "Какое направление подготовки?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Направление подготовки" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_dir_of_train_suz(message):
    user_data[message.chat.id]["Направление подготовки"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_contact_channel_suz(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_phone_number_suz(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())
#конец анкеты СУЗа

# Анкета для "Целевое обучение в ВУЗе"
# entrance - поступление
#меню для выбора, обучается ли уже пользователь в ВУЗе или хочет поступить
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в ВУЗе")
def targeted_training_vuz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_vuz_menu())

@bot.message_handler(func=lambda message: message.text == "Я хочу поступить на целевое обучение в ВУЗ")
def start_entrance_vuz_form(message):
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "entrance_vuz"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_full_name_entrance_vuz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_birth_date_entrance_vuz(message):
    user_data[message.chat.id]["Дата рождения"] = message.text
    user_data[message.chat.id]["step"] = "Город"
    bot.send_message(message.chat.id, "В каком городе проживаете?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Город" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_city_entrance_vuz(message):
    user_data[message.chat.id]["Город"] = message.text
    user_data[message.chat.id]["step"] = "Результаты ЕГЭ/вступительных испытаний"
    bot.send_message(message.chat.id, "Результаты ЕГЭ/Результаты вступительных испытаний:")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Результаты ЕГЭ/вступительных испытаний" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_result_entrance_vuz(message):
    user_data[message.chat.id]["Результаты ЕГЭ/вступительных испытаний"] = message.text
    user_data[message.chat.id]["step"] = "Варианты ВУЗов"
    bot.send_message(message.chat.id, "Какой ВУЗ рассматриваете?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Варианты ВУЗов" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_variants_entrance_vuz(message):
    user_data[message.chat.id]["Варианты ВУЗов"] = message.text
    user_data[message.chat.id]["step"] = "Направление"
    bot.send_message(message.chat.id, "Какое направление подготовки Вас интересует?")

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Направление" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_direction_entrance_vuz(message):
    user_data[message.chat.id]["Направление"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_contact_channel_entrance_vuz(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_phone_number_entrance_vuz(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

#я уже обучаюсь по договору цо в ВУЗе
@bot.message_handler(func=lambda message: message.text == "Я уже обучаюсь по договору целевого обучения в ВУЗе")
def alr_studying_vuz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=alr_studying_menu())
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "VUZ another question"}


#выдача памятки по ВУЗу
@bot.message_handler(func=lambda message: message.text == "Получить памятку студента целевого обучения" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_memo_vuz(message):
    bot.send_message(message.chat.id, "Вот ваша памятка:", reply_markup=back_to_main_menu())
    with open("Буклет ВУЗ.pdf", 'rb') as file:
        bot.send_document(message.chat.id, file)

#задать другой вопрос
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def start_another_quest_vuz(message):
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id]["step"] = "question"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "question" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_another_quest_vuz(message):
    user_data[message.chat.id]["Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_name_another_quest_vuz(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_contact_channel_vuz(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_phone_number_vuz(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Анкета для "Практическая подготовка"
@bot.message_handler(func=lambda message: message.text == "Практическая подготовка")
def start_practice_form(message):
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "practice"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_full_name_practice(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_birth_date_practice(message):
    user_data[message.chat.id]["Дата рождения"] = message.text
    user_data[message.chat.id]["step"] = "Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_education_practice(message):
    user_data[message.chat.id]["Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_profession_practice(message):
    user_data[message.chat.id]["Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Курс" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_course_practice(message):
    user_data[message.chat.id]["Курс"] = message.text
    user_data[message.chat.id]["step"] = "Сроки практики"
    bot.send_message(message.chat.id, "Сроки практики?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Сроки практики" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_practice_duration_practice(message):
    user_data[message.chat.id]["Сроки практики"] = message.text
    user_data[message.chat.id]["step"] = "Прошлая практика"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Прошлая практика" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_previous_practice_practice(message):
    user_data[message.chat.id]["Прошлая практика"] = message.text
    user_data[message.chat.id]["step"] = "Желание пройти практику в том же подразделении"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Желание пройти практику в том же подразделении" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_same_department_practice(message):
    user_data[message.chat.id]["Желание пройти практику в том же подразделении"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_contact_channel_practice(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_phone_number_practice(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


# Анкета для "Летнее трудоустройство"
@bot.message_handler(func=lambda message: message.text == "Летнее трудоустройство")
def start_summer_employment_form(message):
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "summer_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_full_name_summer(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_birth_date_summer(message):
    user_data[message.chat.id]["Дата рождения"] = message.text
    user_data[message.chat.id]["step"] = "Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_education_summer(message):
    user_data[message.chat.id]["Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_profession_summer(message):
    user_data[message.chat.id]["Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Курс" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_course_summer(message):
    user_data[message.chat.id]["Курс"] = message.text
    user_data[message.chat.id]["step"] = "Период трудоустройства"
    bot.send_message(message.chat.id, "На какой период рассматриваете трудоустройство?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Период трудоустройства" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_employment_period_summer(message):
    user_data[message.chat.id]["Период трудоустройства"] = message.text
    user_data[message.chat.id]["step"] = "Опыт работы"
    bot.send_message(message.chat.id, "Работали ли Вы ранее, если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Опыт работы" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_previous_work_summer(message):
    user_data[message.chat.id]["Опыт работы"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_contact_channel_summer(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_phone_number_summer(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
    user_data[message.chat.id]["step"] = "confirm_send"

    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if key not in ["step", "form_type"]])

    bot.send_message(message.chat.id,
                     f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


# Анкета для "Трудоустройство после обучения"
@bot.message_handler(func=lambda message: message.text == "Трудоустройство после обучения")
def start_post_study_employment_form(message):
    user_data[message.chat.id] = {"step": "Ф.И.О", "form_type": "post_study_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_full_name_post_study(message):
    user_data[message.chat.id]["Ф.И.О"] = message.text
    user_data[message.chat.id]["step"] = "Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_birth_date_post_study(message):
    user_data[message.chat.id]["Дата рождения"] = message.text
    user_data[message.chat.id]["step"] = "Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_education_post_study(message):
    user_data[message.chat.id]["Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_profession_post_study(message):
    user_data[message.chat.id]["Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Курс" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_course_post_study(message):
    user_data[message.chat.id]["Курс"] = message.text
    user_data[message.chat.id]["step"] = "Сроки практики"
    bot.send_message(message.chat.id, "Сроки практики?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Сроки практики" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_practice_duration_post_study(message):
    user_data[message.chat.id]["Сроки практики"] = message.text
    user_data[message.chat.id]["step"] = "Прошлая практика"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Прошлая практика" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_previous_practice_post_study(message):
    user_data[message.chat.id]["Прошлая практика"] = message.text
    user_data[message.chat.id]["step"] = "Желание пройти практику в том же подразделении"
    bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Желание пройти практику в том же подразделении" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_same_department_post_study(message):
    user_data[message.chat.id]["Желание пройти практику в том же подразделении"] = message.text
    user_data[message.chat.id]["step"] = "Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_contact_channel_post_study(message):
    user_data[message.chat.id]["Канал связи"] = message.text
    user_data[message.chat.id]["step"] = "Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_phone_number_post_study(message):
    user_data[message.chat.id]["Номер телефона"] = message.text
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
        subject = f"Новая анкета для {'практики' if form_type == 'practice' else 'летнего трудоустройства' if form_type == 'summer_employment' else 'трудоустройства после обучения' if form_type == 'post_study_employment' else 'поступления на целевое обучение в ВУЗ' if form_type == 'entrance_vuz' else 'обучается по договору целевого обучения в ВУЗе' if form_type =='VUZ another question' else 'СУЗа'}"
        to_email = EMAIL_ADDRESS
        if send_email(subject, application_text, to_email):
            bot.send_message(message.chat.id, "Анкета успешно отправлена по электронной почте.")
        else:
            bot.send_message(message.chat.id, "Ошибка при отправке анкеты по электронной почте.")
        bot.send_message(message.chat.id, f"Анкета отправлена:\n\n{application_text}")
        bot.send_message(message.chat.id, "Спасибо, что предоставили необходимую информацию о себе, наши специалисты обязательно рассмотрят Вашу заявку и вернутся к Вам с конкретным ответом.", reply_markup=main_menu())
        if form_type == "practice" or form_type == "summer_employment" or form_type == "post_study_employment":
            bot.send_message(message.chat.id,"На данном этапе вы можете ознакомиться с памяткой", reply_markup=main_menu())
            with open("Памятка_для_будущих_абитуриентов.pdf", 'rb') as file:
                bot.send_document(message.chat.id, file)
        del user_data[message.chat.id]
    elif message.text.lower() == "редактировать":
        user_data[message.chat.id]["step"] = "Ф.И.О"
        bot.send_message(message.chat.id, "Введите ваше Ф.И.О:")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())


bot.polling(none_stop=True)