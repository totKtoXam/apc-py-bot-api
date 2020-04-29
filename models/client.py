class Client:
    Email = ""
    Phone = ""
    ClientBotId = 0
    ChatId = 0
    RoleCode = ""
    BotChannel = "telegram"
    LastName = ""
    FirstName = ""
    MiddleName = ""
    TicketNumber = ""
    Group = ""
    AfterGrade = 0
    School = ""
    TeacherIIN = ""

    # def set_attr(self):
    #     pass

    # def set_attr(self, Email="", Phone="", ClientBotId="", ChatId=0, RoleCode="ROLE_IS_ENROLLEE"):
    #     self.Email = Email
    #     self.Phone = Phone
    #     self.ClientBotId = ClientBotId
    #     self.ChatId = ChatId
    #     self.RoleCode = RoleCode


class StudentClient(Client):
    TicketNumber = ""
    Group = ""


class TeacherClient(Client):
    Groups = list()


class EnrolleeClient(Client):
    AfterGrade = 0
    School = ""


class StartStepCode():
    START = "REG_START"
    SELECT_ROLE = "SELECT_ROLE"
    INPUT_EMAIL = "INPUT_EMAIL"
    INPUT_PHONE = "INPUT_PHONE"
    FINISH = "FINISH"
