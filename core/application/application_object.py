from core.state.ApplicationLayer.Editor.statemanager import EditorStateManager
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.application.editorutility import EditorUtility

class Application_Object:
    def __init__(self,app_interface): # why is init the constructor. I get it initializes the class, but I would like to be free to call init/whatever form in my programs
        self.app_interface = app_interface
        self.app_interface.ui_controller.show_menu("createprojectmenu")
        self.state = EditorStateManager()
        self.util = EditorUtility(app_interface)

    def update(self):
        if self.state.is_state(EDITOR_STATE.MENU):
            pass

    def draw(self):
        self.app_interface.system.window.fill((0,0,0))

    def resize(self):
        pass

    def clean_up_states(self):
        pass

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass
