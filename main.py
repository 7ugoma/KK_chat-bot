import telebot
import pandas as pd
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email
import email.mime.application
import re
import phonenumbers
import os
from datetime import datetime

TOKEN = '7983356108:AAGiBAXrAHyk4RMSxE_d1QqGZMfUyN21lWg'
bot = telebot.TeleBot(TOKEN)

user_data = {}
admin_data = {}
EMAIL_ADDRESS = "sustown82@gmail.com"
PASSWORD = "iyxa rgwu ziwu yzoi"

ADMIN_CREDENTIALS = {
    "login": "admin",
    "password": "admin123"
}

QUESTION_TYPES = [
    "VUZ another question",
    "SUZ another question",
    "Another Question"
]

# функция отправки через почту
def send_email(subject, body, to_email, filename=''):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = to_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))
        if len(filename) != 0:
            fp = open(filename, 'rb')
            att = email.mime.application.MIMEApplication(fp.read(), _subtype="xlsx")
            fp.close()
            att.add_header('Content-Disposition', 'attachment', filename=filename)
            msg.attach(att)

        smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
        smtpObj.starttls()
        smtpObj.login(EMAIL_ADDRESS, PASSWORD)
        smtpObj.sendmail(EMAIL_ADDRESS, to_email, msg.as_string())
        smtpObj.quit()

        return True
    except Exception as e:
        print(f"❌ Ошибка при отправке email: {e}")
        return False


FORM_FILES = {
    "practice": "practice_forms.xlsx",
    "summer_employment": "summer_employment_forms.xlsx",
    "post_study_employment": "post_study_employment_forms.xlsx",
    "entrance_vuz": "entrance_vuz_forms.xlsx",
    "SUZ": "suz_forms.xlsx"
}


def init_form_file(form_type):
    if not os.path.exists(FORM_FILES[form_type]):
        df = pd.DataFrame()
        df.to_excel(FORM_FILES[form_type], index=False)


# сохранение файлов в таблицу Excel
def save_form_to_excel(form_data, form_type):
    """Сохраняет анкету в Excel (только для анкет, не вопросов)"""
    if form_type not in FORM_FILES:
        return False

    try:
        # Создаем копию данных, чтобы не изменять оригинал
        form_data_copy = form_data.copy()

        # Добавляем дату заполнения в правильном формате
        form_data_copy['Дата заполнения'] = datetime.now().strftime('%d.%m.%Y %H:%M')

        # Создаем DataFrame из данных анкеты
        form_df = pd.DataFrame([form_data_copy])

        # Если файл существует, загружаем его и добавляем новую запись
        if os.path.exists(FORM_FILES[form_type]):
            existing_df = pd.read_excel(FORM_FILES[form_type])
            updated_df = pd.concat([existing_df, form_df], ignore_index=True)
        else:
            updated_df = form_df

        # Сохраняем обновленный DataFrame
        updated_df.to_excel(FORM_FILES[form_type], index=False)
        return True
    except Exception as e:
        print(f"Ошибка при сохранении анкеты: {e}")
        return False



# блок с созданием менюшек с кнопками
# главное меню
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("💼 Трудоустройство/практика"))
    markup.add(KeyboardButton("🎓 Целевое обучение"))
    markup.add(KeyboardButton("🗓 Мероприятия"))
    markup.add(KeyboardButton("💬 Задать свой вопрос"))
    markup.add(KeyboardButton("""ℹ️ Информация об АО ‹Концерн ‹Калашников»"""))
    return markup


