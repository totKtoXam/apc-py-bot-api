import telebot
from telebot import types
from flask import Flask, request
import config
from config import GetUrlBotApiInfo, write_json
import requests
import json
import logging
import functions.operations as opers
import platform
import time
from models.client import StudentClient, TeacherClient, EnrolleeClient, Client
from models.sendler import create_sendler_form, GetAttachments, ApplySending
from validate_email import validate_email
import re
import jsons
import vk
import vkapi

global prevSection
global client
client = Client()

# LOGGING PART
logging.basicConfig(format=u'\n\n|LOG_START|\n\t%(filename)s[LINE:%(lineno)d]#\n\t %(levelname)-8s [%(asctime)s]  \n\t%(message)s\n|LOG_END|',
                    level=logging.ERROR,
                    filename=u"data/logs.log")
logger = logging.getLogger(__name__)
# logger.level  - уровень лога
# logger.setLevel()   # 10 / DEBUG / logging.DEBUG
# NOTSET    - 0
# DEBUG     - 10
# INFO      - 20
# WARNING   - 30
# ERROR     - 40
# CRITICAL  - 50

# for key in logging.Logger.manager.loggerDict:
#     print(key)

#   FLASK
app = Flask(__name__)


# TELEGRAM BOT PART
teleBot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN, threaded=False)

teleBot.remove_webhook()
time.sleep(1)
teleBot.set_webhook(
    url="https://7b6b159d.ngrok.io/api/tele/{}".format(config.TELEGRAM_BOT_TOKEN))


@app.route("/api/tele/{}".format(config.TELEGRAM_BOT_TOKEN), methods=['GET', 'POST'])
def GetIndex():
    if request.method == 'POST':
        teleBot.process_new_updates(
            [telebot.types.Update.de_json(request.get_json())])
    return "ok", 200


@app.route("/api/vk/messages", methods=['POST'])
def vkGetMessages():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return config.SERVER_COMFIRMATION_KEY
    elif data['type'] == 'message_new':
        vkapi.create_answer(data['object'], config.VK_API_KEY)
        write_json(data['object'], fileName="vkmessage")
        return 'ok'


@app.route("/api/vk/posts", methods=['POST'])
def vkGetPosts():
    data = json.loads(request.data)
    if 'type' not in data.keys():
        return 'not vk'
    if data['type'] == 'confirmation':
        return config.SERVER_COMFIRMATION_KEY
    else:
        write_json(data['object'], fileName="postFile")
        result = create_sendler_form(data['object'])
        result.Attachments = GetAttachments(data['object'])
        url = config.CSHARP_API_URL + "sendler/vkpost"
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        if ((result is not None) and result != 400):
            write_json(data=result.__dict__, fileName="postresult")
            # write_json(data=jsons.dump(result.__dict__), fileName="postresult")
            response = opers.ExecuteActions(
                url=url, reqstType="POST", sending_body=jsons.dump(result.__dict__), headers=headers)
            if ("status_code" in response):
                send_error_message_to_developer(response)
            else:
                write_json(data=response, fileName="responseSendler")
                ApplySending(data=response, teleBot=teleBot, vkBot=vkapi.api)
            return 'ok'
            # if (response == "REQUEST_ERROR")
    return 'ok'
    # data = json.loads(request.data)
    # if 'type' not in data.keys():
    #     return {"status_code": "404", "content": "NOT_VK"}
    # if data['type'] == 'confirmation':
    #     return config.SERVER_COMFIRMATION_KEY
    # elif data['type'] == 'message_new':
    #     session = vk.Session()
    #     api = vk.API(session, v=5.0)
    #     user_id = data['object']['user_id']
    #     api.messages.send(access_token=config.VK_API_KEY, user_id=str(user_id), message='Привет, я новый бот!')
    # return {"status_code": "200", "content": "SUCCESS"}


@app.route("/api/sendler", methods=['POST'])
def Sendler():
    data = json.loads(request.data)
    write_json(data, fileName="post")


@app.route("/", methods=['GET'])
def MainIndex():
    linkStyle = "text-align: center; margin: auto; margin-top: 20%; width: 600px; padding: 10px; border: 2px solid red; border-radius: 25px;"
    return "<div style=\"" + linkStyle + "\"><h1><a href='" + config.TELE_BOT_PROFILE_URL + "'>@" + config.TELE_BOT_NAME + "</a></h1>"


