import json
import re

TELEGRAM_BOT_TOKEN = "1178033047:AAEyvJ_8h867js85trumkjqEwkLkiYZxobo"
TELE_BOT_NAME = "AstanaPolytechCollegeBot"
TELE_BOT_PROFILE_URL = "https://t.me/AstanaPolytechCollegeBot"

VK_API_KEY = "eee2e56af72e125b7511d765e3920fb247a002787383b55bbdd893e886526999e189ae920e8ecc441a03b"
SERVER_COMFIRMATION_KEY = "24e5c513"
SERVER_SECRET_KEY = "FF4DDB22A5AD7A7853E74B2FDB524"

DEV_CHAT_ID = 757051459

MAX_LOG_COUNT = 200
startLog = "|LOG_START|"

CSHARP_API_URL = "https://localhost:7001/api/"
CSHARP_API_BOT_URL = "https://localhost:7001/api/bot/"  # local

DEV_URL = "https://6e79ec90.ngrok.io/"

LOCAL_COMMANDS = ["/getimg", "/test"]

def GetUrlBotApiInfo(*apiLinks):
    apiUrl = CSHARP_API_BOT_URL + "actions/"
    for link in apiLinks:
        apiUrl += link + "/"
    return apiUrl

# url = GetUrlApi("asd", "asd")
# print(url)


def GetLogs():
    handle = open("/logging.logs.log", "w")
    CheckCountLogs(handle)

# def LogFileClear(handle):
#     for line in handle:


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
            # json.dump(data, f, indent=2, ensure_ascii=False)
            print(ex)
