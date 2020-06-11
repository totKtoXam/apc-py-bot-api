import json
import re
from functions.operations import get_command
# from main import clients_sections

TELEGRAM_BOT_TOKEN = "1178033047:AAEyvJ_8h867js85trumkjqEwkLkiYZxobo"
TELE_BOT_NAME = "AstanaPolytechCollegeBot"
TELE_BOT_PROFILE_URL = "https://t.me/AstanaPolytechCollegeBot"

VK_API_KEY = "eee2e56af72e125b7511d765e3920fb247a002787383b55bbdd893e886526999e189ae920e8ecc441a03b"
SERVER_COMFIRMATION_KEY = "8aeaa9c1"
SERVER_SECRET_KEY = "FF4DDB22A5AD7A7853E74B2FDB524"

DEV_CHAT_ID = 757051459

MAX_LOG_COUNT = 200
startLog = "|LOG_START|"

CSHARP_API_URL = "https://localhost:7001/api/"
CSHARP_API_BOT_URL = "https://localhost:7001/api/bot/"  # local

DEV_URL = "https://747df95f7c5d.ngrok.io/"

LOCAL_COMMANDS = ["/getimg", "/test"]


def GetUrlApi(chatId, apiName, commandName):
    return CSHARP_API_URL + apiName + "/" + commandName + '?channel=TELEGRAM&chatId=' + str(chatId)


def GetLogs():
    handle = open("/logging.logs.log", "w")
    CheckCountLogs(handle)


def CheckCountLogs(handle):
    fileData = handle.readlines()
    print(re.findall(startLog, fileData))


def write_json(data, fileName="answer.json"):
    if (".json" not in fileName):
        fileName += ".json"
    with open("data/" + fileName, 'w') as f:
        try:
            json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as ex:
            json.dump(data.__dict__, f, indent=2, ensure_ascii=False)
            print(ex)


def create_or_update_current_command_item(chatId, item_list, channel, command=None, inWork=True):
    if (channel is not None and item_list is not None):
        index = findIndexByChatId(item_list, chatId, channel)
        if (index is not None):
            if (command is not None):
                item_list[channel][index]["command"] = command
            item_list[channel][index]["inWork"] = inWork
        else:
            new_item = {
                "chatId": chatId,
                "command": command,
                "inWork": inWork
            }
            item_list[channel].append(new_item)
    return item_list


def findIndexByChatId(item_list, chatId, channel=None):
    index = 0
    if (channel is None):
        while index < item_list.__len__():
            if (item_list[index]["chatId"] == chatId):
                return index
    else:
        while index < item_list[channel].__len__():
            if (item_list[channel][index]["chatId"] == chatId):
                return index
    return None


def get_command_msg_id(item_list, chatId):
    for item in item_list:
        if (item["chatId"] == chatId):
            return item["startedMsgId"]
    return None


def get_command_by_chat_id(item_list, chatId):
    for item in item_list:
        if(item["chatId"] == chatId):
            return item["command"]
    return None


def check_command_in_work(item_list, chatId, command=None):
    for item in item_list:
        if (command is None):
            if(item["chatId"] == chatId):
                return item["inWork"]
        else:
            if (item["command"] == command and item["chatId"] == chatId):
                return item["inWork"]
    return False


class RegexPatterns:
    Is_Letters = "^[А-Яа-яӘІҢҒҮҰҚӨҺәіңғүұқөһ]*$"

    @staticmethod
    def is_letters(text):
        result = re.fullmatch(RegexPatterns.Is_Letters, text)
        return result
