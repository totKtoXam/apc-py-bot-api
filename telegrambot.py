import telebot
from telebot import types
import config
import requests
import json
from models.client import StudentClient, TeacherClient, EnrolleeClient, Client

# response = requests.get('https://localhost:7001/WeatherForecast', verify=False)
# print(response.content)

teleBot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
urlBotApi = config.CSHARP_API_URL + "bot/actions/"
# newClient = Client()

@teleBot.message_handler(content_types=['text'])
def onIncommingMessages(message):
    if message.text == "/start":
        url = urlBotApi + message.text.replace('/', '')
        response = requests.get(url, verify=False)
        jsonContent = json.loads(response.content)
        keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
        for item in jsonContent:
            # print(item)
            keyAction = types.InlineKeyboardButton(
                text=item['name'], callback_data=item['code'])
            keyboard.add(keyAction)
        clientFullName = message.from_user.first_name if message.from_user.first_name else "" + \
            message.from_user.last_name if message.from_user.last_name else ""
        question = "Здравствуйте, " + clientFullName + "!\n Выберите Вашу роль:"
        teleBot.send_message(message.from_user.id,
                             text=question, reply_markup=keyboard)
        # teleBot.send_message(message.chat.id, response.content)
        # print(response.co)
        # roleTeacher = types.InlineKeyboardButton(
        #     text='Препод', callback_data='ROLE_IS_TEACHER')
        # #
        # roleEnrollee = types.InlineKeyboardButton(
        #     text='Абитуриент', callback_data='ROLE_IS_ENROLLEE')
        # #
        # keyboard.add(roleStudent)  # добавляем кнопку в клавиатуру
        # keyboard.add(roleTeacher)
        # #
        # keyboard.add(roleEnrollee)
        # #
        # teleBot.send_message(message.from_user.id,
        #                      text=question, reply_markup=keyboard)
        # teleBot.send_message(message.chat.id, "Здравствуйте, " + clientFullName + "! Пожалуйста, введите Ваше полное ФИО:")


@teleBot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "ROLE_IS_STUDENT":
        global StudentClient
        teleBot.send_message(call.message.chat.id, 'Отлично! Вы - студент!')
        teleBot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="Вы уже выбрали роль: студент")
    if call.data == "ROLE_IS_TEACHER":
        global TeacherClient
        teleBot.send_message(call.message.chat.id, 'Отлично! Вы - преподаватель!')
        teleBot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="Вы уже выбрали роль: преподаватель")
    if call.data == "ROLE_IS_ENROLLEE":
        global EnrolleeClient
        teleBot.send_message(call.message.chat.id, 'Отлично! Вы - абитуриент!')
        teleBot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="Вы уже выбрали роль: абитуриент")

    # if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
    #     .... #код сохранения данных, или их обработки
    #     bot.send_message(call.message.chat.id, 'Запомню : )');
    # elif call.data == "no":
# RUN
teleBot.polling(none_stop=True)
