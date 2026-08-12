from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
class Navigation:
    def __init__(self,distant_realms):
        self.distant_realms = distant_realms

    def main_menu(self):
        editor = self.distant_realms.application.editor
        if editor:
            self.distant_realms.application.editor.clean_up_states()
        browser = self.distant_realms.application.ProjectBrowser
        if browser:
            self.distant_realms.application.ProjectBrowser = None
        self.distant_realms.ui_controller.show_ui("editor_main_menu")
        self.distant_realms.application.state.set_state(EDITOR_STATE.NONE)
        self.distant_realms.application.editor = None