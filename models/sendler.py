from typing import List, Optional
from json import JSONEncoder
import json
# from pydantic import BaseModel


class SendlerForm ():
    BotChannel = "TELEGRAM"
    Text = ""
    Attachments = []


class PostAttachment:
    Type = ""

    Id = 0
    OwnerId = 0
    Url = ""
    Title = ""
    Text = ""
    Ext = ""

    AccessKey = ""

    def clear(self):
        self.Type = ""
        self.Id = 0
        self.OwnerId = 0
        self.Url = ""
        self.Title = ""
        self.Text = ""
        self.Ext = ""
        self.AccessKey = ""


def create_sendler_form(data):
    sendler_form = SendlerForm()
    sendler_form.BotChannel = "TELEGRAM"
    sendler_form.Text = data["text"]
    sendler_form.Attachments = []

    return sendler_form


def GetAttachments(data):
    attachs = []
    if ("attachments" not in data):
        return 404
    if (data["attachments"] is None):
        return 400

    for attach in data["attachments"]:
        post_attach = PostAttachment()
        post_attach.Type = attach["type"]
        post_attach.Id = attach[attach["type"]]["id"]
        post_attach.OwnerId = attach[attach["type"]]["owner_id"]
        post_attach.OwnerId = attach[attach["type"]]["access_key"]

        if (attach["type"] == "photo"):
            post_attach.Url = attach[attach["type"]]["photo_807"]
            post_attach.Text = attach[attach["type"]]["text"]
        else:
            post_attach.Title = attach[attach["type"]]["title"]
            post_attach.Url = attach[attach["type"]]["url"]
            post_attach.Ext = attach[attach["type"]]["ext"]

        attachs.append(post_attach.__dict__)
    return attachs


def ApplySending(data=None, teleBot=None, vkBot=None):
    if (data is None):
        return 400

    if ("studentList" not in data):
        return 404
    if ((data["studentList"] is None) or (len(data["studentList"]) == 0)):
        return 400

    if (("studentList" in data) and "sendingFileList" in data):
        for student in data["studentList"]:
            for sending_file in data["sendingFileList"]:
                if ((sending_file["type"] == "photo") and ("url" in sending_file)):
                    if (teleBot is not None):
                        if (("teleChatId" in student) and (student["teleChatId"] is not None)):
                            teleBot.send_message(
                                student["teleChatId"], f'{sending_file["text"] if "text" in sending_file else ""}\n{sending_file["url"]}')
                    if (vkBot is not None):
                        if (("vkChatId" in student) and (student["vkChatId"] is not None)):
                            vkBot.messages.send(access_token="eee2e56af72e125b7511d765e3920fb247a002787383b55bbdd893e886526999e189ae920e8ecc441a03b",
                                                user_id=student["vkChatId"], message="", attachment="photo" + sending_file["ownerId"]["id"])
