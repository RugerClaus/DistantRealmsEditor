from helper import sine
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

from core.util.colors import *
from core.state.ApplicationLayer.Editor.statemanager import EditorStateManager
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.application.Editor.editorutility import EditorUtility
from core.application.Editor.navigation import Navigation

class Application:
    def __init__(self,app_interface):
        self.app_interface = app_interface
        self.state = EditorStateManager()
        self.util = EditorUtility(app_interface)
        self.editor = None
        self.ProjectBrowser = None
        self.navigation = Navigation(app_interface)
        
        self.init()

    def handle_event(self,event,command):
        if self.state.is_state(EDITOR_STATE.NONE):
            if self.ProjectBrowser:
                self.ProjectBrowser.handle_event(event,command)
            return
        
        if self.editor:
            self.editor.handle_event(event,command)

        

        if self.app_interface.system.control_state.is_state(DEVELOPER_MODE.ON):

            if command == "reload_menu_editor":
                self.initialize_menu_editor()
                print("Reloading Menu Editor...")
            elif command == "reload_form_editor":
                self.initialize_form_editor()
                print("Reloading Form Editor...")

    def update(self):
        
        if self.state.is_state(EDITOR_STATE.NONE):

            pulse = sine(self.app_interface.system.time.get_current_time())
            fade_color = (
                int(50 * pulse), 
                int(50 * pulse), 
                int(50 * pulse)
            )
            self.app_interface.system.window.fill((fade_color))
            self.clean_up_states()


            if self.ProjectBrowser:
                self.ProjectBrowser.update()

            self.util.display_volume(self.app_interface.ui_controller.get_active_ui())

        else:
            if self.editor:
                self.editor.update()

    def draw(self):
        
        if self.editor:
            self.editor.draw()

        if self.ProjectBrowser:
            self.ProjectBrowser.draw()

    def resize(self):
        pass

    def clean_up_states(self):
        self.app_interface.system.app_inspector.clear()
        self.app_interface.system.clean_up_states([self.state.state])

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass

    def init(self):
        self.app_interface.ui_controller.show_ui("editor_main_menu")

    def initialize_project_browser(self):
        import importlib
        from core.application.Editor import projectbrowser
        importlib.reload(projectbrowser)
        self.ProjectBrowser = projectbrowser.ProjectBrowser(self)
        self.app_interface.ui_controller.clear()
        self.app_interface.ui_controller.show_ui("editor_project_browser")

    def initialize_menu_editor(self):
        import importlib
        from core.application.Editor.Menu import menueditor
        importlib.reload(menueditor)
        self.editor = menueditor.MenuEditor(self.app_interface)
        self.app_interface.ui_controller.clear()
        self.app_interface.ui_controller.show_ui("editor_noprops")

    def initialize_form_editor(self):
        import importlib
        from core.application.Editor.Form import formeditor
        importlib.reload(formeditor)
        self.editor = formeditor.FormEditor(self.app_interface)
        self.app_interface.ui_controller.clear()
        self.app_interface.ui_controller.show_ui("form_editor_noprops")