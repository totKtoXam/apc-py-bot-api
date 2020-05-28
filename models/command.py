class CommandExecForm:
    Command = ""
    Content = dict()

    def __init__(self, _command="", _content={}):
        self.Command = _command
        self.Content = _content