@teleBot.message_handler(content_types=['text'])
def onIncommingMessages(message):
    command = opers.get_command(message.text)
    write_json(data=message.chat.__dict__, fileName="telemessage")
    if (message.text in config.LOCAL_COMMANDS):
        text = "на тебе фото"
        imgUrl = "https://sun9-11.userapi.com/c840329/v840329318/cdeb/dHft4lHtLao.jpg"
        teleBot.send_message(message.chat.id, f'{text}\n{imgUrl}')
    elif ((command is not None) and command != 404):
        client.ChatId = str(message.chat.id)
        url = GetUrlBotApiInfo(command)
        response_result = opers.ExecuteActions(url)
        if (response_result == "REQUEST_ERROR"):
            server_error(message)
            send_error_message_to_developer(response_result)
        else:
            if ("status_code" in response_result):
                server_error(message)
            else:
                if ("stepCode" in response_result):
                    write_json(response_result)
                    if ("actionList" in response_result):
                        key_board = types.InlineKeyboardMarkup()
                        for item in response_result['actionList']:
                            keyAction = types.InlineKeyboardButton(
                                text=item['name'], callback_data=item['code'])
                            key_board.add(keyAction)
                        teleBot.send_message(
                            message.from_user.id, text=response_result['stepName'], reply_markup=key_board)
                    else:
                        teleBot.send_message(
                            message.from_user.id, text=response_result['stepName'])
                elif("sectionCode" in response_result):
                    pass
                else:
                    send_error_message_to_developer(response_result)
    else:
        command_is_unknown(message)

    # if message.text == "/start":
    #     # url = urlBotApi + message.text.replace('/', '')
    #     url = GetUrlApi(message.text.replace('/', ''))
    #     try:
    #         response = requests.get(url, verify=False)

    #         jsonContent = json.loads(response.content)
    #         keyboard = types.InlineKeyboardMarkup()  # наша клавиатура
    #         for item in jsonContent:
    #             # print(item)
    #             keyAction = types.InlineKeyboardButton(
    #                 text=item['name'], callback_data=item['code'])
    #             keyboard.add(keyAction)

    #         clientFullName = message.from_user.first_name if message.from_user.first_name else "" + \
    #             message.from_user.last_name if message.from_user.last_name else ""
    #         question = "Здравствуйте, " + clientFullName + "!\n Выберите Вашу роль:"
    #         teleBot.send_message(message.from_user.id,
    #                              text=question, reply_markup=keyboard)
    #     except OSError as e:
    #         logger.error(e)
    #         # logger.error(e, exc_info=True)
    #     else:
    #         teleBot.send_message(
    #             message.from_user.id, "Ошибка сервера. Просим прощения на досталвенные неудобства.")


@teleBot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if ("ROLE_IS_" in call.data):
        # ClientChatId == call.message.chat.id
        client.RoleCode = call.data
        roleName = "студент" if ("STUDENT" in call.data) else "преподаватель" if (
            "TEACHER" in call.data) else "абитуриент"
        teleBot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="Вы уже выбрали роль: " + roleName)
        teleBot.send_message(chat_id=call.message.chat.id,
                             text=" Если запрашиваемые данные являются не обязательными и Вы не хотите или по какой-либо причине не желаете давать их, то введите \"-\". Обязательные данные будут отмечены *")
        teleBot.send_message(chat_id=call.message.chat.id,
                             text="Чтобы прервать регистрацию введите /stop")
        client_reg(call.message)


# ENROLLEE
def client_reg(message):
    get_and_send_msg_text(
        message, "Отлично! Введите фамилию*:", 1, get_last_name)


def get_last_name(message):
    client.LastName = get_and_send_msg_text(
        message, "Введите имя*:", 1, get_first_name)


def get_first_name(message):
    client.FirstName = get_and_send_msg_text(
        message, "Введите отчество:", 1, get_middle_name)


def get_middle_name(message):
    mdlName = get_and_send_msg_text(
        message, "Введите эл. адрес*:", 1, get_email)
    if (mdlName != "-"):
        client.MiddleName = mdlName