# функция для создание меню внутри трудоустройства/практики
def job_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("💪 Практическая подготовка"))
    markup.add(KeyboardButton("☀️ Летнее трудоустройство"))
    markup.add(KeyboardButton("👨🏼‍🎓 Трудоустройство после обучения"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


# Функция для создания меню "Целевое обучение"
def education_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Целевое обучение в ВУЗе"))
    markup.add(KeyboardButton("Целевое обучение в СУЗе"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


# Функция для создания меню "Целевое обучение в ВУЗе "
def education_vuz_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Я хочу поступить на целевое обучение в ВУЗ"))
    markup.add(KeyboardButton("Я уже обучаюсь по договору целевого обучения в ВУЗе"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


# Функция для создания меню "Целевое обучение в СУЗе "
def education_suz_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Я хочу подписать договор на целевое обучение в СУЗ"))
    markup.add(KeyboardButton("Я уже обучаюсь по договору целевого обучения в СУЗе"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup



# меню для целевого обучения для получения памятки, стипендии и др. вопроса
def alr_studying_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("📜 Получить памятку студента целевого обучения"))
    markup.add(KeyboardButton("💰 Узнать сумму стипендии"))
    markup.add(KeyboardButton("❓ Задать другой вопрос"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


# Функция для создания меню "Другое"
def another_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("❓ Задайте свой вопрос"))
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


def contact_channel_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Телефон"))
    markup.add(KeyboardButton("WhatsApp"))
    markup.add(KeyboardButton("Telegram"))
    return markup


def simple_question():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Да"))
    markup.add(KeyboardButton("Нет"))
    return markup



def confirm_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("📩 Отправить"))
    markup.add(KeyboardButton("✏️ Редактировать"))
    return markup


# функция для возврата в главное меню из анкеты
def back_to_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("🔙 Назад в меню"))
    return markup


def admin_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("⬆️ Загрузить таблицу со стипендиями"))
    markup.add(KeyboardButton("⬇️ Скачать таблицу со стипендиями"))
    markup.add(KeyboardButton("📤 Загрузить таблицу мероприятий"))
    markup.add(KeyboardButton("📥 Скачать таблицу мероприятий"))
    markup.add(KeyboardButton("📊 Скачать анкеты"))
    markup.add(KeyboardButton("🔙 Выйти из админ-панели"))
    return markup

def admin_forms_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("💪 Анкеты практической подготовки"))
    markup.add(KeyboardButton("☀️ Анкеты летнего трудоустройства"))
    markup.add(KeyboardButton("👨🏼‍🎓 Анкеты трудоустройства после обучения"))
    markup.add(KeyboardButton("🎓 Анкеты целевого обучения в ВУЗ"))
    markup.add(KeyboardButton("🏫 Анкеты целевого обучения в СУЗ"))
    markup.add(KeyboardButton("🔙 Назад в админ-меню"))
    return markup
# конец блока с менюшками



# блок со скачиванием заполненный таблиц с заполненными анкетами
@bot.message_handler(func=lambda message: message.text == "📊 Скачать анкеты" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_forms_menu(message):
    bot.send_message(message.chat.id, "Выберите тип анкет для скачивания:", reply_markup=admin_forms_menu())


@bot.message_handler(func=lambda message: message.text == "💪 Анкеты практической подготовки" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_practice_forms(message):
    try:
        if os.path.exists(FORM_FILES["practice"]):
            with open(FORM_FILES["practice"], 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_forms_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл анкет не найден", reply_markup=admin_forms_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_forms_menu())


@bot.message_handler(func=lambda message: message.text == "☀️ Анкеты летнего трудоустройства" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_summer_forms(message):
    try:
        if os.path.exists(FORM_FILES["summer_employment"]):
            with open(FORM_FILES["summer_employment"], 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_forms_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл анкет не найден", reply_markup=admin_forms_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_forms_menu())


@bot.message_handler(func=lambda message: message.text == "👨🏼‍🎓 Анкеты трудоустройства после обучения" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_post_study_forms(message):
    try:
        if os.path.exists(FORM_FILES["post_study_employment"]):
            with open(FORM_FILES["post_study_employment"], 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_forms_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл анкет не найден", reply_markup=admin_forms_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_forms_menu())

@bot.message_handler(func=lambda message: message.text == "🎓 Анкеты целевого обучения в ВУЗ" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_vuz_forms(message):
    try:
        if os.path.exists(FORM_FILES["entrance_vuz"]):
            with open(FORM_FILES["entrance_vuz"], 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_forms_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл анкет не найден", reply_markup=admin_forms_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_forms_menu())

@bot.message_handler(func=lambda message: message.text == "🏫 Анкеты целевого обучения в СУЗ" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_suz_forms(message):
    try:
        if os.path.exists(FORM_FILES["SUZ"]):
            with open(FORM_FILES["SUZ"], 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_forms_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл анкет не найден", reply_markup=admin_forms_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_forms_menu())
# конец блока со скачиванием таблиц

# возврат в админ меню
@bot.message_handler(func=lambda message: message.text == "🔙 Назад в админ-меню" and message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def back_to_admin_menu(message):
    bot.send_message(message.chat.id, "Вы вернулись в админ-меню:", reply_markup=admin_menu())



# начало блока функций для проверок корректности ввода данных в анкетах
# проверка корректности ввода даты рождения
def check_contact_channel(channel):
    if str(channel).lower() in ["телефон", "whatsapp", "telegram"]:
        return True

    else:
        return False


# проверка правильности ввода простого вопроса
def check_simple_question(answer):
    if str(answer).lower() in ["да", 'нет']:
        return True

    else:
        return False


# Регулярное выражение для формата ДД.ММ.ГГГГ
def check_dates(birthdate):
    pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d-(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$"

    if re.match(pattern, birthdate):  # Проверка соответствия регулярному выражению
        return True

    else:
        return False


# Регулярное выражение для формата ДД.ММ.ГГГГ
def check_birthdate(birthdate):
    pattern = r"^(0[1-9]|[12][0-9]|3[01])\.(0[1-9]|1[0-2])\.(19|20)\d\d$"
    if re.match(pattern, birthdate):  # Проверка соответствия регулярному выражению
        return True

    else:
        return False


# проверка телефонного номера
def check_phone_number(phone_number):
    try:
        phone_number = phonenumbers.parse(phone_number)
        return phonenumbers.is_possible_number(phone_number)
    except:
        return False


# проверка имени
def check_full_name(fio):
    pattern = r"^[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+$"  # регулярное выражение формата Иванов Иван Иванович
    if re.match(pattern, fio):  # сравнение строки с регулярным выражением
        return True

    else:
        return False
# конец блока с регулярными выражениями




# сам старт бота
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
                     "Привет!👋 Это виртуальный помощник от АО «Концерн Калашников» . Задайте свой вопрос или выберете один из предложенных вариантов.\n\nЧтобы вернуться в начало или запустить чат-бот заново, напишите\n/start",
                     reply_markup=main_menu())


# отправка по нажатию кнопки информации о КК
@bot.message_handler(func=lambda message: message.text == """ℹ️ Информация об АО ‹Концерн ‹Калашников»""")
def admin_login_start(message):
    with open("KK.jpg", 'rb') as file:
        bot.send_photo(message.chat.id, file)
    bot.send_message(message.chat.id, """Акционерное общество "Концерн "Калашников" - это ведущее оборонное предприятие в сфере разработки стрелкового вооружения, спецтехники, станков и производства беспилотников.Мы уделяем особое внимание привлечению и закреплению перспективных студентов на предприятия""")

# обработчик команды /admin
@bot.message_handler(commands=['admin'])
def admin_login_start(message):
    msg = bot.send_message(message.chat.id, "Введите логин:")
    bot.register_next_step_handler(msg, admin_login_check)


# прием ввода админского логина и пароля
def admin_login_check(message):
    login = message.text
    admin_data[message.chat.id] = {"login": login}
    msg = bot.send_message(message.chat.id, "Введите пароль:")
    bot.register_next_step_handler(msg, admin_password_check)


# проверка правильности ввода данных логина и пароля
def admin_password_check(message):
    password = message.text
    login = admin_data[message.chat.id]["login"]

    if login == ADMIN_CREDENTIALS["login"] and password == ADMIN_CREDENTIALS["password"]:
        bot.send_message(message.chat.id, "✅ Авторизация успешна!", reply_markup=admin_menu())
        admin_data[message.chat.id]["authenticated"] = True
    else:
        bot.send_message(message.chat.id, "❌ Неверный логин или пароль", reply_markup=main_menu())
        if message.chat.id in admin_data:
            del admin_data[message.chat.id]


# функция для выхода из меню админа
@bot.message_handler(func=lambda message: message.text == "🔙 Выйти из админ-панели")
def admin_logout(message):
    if message.chat.id in admin_data:
        del admin_data[message.chat.id]
    bot.send_message(message.chat.id, "Вы вышли из админ-панели", reply_markup=main_menu())


# обработчик команды по замене таблицы со степендиями
@bot.message_handler(func=lambda message: message.text == "⬆️ Загрузить таблицу со стипендиями" and
                                          message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def request_upload_file_grants(message):
    msg = bot.send_message(message.chat.id, "Отправьте файл Excel со стипендиями (стипендия.xlsx):")
    bot.register_next_step_handler(msg, handle_upload_file_grants)


# сам загрузчик и обработчик другой таблицы со стипендиями
def handle_upload_file_grants(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем файл
            with open("стипендия.xlsx", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, "✅ Таблица стипендий успешно обновлена!", reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "❌ Пожалуйста, отправьте файл", reply_markup=admin_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при загрузке файла: {str(e)}", reply_markup=admin_menu())


# отправка пользователю таблицы со стипендиями
@bot.message_handler(func=lambda message: message.text == "⬇️ Скачать таблицу со стипендиями" and
                                          message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def download_grants_file(message):
    try:
        if os.path.exists("стипендия.xlsx"):
            with open("стипендия.xlsx", 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл стипендий не найден", reply_markup=admin_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_menu())


# обработчик команды по смене таблицы
@bot.message_handler(func=lambda message: message.text == "📤 Загрузить таблицу мероприятий" and
                                          message.chat.id in admin_data and admin_data[message.chat.id].get("authenticated", False))
def request_upload_file(message):
    msg = bot.send_message(message.chat.id, "Отправьте файл Excel с таблицей мероприятий (events.xlsx):")
    bot.register_next_step_handler(msg, handle_upload_file)


# обработчик самого файла с таблицей, чтобы заменить таблицу
def handle_upload_file(message):
    try:
        if message.document:
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем файл
            with open("events.xlsx", 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.send_message(message.chat.id, "✅ Таблица мероприятий успешно обновлена!", reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "❌ Пожалуйста, отправьте файл", reply_markup=admin_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при загрузке файла: {str(e)}", reply_markup=admin_menu())


# отправка админу таблицы с мероприятиями
@bot.message_handler(func=lambda message: message.text == "📥 Скачать таблицу мероприятий" and
                                          message.chat.id in admin_data and admin_data[message.chat.id].get(
    "authenticated", False))
def download_events_file(message):
    try:
        if os.path.exists("events.xlsx"):
            with open("events.xlsx", 'rb') as file:
                bot.send_document(message.chat.id, file, reply_markup=admin_menu())
        else:
            bot.send_message(message.chat.id, "❌ Файл мероприятий не найден", reply_markup=admin_menu())
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Ошибка при отправке файла: {str(e)}", reply_markup=admin_menu())


# возврат в главное меню
@bot.message_handler(func=lambda message: message.text == "🔙 Назад в меню")
def back_to_main(message):
    user_data[message.chat.id] = {"step": "", "form_type": ""}
    bot.send_message(message.chat.id, "Вы вернулись в главное меню:", reply_markup=main_menu())


# вход в ветку трудоустройства и практики
@bot.message_handler(func=lambda message: message.text == "💼 Трудоустройство/практика")
def employment_practice(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=job_menu())


# менюшка для выбора СУЗа или ВУЗа
@bot.message_handler(func=lambda message: message.text == "🎓 Целевое обучение")
def targeted_training(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_menu())
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "SUZ another question"}


# меню ветки другое
@bot.message_handler(func=lambda message: message.text == "💬 Задать свой вопрос")
def ask_question_other(message):
    bot.send_message(message.chat.id, "Задайте свой вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id] = {"step": "📝 Вопрос", "form_type": "Another Question"}


# начало другого вопроса


# записывает вопрос, спрашивает фио
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📝 Вопрос" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_another_quest_drugoe(message):
    user_data[message.chat.id]["📝 Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


# записывает имя, спрашивает канал связи и предлагает меню с выбором
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id,{}).get("form_type") == "Another Question")
def get_name_drugoe(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


# записывает канал связи, проверяет корректность его ввода, спрашивает номер телефона
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_contact_channel_drugoe(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона в формате +71234567890:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_phone_number_drugoe(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "Another Question")
def get_phone_number_drugoe(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

 #конец другого вопроса

# меню для выбора, обучается ли уже пользователь в СУЗе или только хочет поступить
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в СУЗе")
def targeted_training_suz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_suz_menu())


# суз уже идет обучение
@bot.message_handler(func=lambda message: message.text == "Я уже обучаюсь по договору целевого обучения в СУЗе")
def alr_studying_suz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=alr_studying_menu())
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "SUZ another question"}


# выдача памятки по СУЗу
@bot.message_handler(func=lambda message: message.text == "📜 Получить памятку студента целевого обучения" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_memo_suz(message):
    bot.send_message(message.chat.id, "Вот ваша памятка:", reply_markup=back_to_main_menu())
    with open("Буклет СУЗ.pdf", 'rb') as file:
        bot.send_document(message.chat.id, file)


# узнать, сколько будет стипендия
@bot.message_handler(func=lambda message: message.text == "💰 Узнать сумму стипендии" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_scholarship_summ_suz(message):
    bot.send_message(message.chat.id, "В файле находится актуальная информация по суммам стипендий:", reply_markup=back_to_main_menu())
    with open("стипендия.xlsx", 'rb') as file:
        bot.send_document(message.chat.id, file)


# анкета другого вопроса
@bot.message_handler(func=lambda message: message.text == "❓ Задать другой вопрос" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def start_another_quest_suz(message):
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id]["step"] = "question"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "question" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_another_quest_suz(message):
    user_data[message.chat.id]["📝 Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_name_another_quest_suz(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_contact_channel_another_suz(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_phone_number_another_suz(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ another question")
def get_agreement_another_suz(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

#конец анкеты СУЗа


# Анкета для целевого обучения в сузе начинается отсюда
@bot.message_handler(func=lambda message: message.text == "Я хочу подписать договор на целевое обучение в СУЗ")
def start_suz_form(message):
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "SUZ"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "ℹ️ Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_full_name_suz(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "📅 Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📅 Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_birthdate_suz(message):
    msg = message.text
    if check_birthdate(msg):
        user_data[message.chat.id]["📅 Дата рождения"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных дд.мм.гггг")
        return 0
    user_data[message.chat.id]["step"] = "🏙️ Город"
    bot.send_message(message.chat.id, "В каком городе проживаете?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🏙️ Город" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_city_suz(message):
    user_data[message.chat.id]["🏙️ Город"] = message.text
    user_data[message.chat.id]["step"] = "🏫 СУЗ"
    bot.send_message(message.chat.id, "В каком СУЗе обучаетесь?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🏫 СУЗ" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_suz_suz(message):
    user_data[message.chat.id]["🏫 СУЗ"] = message.text
    user_data[message.chat.id]["step"] = "🗂️ Направление подготовки"
    bot.send_message(message.chat.id, "Какое направление подготовки?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🗂️ Направление подготовки" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_dir_of_train_suz(message):
    user_data[message.chat.id]["🗂️ Направление подготовки"] = message.text
    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_contact_channel_suz(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_phone_number_suz(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "SUZ")
def get_agreement_suz(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())
#конец анкеты СУЗа

# Анкета для "Целевое обучение в ВУЗе"
# entrance - поступление
# меню для выбора, обучается ли уже пользователь в ВУЗе или хочет поступить
@bot.message_handler(func=lambda message: message.text == "Целевое обучение в ВУЗе")
def targeted_training_vuz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=education_vuz_menu())


@bot.message_handler(func=lambda message: message.text == "Я хочу поступить на целевое обучение в ВУЗ")
def start_entrance_vuz_form(message):
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "entrance_vuz"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "ℹ️ Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_full_name_entrance_vuz(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "📅 Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📅 Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_birth_date_entrance_vuz(message):
    msg = message.text
    if check_birthdate(msg):
        user_data[message.chat.id]["📅 Дата рождения"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных дд.мм.гггг")
        return 0
    user_data[message.chat.id]["step"] = "🏙️ Город"
    bot.send_message(message.chat.id, "В каком городе проживаете?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🏙️ Город" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_city_entrance_vuz(message):
    user_data[message.chat.id]["🏙️ Город"] = message.text
    user_data[message.chat.id]["step"] = "💯 Результаты ЕГЭ/вступительных испытаний"
    bot.send_message(message.chat.id, "Результаты ЕГЭ/Результаты вступительных испытаний:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "💯 Результаты ЕГЭ/вступительных испытаний" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_result_entrance_vuz(message):
    user_data[message.chat.id]["💯 Результаты ЕГЭ/вступительных испытаний"] = message.text
    user_data[message.chat.id]["step"] = "📊 Варианты ВУЗов"
    bot.send_message(message.chat.id, "Какой ВУЗ рассматриваете?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📊 Варианты ВУЗов" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_variants_entrance_vuz(message):
    user_data[message.chat.id]["📊 Варианты ВУЗов"] = message.text
    user_data[message.chat.id]["step"] = "🗂️ Направление"
    bot.send_message(message.chat.id, "Какое направление подготовки Вас интересует?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🗂️ Направление" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_direction_entrance_vuz(message):
    user_data[message.chat.id]["🗂️ Направление"] = message.text
    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_contact_channel_entrance_vuz(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_phone_number_entrance_vuz(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "entrance_vuz")
def get_agreement_entrance_vuz(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваша анкета:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# я уже обучаюсь по договору цо в ВУЗе
@bot.message_handler(func=lambda message: message.text == "Я уже обучаюсь по договору целевого обучения в ВУЗе")
def alr_studying_vuz(message):
    bot.send_message(message.chat.id, "Выберите интересующий вас пункт:", reply_markup=alr_studying_menu())
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "VUZ another question"}


# выдача памятки по ВУЗу
@bot.message_handler(
    func=lambda message: message.text == "📜 Получить памятку студента целевого обучения" and user_data.get(
        message.chat.id, {}).get("form_type") == "VUZ another question")
def get_memo_vuz(message):
    bot.send_message(message.chat.id, "Вот ваша памятка:", reply_markup=back_to_main_menu())
    with open("Буклет ВУЗ.pdf", 'rb') as file:
        bot.send_document(message.chat.id, file)


#узнать, сколько будет стипендия
@bot.message_handler(func=lambda message: message.text == "💰 Узнать сумму стипендии" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_scholarship_summ_suz(message):
    bot.send_message(message.chat.id, "В файле находится актуальная информация по суммам стипендий:", reply_markup=back_to_main_menu())
    with open("стипендия.xlsx", 'rb') as file:
        bot.send_document(message.chat.id, file)


#задать другой вопрос
@bot.message_handler(func=lambda message: message.text == "❓ Задать другой вопрос" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def start_another_quest_vuz(message):
    bot.send_message(message.chat.id, "Введите ваш вопрос:", reply_markup=back_to_main_menu())
    user_data[message.chat.id]["step"] = "question"

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "question" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_another_quest_vuz(message):
    user_data[message.chat.id]["📝 Вопрос"] = message.text
    user_data[message.chat.id]["step"] = "name"
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "name" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_name_another_quest_vuz(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())

@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_contact_channel_another_vuz(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_phone_number_another_suz(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question")
def get_agreement_another_suz(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Анкета для "Практическая подготовка"
@bot.message_handler(func=lambda message: message.text == "💪 Практическая подготовка")
def start_practice_form(message):
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "practice"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "ℹ️ Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_full_name_practice(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "📅 Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📅 Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_birth_date_practice(message):
    msg = message.text
    if check_birthdate(msg):
        user_data[message.chat.id]["📅 Дата рождения"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных дд.мм.гггг")
        return 0
    user_data[message.chat.id]["step"] = "📚 Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📚 Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_education_practice(message):
    user_data[message.chat.id]["📚 Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "👨🏽‍💼 Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "👨🏽‍💼 Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_profession_practice(message):
    user_data[message.chat.id]["👨🏽‍💼 Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "🗂️ Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🗂️ Курс" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_course_practice(message):
    user_data[message.chat.id]["🗂️ Курс"] = message.text
    user_data[message.chat.id]["step"] = "💨 Прошлая практика"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")



@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "💨 Прошлая практика" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_previous_practice_practice(message):
    msg = message.text
    if "нет" in msg.lower() and len(msg.lower()) == 3:
        user_data[message.chat.id]["💨 Прошлая практика"] = msg
        user_data[message.chat.id]["step"] = "🌐 Канал связи"
        bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())
    elif "да, " == msg.lower()[0:4]:
        user_data[message.chat.id]["💨 Прошлая практика"] = msg
        user_data[message.chat.id]["step"] = "⏳ Сроки практики"
        bot.send_message(message.chat.id, "Сроки практики?", reply_markup=back_to_main_menu())
    else:
        bot.send_message(message.chat.id,
                         """Пожалуйста, напишите либо "Нет", либо "Да" и где была практика через запятую""")
        return 0


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "⏳ Сроки практики" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_practice_duration_practice(message):
    msg = message.text
    if check_dates(msg):
        user_data[message.chat.id]["⏳ Сроки практики"] = message.text
        user_data[message.chat.id]["step"] = "🙌 Желание пройти практику в том же подразделении"
        bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, перепроверьте, в правильном ли вы формате написали, т.е.: дд.мм.гггг-дд.мм.гггг")
        return 0


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🙌 Желание пройти практику в том же подразделении" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_same_department_practice(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🙌 Желание пройти практику в том же подразделении"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите да или нет")
        return 0

    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_contact_channel_practice(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_phone_number_practice(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "practice")
def get_agreement_practice(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Анкета для "Летнее трудоустройство"
@bot.message_handler(func=lambda message: message.text == "☀️ Летнее трудоустройство")
def start_summer_employment_form(message):
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "summer_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "ℹ️ Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_full_name_summer(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович", reply_markup=back_to_main_menu())
        return 0

    user_data[message.chat.id]["step"] = "📅 Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📅 Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_birth_date_summer(message):
    msg = message.text
    if check_birthdate(msg):
        user_data[message.chat.id]["📅 Дата рождения"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных дд.мм.гггг")
        return 0
    user_data[message.chat.id]["step"] = "📚 Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📚 Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_education_summer(message):
    user_data[message.chat.id]["📚 Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "👨🏽‍💼 Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "👨🏽‍💼 Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_profession_summer(message):
    user_data[message.chat.id]["👨🏽‍💼 Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "🗂️ Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🗂️ Курс" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_course_summer(message):
    user_data[message.chat.id]["🗂️ Курс"] = message.text
    user_data[message.chat.id]["step"] = "⏳ Период трудоустройства"
    bot.send_message(message.chat.id, "На какой период рассматриваете трудоустройство?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "⏳ Период трудоустройства" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_employment_period_summer(message):
    msg = message.text
    if check_dates(msg):
        user_data[message.chat.id]["⏳ Период трудоустройства"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста,напишите период в формате дд.мм.гггг-дд.мм.гггг")
        return 0

    user_data[message.chat.id]["step"] = "💼 Опыт работы"
    bot.send_message(message.chat.id, "Работали ли Вы ранее, если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "💼 Опыт работы" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_previous_work_summer(message):
    msg = message.text
    if "нет" in msg.lower() and len(msg.lower()) == 3:
        user_data[message.chat.id]["💼 Опыт работы"] = msg
        user_data[message.chat.id]["step"] = "🌐 Канал связи"
        bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())
    elif "да, " == msg.lower()[0:4]:
        user_data[message.chat.id]["💼 Опыт работы"] = msg
        user_data[message.chat.id]["step"] = "🌐 Канал связи"
        bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())
    else:
        bot.send_message(message.chat.id,
                         """Пожалуйста, напишите либо "Нет", либо "Да" и где Вы работали через запятую""")
        return 0



@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_contact_channel_summer(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу", reply_markup=contact_channel_menu())
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_phone_number_summer(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890", reply_markup=back_to_main_menu())
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "summer_employment")
def get_agreement_summer(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Анкета для "Трудоустройство после обучения"
@bot.message_handler(func=lambda message: message.text == "👨🏼‍🎓 Трудоустройство после обучения")
def start_post_study_employment_form(message):
    user_data[message.chat.id] = {"step": "ℹ️ Ф.И.О", "form_type": "post_study_employment"}
    bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "ℹ️ Ф.И.О" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_full_name_post_study(message):
    msg = message.text
    if check_full_name(msg):
        user_data[message.chat.id]["ℹ️ Ф.И.О"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, проверьте корректность ввода данных, например: Иванов Иван Иванович")
        return 0

    user_data[message.chat.id]["step"] = "📅 Дата рождения"
    bot.send_message(message.chat.id, "Введите вашу дату рождения (дд.мм.гггг):")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📅 Дата рождения" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_birth_date_post_study(message):
    msg = message.text
    if check_birthdate(msg):
        user_data[message.chat.id]["📅 Дата рождения"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных дд.мм.гггг")
        return 0
    user_data[message.chat.id]["step"] = "📚 Обучаетесь/обучались"
    bot.send_message(message.chat.id, "Где обучаетесь/обучались?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📚 Обучаетесь/обучались" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_education_post_study(message):
    user_data[message.chat.id]["📚 Обучаетесь/обучались"] = message.text
    user_data[message.chat.id]["step"] = "👨🏽‍💼 Профессия/специальность"
    bot.send_message(message.chat.id, "По какой профессии/специальности?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "👨🏽‍💼 Профессия/специальность" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_profession_post_study(message):
    user_data[message.chat.id]["👨🏽‍💼 Профессия/специальность"] = message.text
    user_data[message.chat.id]["step"] = "🗂️ Курс"
    bot.send_message(message.chat.id, "Какой курс?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🗂️ Курс" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_course_post_study(message):
    user_data[message.chat.id]["🗂️ Курс"] = message.text
    user_data[message.chat.id]["step"] = "💨 Прошлая практика"
    bot.send_message(message.chat.id, "Проходили ли практику ранее? Если да, то где?")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "💨 Прошлая практика" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_previous_practice_post_study(message):
    msg = message.text
    if "нет" in msg.lower() and len(msg.lower()) == 3:
        user_data[message.chat.id]["💨 Прошлая практика"] = msg
        user_data[message.chat.id]["step"] = "🌐 Канал связи"
        bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())
    elif "да, " == msg.lower()[0:4]:
        user_data[message.chat.id]["💨 Прошлая практика"] = msg
        user_data[message.chat.id]["step"] = "⏳ Сроки практики"
        bot.send_message(message.chat.id, "Сроки практики?")
    else:
        bot.send_message(message.chat.id,
                         """Пожалуйста, напишите либо "Нет", либо "Да" и где была практика через запятую""")
        return 0


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "⏳ Сроки практики" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_practice_duration_post_study(message):
    msg = message.text
    if check_dates(msg):
        user_data[message.chat.id]["⏳ Сроки практики"] = message.text
        user_data[message.chat.id]["step"] = "🙌 Желание пройти практику в том же подразделении"
        bot.send_message(message.chat.id, "Хотели бы пройти практику в том же подразделении? (Да/Нет)")
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, перепроверьте, в правильном ли вы формате написали, т.е.: дд.мм.гггг-дд.мм.гггг")
        return 0


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🙌 Желание пройти практику в том же подразделении" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_same_department_post_study(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🙌 Желание пройти практику в том же подразделении"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, напишите да или нет")
        return 0

    user_data[message.chat.id]["step"] = "🌐 Канал связи"
    bot.send_message(message.chat.id, "Выберите наиболее удобный канал связи:", reply_markup=contact_channel_menu())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🌐 Канал связи" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_contact_channel_post_study(message):
    msg = message.text
    if check_contact_channel(msg):
        user_data[message.chat.id]["🌐 Канал связи"] = message.text
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, выберите вариант из меню снизу")
        return 0

    user_data[message.chat.id]["step"] = "📞 Номер телефона"
    bot.send_message(message.chat.id, "Введите ваш контактный номер телефона:")


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "📞 Номер телефона" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_phone_number_post_study(message):
    msg = message.text
    if check_phone_number(msg):
        user_data[message.chat.id]["📞 Номер телефона"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, проверьте корректность ввода данных: +71234567890")
        return 0
    user_data[message.chat.id]["step"] = "🔏Согласие на обработку данных"

    bot.send_message(message.chat.id,f"Согласны ли Вы на обработку персональных данных?", reply_markup=simple_question())


@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "🔏Согласие на обработку данных" and user_data.get(message.chat.id, {}).get("form_type") == "post_study_employment")
def get_agreement_post_study(message):
    msg = message.text
    if check_simple_question(msg):
        user_data[message.chat.id]["🔏Согласие на обработку данных"] = msg
    else:
        bot.send_message(message.chat.id, "Пожалуйста, напишите да или нет", reply_markup=simple_question())
        return 0

    user_data[message.chat.id]["step"] = "confirm_send"
    application_text = "\n".join(
        [f"{key}: {value}" for key, value in user_data[message.chat.id].items() if
         key not in ["step", "form_type"]])
    bot.send_message(message.chat.id,f"Ваш вопрос:\n\n{application_text}\n\nНапишите 'Отправить' для подтверждения отправки или 'Редактировать' для изменения данных.",reply_markup=confirm_menu())

# Общий обработчик для подтверждения отправки
@bot.message_handler(func=lambda message: user_data.get(message.chat.id, {}).get("step") == "confirm_send")
def confirm_send(message):
    if message.text.lower() == "📩 отправить":
        form_data = {key: value for key, value in user_data[message.chat.id].items() if
                     key not in ["step", "form_type"]}
        form_type = user_data[message.chat.id].get("form_type")
        application_text = "\n".join([f"{key}: {value}" for key, value in form_data.items()])

        # Если это вопрос - отправляем на почту
        if form_type in QUESTION_TYPES:
            subject = f"Новый вопрос ({'по ВУЗу' if form_type == 'VUZ another question' else 'по СУЗу' if form_type == 'SUZ another question' else 'другой'})"
            if send_email(subject, application_text, EMAIL_ADDRESS):
                bot.send_message(message.chat.id, "✔️ Вопрос успешно отправлен!")
            else:
                bot.send_message(message.chat.id, "❌ Ошибка при отправке вопроса.")

        # Если это анкета - сохраняем в Excel
        else:
            if save_form_to_excel(form_data, form_type):
                bot.send_message(message.chat.id, "✔️ Анкета успешно сохранена!")
                if pd.read_excel(FORM_FILES[form_type]).shape[0] >= 3:
                    send_email(f"Отправка анкеты {'практика' if form_type == 'practice' else 'летнее трудоустройство' if form_type == 'summer_employment' else 'трудоустройство после обучения' if form_type == 'post_study_employment' else 'целевое обучение в ВУЗе' if form_type=='entrance_vuz' else 'целевое обучение в СУЗе'}","",EMAIL_ADDRESS,filename=FORM_FILES[form_type])
                    os.remove(FORM_FILES[form_type])




            else:
                bot.send_message(message.chat.id, "❌ Ошибка при сохранении анкеты.")

        bot.send_message(message.chat.id, f"Данные:\n\n{application_text}")
        bot.send_message(message.chat.id, "Спасибо за обращение! Мы свяжемся с вами в ближайшее время.",
                         reply_markup=main_menu())

        if form_type in ["practice", "summer_employment", "post_study_employment"]:
            with open("Памятка_для_будущих_абитуриентов.pdf", 'rb') as file:
                bot.send_document(message.chat.id, file)
        del user_data[message.chat.id]

    elif message.text.lower() == "✏️ редактировать":
        if user_data[message.chat.id]["form_type"] == "Another Question":
            user_data[message.chat.id]["step"] = "📝 Вопрос"
            bot.send_message(message.chat.id, "Введите ваш вопрос")
        elif user_data.get(message.chat.id, {}).get("form_type") == "VUZ another question" or user_data.get(
                message.chat.id, {}).get("form_type") == "SUZ another question":
            user_data[message.chat.id]["step"] = "question"
            bot.send_message(message.chat.id, "Введите ваш вопрос", reply_markup=back_to_main_menu())
        else:
            user_data[message.chat.id]["step"] = "ℹ️ Ф.И.О"
            bot.send_message(message.chat.id, "Введите ваше Ф.И.О:", reply_markup=back_to_main_menu())
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите 'Отправить' или 'Редактировать'.",
                         reply_markup=confirm_menu())


@bot.message_handler(func=lambda message: message.text == "🗓 Мероприятия")
def show_events(message):
    try:
        df = pd.read_excel('events.xlsx')

        markup = InlineKeyboardMarkup()

        for index, row in df.iterrows():
            event_name = row.iloc[0]
            event_date = row.iloc[1]
            event_url = row.iloc[2]

            try:
                event_date = pd.to_datetime(event_date).strftime('%d.%m.%Y')
            except:
                pass

            button_text = f"{event_name} ({event_date})"

            if isinstance(event_url, str) and event_url.startswith(('http://', 'https://')):
                markup.add(InlineKeyboardButton(text=button_text, url=event_url))
            else:
                print(f"❌ Неверный URL для мероприятия: {event_name}")

        if not markup.keyboard:
            bot.send_message(message.chat.id, "На данный момент нет доступных мероприятий.")
            return

        back_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        back_markup.add(KeyboardButton("🔙 Назад в меню"))

        bot.send_message(message.chat.id, "Выберите мероприятие:", reply_markup=markup)

        bot.send_message(message.chat.id, "Чтобы вернуться в главное меню:", reply_markup=back_markup)

    except Exception as e:
        print(f"❌ Ошибка при чтении файла мероприятий: {e}")
        bot.send_message(message.chat.id,
                         "В данный момент информация о мероприятиях недоступна 😞\nПожалуйста, попробуйте позже.",
                         reply_markup=main_menu())


bot.polling(none_stop=True)
