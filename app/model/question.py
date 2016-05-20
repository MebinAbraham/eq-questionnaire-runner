from app.model.display import Display


class Question(object):
    def __init__(self):
        self.id = None
        self.title = None
        self.description = None
        self.responses = []
        self.children = self.responses
        self.container = None
        self.questionnaire = None
        self.validation = None
        self.questionnaire = None
        self.templatable_properties = ['description']
        self.display = Display()

    def add_response(self, response):
        if response not in self.responses:
            self.responses.append(response)
            response.container = self
