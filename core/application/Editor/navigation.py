from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
class Navigation:
    def __init__(self,app_interface):
        self.app_interface = app_interface

    def main_menu(self):
        self.app_interface.ui_controller.show_ui("createprojectmenu")
        self.app_interface.app_object.state.set_state(EDITOR_STATE.NONE)