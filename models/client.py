class Client:
    Email = ""
    Phone = ""
    ClientBotId = 0
    ChatId = 0
    BotChannel = "telegram"


class StudentClient(Client):
    TicketNumber = ""
    Group = ""


class TeacherClient(Client):
    Groups = list()


class EnrolleeClient(Client):
    AfterGrade = 0
    School = ""
