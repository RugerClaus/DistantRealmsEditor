class ActionRegistrar:
    def __init__(self, application):
        self.application = application
        self.system = application.system

    def register(self):
        application = self.application
        application.actions.register("quit",self.system.quit)