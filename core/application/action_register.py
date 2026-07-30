from systemlogging import log_event

class ActionRegistrar:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        self.system = app_interface.system

    def register(self):
        self.app_interface.actions.register("create_project",self.app_interface.app_object.util.create_project)

        self.app_interface.actions.register("app_to_menu", self.app_interface.app_object.navigation.main_menu)
        self.app_interface.actions.register("app_resume", self.app_interface.app_object.toggle_pause)

        self.app_interface.actions.register("main_menu", lambda: self.app_interface.ui_controller.show_ui("createprojectmenu"))

        self.app_interface.actions.register("new_project_form",lambda: self.app_interface.ui_controller.show_ui("newprojectform"))
        self.app_interface.actions.register("quit",self.system.quit)
