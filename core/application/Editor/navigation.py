from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
class Navigation:
    def __init__(self,app_interface):
        self.app_interface = app_interface

    def main_menu(self):
        editor = self.app_interface.application.editor
        if editor:
            self.app_interface.application.editor.clean_up_states()
        browser = self.app_interface.application.ProjectBrowser
        if browser:
            self.app_interface.application.ProjectBrowser = None
        self.app_interface.ui_controller.show_ui("editor_main_menu")
        self.app_interface.application.state.set_state(EDITOR_STATE.NONE)
        self.app_interface.application.editor = None