def get_email(message):
    email = message.text
    if (validate_email(email)):
        client.Email = get_and_send_msg_text(
            message, "Введите сот. номер без \"+7\" в формате 7771112233:", 1, get_phone)
    else:
        get_and_send_msg_text(
            message, "Эл. адрес был введён некорректно. Введите эл. адрес повторно*:", 1, get_email)


def get_phone(message):
    if (client.RoleCode == "ROLE_IS_STUDENT"):
        phone = get_and_send_msg_text(
            message, "Введите номер Вашего студ. билета*:", 1, get_ticket_number)
    elif (client.RoleCode == "ROLE_IS_TEACHER"):
        phone = phone = get_and_send_msg_text(
            message, "Введите Ваш ИИН (Необходим для уникальности записи)*:", 1, get_teacher_iin)
        pass
    else:
        phone = get_and_send_msg_text(
            message, "Отлично! Ожидайте ответа. Введите /help, чтобы получить больше информации.", 2, create_post_client_from_tele)
    if (phone != "-"):
        client.Phone = phone


# teacher
def get_teacher_iin(message):
    # client.TeacherIIN
    iin = get_and_send_msg_text(
        message, "Введите группу, которую Вы курируете:", 1, get_group)
    if (re.search(r'\d{12}', iin)):
        client.TeacherIIN = iin
    else:
        get_and_send_msg_text(
            message, "ИИН был введён некорректно. Введите ИИН повторно*:", 1, get_teacher_iin)


# student
def get_ticket_number(message):
    client.TicketNumber = get_and_send_msg_text(
        message, "Введите группу, в которой Вы обучаетесь*:", 1, get_group)


def get_group(message):
    client.Group = get_and_send_msg_text(
        message, "Отлично! Ожидайте ответа. Введите /help, чтобы получить больше информации.", 2, create_post_client_from_tele)


def create_post_client_from_tele(message):
    client.BotChannel = "TELEGRAM"
    data = jsons.dump(client.__dict__)
    headers = {'Content-type': 'application/json',  # Определение типа данных
               'Accept': 'text/plain',
               'Content-Encoding': 'utf-8'}
    response_result = opers.ExecuteActions(url=config.CSHARP_API_BOT_URL +
                                           "createClient", reqstType='POST', headers=headers, sending_body=data)
    if (response_result == "REQUEST_ERROR"):
        server_error(message)
        send_error_message_to_developer(response_result)
    else:
        if ("status_code" in response_result):
            server_error(message)
        else:
            client.ClientBotId = response_result['clientBotId']
            get_and_send_msg_text(
                message,
                "Регистрация прошла успешно! Подтвердите эл. почту, чтобы получать необходимую информацию и рассылку. Введите /help, чтобы получить больше инфорации." +
                "Ожидайте активации учётной записи администратором." if "TEACHER" in client.RoleCode else "")


def get_and_send_msg_text(message, text="Бот сломался ;D", type_s=0, func=None):
    if ("/" in message.text):
        if (opers.check_command(opers.get_command(message.text))):
            pass
        elif (check_local_command(opers.get_command(message.text))):
            if (message.text == "/stop"):
                teleBot.send_message(
                    message.chat.id, "Регистрация прервана. Чтобы начать регистрацию повторно введите /start")
                return

    teleBot.send_message(message.chat.id, text)
    if type_s == 1:
        if(func is not None):
            teleBot.register_next_step_handler(message, func)
    if (type_s == 2):
        func(message)
    return message.text


def send_error_message_to_developer(error_msg):
    teleBot.send_message(config.DEV_CHAT_ID, text=error_msg)


def command_is_unknown(message):
    teleBot.send_message(message.from_user.id,
                         text="Извините, но бот не знает указанной команды")


def server_error(message):
    teleBot.send_message(
        message.from_user.id, text="Ошибка сервера. Просим прощения за доставленные неудобства.")


def check_local_command(command):
    return False


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
# try:
#     teleBot.polling(timeout=30)
# except:
#     time.sleep(15)
#     teleBot.polling(timeout=30)
    # teleBot.polling(none_stop=True)
