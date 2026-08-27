from helper import sine
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

from core.util.colors import *
from core.state.ApplicationLayer.Editor.statemanager import EditorStateManager
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from application.Editor.editorutility import EditorUtility
from application.Editor.navigation import Navigation

class Application:
    def __init__(self,distant_realms):
        self.distant_realms = distant_realms
        self.state = EditorStateManager()
        self.util = EditorUtility(distant_realms)
        self.editor = None
        self.ProjectBrowser = None
        self.navigation = Navigation(distant_realms)
        
        self.init()

    def handle_event(self,event,command):
        if self.state.is_state(EDITOR_STATE.NONE):
            if self.ProjectBrowser:
                self.ProjectBrowser.handle_event(event,command)
            return
        
        if self.editor:
            self.editor.handle_event(event,command)

        

        if self.distant_realms.system.control_state.is_state(DEVELOPER_MODE.ON):

            if command == "reload_menu_editor":
                self.initialize_menu_editor()
                print("Reloading Menu Editor...")
            elif command == "reload_form_editor":
                self.initialize_form_editor()
                print("Reloading Form Editor...")

    def update(self):
        
        if self.state.is_state(EDITOR_STATE.NONE):

            pulse = sine(self.distant_realms.system.time.get_current_time())
            fade_color = (
                int(50 * pulse), 
                int(50 * pulse), 
                int(50 * pulse)
            )
            self.distant_realms.system.window.fill((fade_color))
            self.clean_up_states()


            if self.ProjectBrowser:
                self.ProjectBrowser.update()

            self.util.display_volume(self.distant_realms.ui_controller.get_active_ui())

        else:
            if self.editor:
                self.editor.update()

    def draw(self):
        
        if self.editor:
            self.editor.draw()

        if self.ProjectBrowser:
            self.ProjectBrowser.draw()

    def scale(self):
        pass

    def clean_up_states(self):
        self.distant_realms.system.app_inspector.clear()
        self.distant_realms.system.clean_up_states([self.state.state])

    def register_debug_telemetry(self):
        # exmaple:
        # self.system.app_inspector["seed"] = self.world.seed
        pass

    def reset(self):
        pass

    def init(self):
        self.distant_realms.ui_controller.show_ui("editor_main_menu")

    def initialize_ui_project_browser(self):
        import importlib
        from application.Editor import uiprojectbrowser
        importlib.reload(uiprojectbrowser)
        self.ProjectBrowser = uiprojectbrowser.UIProjectBrowser(self)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("editor_project_browser")

    def initialize_cellmap_project_browser(self):
        import importlib
        from application.Editor import cellmapprojectbrowser
        importlib.reload(cellmapprojectbrowser)
        self.ProjectBrowser = cellmapprojectbrowser.CellMapProjectBrowser(self)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("editor_project_browser")

    def initialize_world_project_browser(self):
        import importlib
        from application.Editor import worldprojectbrowser
        importlib.reload(worldprojectbrowser)
        self.ProjectBrowser = worldprojectbrowser.WorldProjectBrowser(self)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("editor_project_browser")

    def initialize_menu_editor(self):
        import importlib
        from application.Editor.Menu import menueditor
        importlib.reload(menueditor)
        self.editor = menueditor.MenuEditor(self.distant_realms)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("editor_noprops")

    def initialize_form_editor(self):
        import importlib
        from application.Editor.Form import formeditor
        importlib.reload(formeditor)
        self.editor = formeditor.FormEditor(self.distant_realms)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("form_editor_noprops")

    def initialize_cellmap_editor(self):
        import importlib
        from application.Editor import cellmap_editor
        importlib.reload(cellmap_editor)
        self.editor = cellmap_editor.CMEditor(self.distant_realms)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("cell_map_editor_layout")

    def initialize_world_editor(self):
        import importlib
        from application.Editor import worldeditor
        importlib.reload(worldeditor)
        self.editor = worldeditor.WorldEditor(self.distant_realms)
        self.distant_realms.ui_controller.clear()
        self.distant_realms.ui_controller.show_ui("world_editor_layout")