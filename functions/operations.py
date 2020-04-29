import requests
import logging
import re

logging.basicConfig(format=u'\n\n|LOG_START|\n\t%(filename)s[LINE:%(lineno)d]#\n\t %(levelname)-8s [%(asctime)s]  \n\t%(message)s\n|LOG_END|',
                    level=logging.ERROR,
                    filename=u"data\\logs.log")
logger = logging.getLogger(__name__)


def ExecuteActions(url, reqstType="GET", headers=None, sending_body=None):
    response = ''
    try:
        if((sending_body is not None and reqstType == "GET") or (reqstType == "POST" and sending_body is not None)):
            response = requests.post(url, json=sending_body, headers=headers, verify=False)
        elif(reqstType == "PUT"):
            response = requests.put(url, json=sending_body, verify=False)
        elif(reqstType == "GET"):
            response = requests.get(url, verify=False)
        elif(reqstType == "PATCH"):
            response = requests.patch(url, json=sending_body, verify=False)
        elif(reqstType == "DELETE"):
            response = requests.delete(url, verify=False)

        if (response.status_code == 200):
            return  response.json()
        else:
            return {'status_code': response.status_code, 'content': response.reason}
    except OSError as e:
        logger.error(e)
        # logger.error(e, exc_info=True)
    else:
        return "REQUEST_ERROR"
    finally:
        print("Operation finished...")


def get_command(text):
    if ("/" in text):
        pattern = r"/\w+"
        command = re.search(pattern, text).group()[1:]
        if(check_command(command)):
            return command
    return 404
        

def check_command(command):
    try:
        response = requests.get("https://localhost:7001/api/bot/checkStep/" + command, verify=False)
        if (response.status_code == 200):
            return True
        elif(response.status_code == 404):
            return False
    except OSError as e:
        logger.error(e)
    else:
        return False

# get GetNextStep():
