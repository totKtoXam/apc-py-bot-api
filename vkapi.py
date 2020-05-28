import vk
import config
from models.client import StudentClient, TeacherClient, EnrolleeClient, Client
from validate_email import validate_email
import functions.operations as opers
from config import GetUrlApi, write_json
from enum import Enum
import six
import json
import logging
from VkKeyboard import VkKeyboardButtonColor, VkKeyboardButtonType
import math

logging.basicConfig(format=u'\n\n|LOG_START|\n\t%(filename)s[LINE:%(lineno)d]#\n\t %(levelname)-8s [%(asctime)s]  \n\t%(message)s\n|LOG_END|',
                    level=logging.ERROR,
                    filename=u"data\\logs.log")
logger = logging.getLogger(__name__)

session = vk.Session()
api = vk.API(session, v=5.0)


def send_message(user_id, token, message, attachment=""):
    isExecuted = False
    try:
        testNewKeyboard = get_keyboard(buttons=keyboardBtn, one_time=True)
        write_json(testNewKeyboard, "testNewKeyboard")
        write_json(testKeyboard, "testKeyboard")
        # api.messages.send(access_token=config.VK_API_KEY, user_id=str(
        #     user_id), message=message, attachment=attachment, keyboard=json.dumps(testKeyboard, ensure_ascii=False))
        api.messages.send(access_token=config.VK_API_KEY, user_id=str(
            user_id), message=message, attachment=attachment, keyboard=json.dumps(testNewKeyboard, ensure_ascii=False))
        isExecuted = True
        write_json(keyboardBtn, "keyboardBtn")
    except OSError as e:
        logger.error(e)
    finally:
        print("vk_send_message_completed")
    return isExecuted


def get_answer(body):
    message = "Привет, я новый бот!"
    return message


def create_answer(data, token):
    isExecuted = False
    try:
        user_id = data['user_id']
        message = get_answer(data['body'].lower())
        send_message(user_id, token, message,
                     attachment="photo-193771849_457239021")
        isExecuted = False
    except OSError as e:
        logger.error(e)
    finally:
        print("vk_create_answer_completed")
    return isExecuted


testKeyboard = {
    "one_time": True,
    "buttons": [
        # [{
        #     "action": {
        #         "type": "location",
        #         "payload": "{\"button\": \"1\"}"
        #     }
        # }],
        # [{
        #     "action": {
        #         "type": "open_app",
        #         "app_id": 6979558,
        #         "owner_id": -181108510,
        #         "hash": "sendKeyboard",
        #         "label": "Отправить клавиатуру"
        #     }
        # }],
        # [{
        #     "action": {
        #         "type": "vkpay",
        #         "hash": "action=transfer-to-group&group_id=181108510&aid=10"
        #     }
        # }],
        [{
            "action": {
                "type": "text",
                "payload": "{\"button\": \"Negative\"}",
                "label": "Negative"
            },
            "color": "negative"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"Positive\"}",
                    "label": "Positive"
                },
                "color": "positive"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"Primary\"}",
                    "label": "Primary"
                },
                "color": "primary"
        },
            {
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"Secondary\"}",
                    "label": "Secondary"
                },
                "color": "secondary"
        }
        ]
    ]
}


def get_button(label, color=VkKeyboardButtonColor.PRIMARY, payload=None, type='text'):
    result = {
        "action": {
            "type": "text",
            "payload": "{\"command\": \"" + (payload if payload is not None else label) + "\"}",
            "label": label
        },
        "color": color
    }
    return result


keyboardBtn = []
keyboardBtn.append(get_button("bnt1", "primary", "primary1btn"))
keyboardBtn.append(get_button("bnt2", "secondary", "primary2btn"))
keyboardBtn.append(get_button("bnt3", "negative", "primary3btn"))
keyboardBtn.append(get_button("bnt4", "positive", "primary4btn"))
keyboardBtn.append(get_button("bnt5", "primary"))
keyboardBtn.append(get_button("bnt6"))


def get_keyboard(buttons=[], one_time=False, inline=False, lineLenght=4):
    write_json(buttons, "vkkeyboardbuttons")
    btnLines = []
    inlineIndex = 0
    lineIndex = 0
    for button in buttons:
        if (inlineIndex == 0 and math.ceil(btnLines.__len__() != len(buttons)/lineLenght)):
            btnLines.append([])
        btnLines[lineIndex].append(button)
        inlineIndex += 1
        if (inlineIndex % lineLenght == 0):
            inlineIndex = 0
            lineIndex += 1

    write_json(btnLines, "btnLine")

    return {
        "one_time": one_time,
        "buttons": btnLines
    }


def check_server_key(data):
    if(data["secret"] == config.SERVER_SECRET_KEY):
        return True
    else:
        return False
