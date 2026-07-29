from core.state.ApplicationLayer.Editor.statemanager import EditorStateManager
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.application.Editor.editorutility import EditorUtility
from core.application.Editor.Menu.menueditor import MenuEditor
from core.application.Editor.Form.formeditor import FormEditor

class Application:
    def __init__(self,app_interface): # why is init the constructor. I get it initializes the class, but I would like to be free to call init/whatever form in my programs
        self.app_interface = app_interface
        self.app_interface.ui_controller.show_menu("createprojectmenu")
        self.state = EditorStateManager()
        self.util = EditorUtility(app_interface)

    def handle_event(self,event):
        pass

    def update(self):
        
        if self.state.is_state(EDITOR_STATE.NONE):
            self.clean_up_states()
        if self.state.is_state(EDITOR_STATE.MENU):
            pass

    def draw(self):
        self.app_interface.system.window.fill((0,0,0))
        
    def resize(self):
        pass

    def clean_up_states(self):
        self.app_interface.system.clean_up_states([self.state.state])

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass

    def initialize_menu_editor(self):
        self.editor = MenuEditor(self.system)