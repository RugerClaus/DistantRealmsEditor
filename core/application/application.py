from helper import sine
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

from core.util.colors import *
from core.state.ApplicationLayer.Editor.statemanager import EditorStateManager
from core.state.ApplicationLayer.Editor.Pause.statemanager import PauseStateManager
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.state.ApplicationLayer.Editor.Pause.state import PAUSE_STATE
from core.application.Editor.editorutility import EditorUtility
from core.application.Editor.Form.formeditor import FormEditor
from core.application.Editor.navigation import Navigation

class Application:
    def __init__(self,app_interface): # why is init the constructor. I get it initializes the class, but I would like to be free to call init/whatever form in my programs
        self.app_interface = app_interface
        self.state = EditorStateManager()
        self.pause_state = PauseStateManager()
        self.util = EditorUtility(app_interface)
        self.editor = None
        self.navigation = Navigation(app_interface)
        self.init()

    def toggle_pause(self):
        if self.pause_state.is_state(PAUSE_STATE.PAUSED):
            self.pause_state.set_state(PAUSE_STATE.ACTIVE)
            self.app_interface.ui_controller.clear()
            if self.state.is_state(EDITOR_STATE.MENU):
                self.app_interface.ui_controller.show_ui("menu_editor_ui")
            elif self.state.is_state(EDITOR_STATE.FORM):
                self.app_interface.ui_controller.show_ui("form_editor_ui")
        elif self.pause_state.is_state(PAUSE_STATE.ACTIVE):
            self.pause_state.set_state(PAUSE_STATE.PAUSED)
            self.app_interface.ui_controller.show_ui("pause")

    def handle_event(self,event,command=None):
        if self.state.is_state(EDITOR_STATE.NONE):
            return
        if event.type == self.app_interface.system.input.keydown():
            if event.key == self.app_interface.system.input.keys.escape_key():
                self.toggle_pause()

        if self.pause_state.is_state(PAUSE_STATE.ACTIVE):
            if self.editor:
                self.editor.handle_event(event)

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
                int(255 * pulse), 
                int(255 * pulse), 
                int(255 * pulse)
            )
            self.app_interface.system.window.fill((fade_color))
            self.clean_up_states()
        else:
            if self.pause_state.is_state(PAUSE_STATE.ACTIVE):
                if self.editor:
                    self.editor.update()
        
    def draw(self):
        
        if self.editor:
            self.editor.draw()
        

    def resize(self):
        pass

    def clean_up_states(self):
        self.app_interface.system.clean_up_states([self.state.state,self.pause_state.state])

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass

    def init(self):
        self.app_interface.ui_controller.show_ui("mainmenu")

    def initialize_menu_editor(self):
        import importlib
        from core.application.Editor.Menu import menueditor
        importlib.reload(menueditor)
        self.editor = menueditor.MenuEditor(self.app_interface)
        self.app_interface.ui_controller.clear()
        self.app_interface.ui_controller.show_ui("menu_editor_ui")

    def initialize_form_editor(self):
        import importlib
        from core.application.Editor.Form import formeditor
        importlib.reload(formeditor)
        self.editor = formeditor.FormEditor(self.app_interface)
        self.app_interface.ui_controller.clear()
        self.app_interface.ui_controller.show_ui("form_editor_ui")