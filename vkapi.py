import vk
import config
from models.client import StudentClient, TeacherClient, EnrolleeClient, Client
from validate_email import validate_email
import functions.operations as opers
from config import GetUrlBotApiInfo, write_json

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, token, message, attachment=""):
    api.messages.send(access_token=config.VK_API_KEY, user_id=str(
        user_id), message=message, attachment=attachment)


def get_answer(body):
    message = "Привет, я новый бот!"
    return message


def create_answer(data, token):
    user_id = data['user_id']
    message = get_answer(data['body'].lower())
    send_message(user_id, token, message)

# def get_and_set_messge():
#     if ()