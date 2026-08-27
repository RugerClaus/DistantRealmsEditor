
import json
from systemlogging import log_event

from core.state.ApplicationLayer.Editor.state import EDITOR_STATE


class EditorUtility:

    def __init__(self, distant_realms):
        self.distant_realms = distant_realms

    def get_project_directory(self, project_type):
        persistence = self.distant_realms.system.persistence

        project_type = project_type.lower()

        if project_type == "menu":
            return persistence.workspace_menus

        if project_type == "form":
            return persistence.workspace_forms

        if project_type == "game world":
            return persistence.world

        if project_type == "cell map":
            return persistence.world

        raise ValueError(f"Unknown project type: {project_type}")
    
    def get_project_data(self, project_type, project_name):
        project_type = project_type.lower()

        if project_type == "menu":
            return {
                "type": "menu",
                "name": project_name,
                "elements": []
            }

        if project_type == "form":
            return {
                "type": "form",
                "name": project_name,
                "elements": []
            }

        if project_type == "game world":
            return {
                "type": "game world",
                "name": project_name,
                "maps": []
            }

        if project_type == "cell map":
            return {
                "type": "cell map",
                "name": project_name,
                "cell_map": []
            }

        raise ValueError(f"Unknown project type: {project_type}")

    def create_project_file(self, data):
        project_name = data["name"].strip().upper()
        project_type = data["project_type"]

        log_event(f"Creating project: {project_name}, of type: {project_type}","EditorUtility.create_project_file")

        directory = self.get_project_directory(project_type)

        directory.mkdir(parents=True, exist_ok=True)

        project_data = self.get_project_data(project_type, project_name)

        filename = directory / f"{project_name}.json"

        with filename.open("w") as file:
            json.dump(project_data, file, indent=4)

        log_event(f"Created: {filename.resolve()}","EditorUtility.create_project_file")

        if self.distant_realms.application:
            application = self.distant_realms.application

            if project_type == "Menu":
                application.state.set_state(EDITOR_STATE.MENU)

                self.distant_realms.ui_controller.clear()

                self.distant_realms.ui_controller.show_ui("editor_noprops")

            elif project_type == "Form":
                application.state.set_state(EDITOR_STATE.FORM)

                self.distant_realms.ui_controller.clear()

                self.distant_realms.ui_controller.show_ui("form_editor_noprops")

            elif project_type == "Game World":
                application.state.set_state(EDITOR_STATE.GAMEWORLD)

                self.distant_realms.ui_controller.clear()

                self.distant_realms.ui_controller.show_ui("world_editor_base")

            elif project_type == "Cell Map":
                application.state.set_state(EDITOR_STATE.CELLMAP)

                self.distant_realms.ui_controller.clear()

                self.distant_realms.ui_controller.show_ui("cell_map_editor_base")

            application.editor.active_file = self.load_project_file(filename)

    def create_project(self):
        form = self.distant_realms.ui_controller.get_active_ui()

        data = {
            "name": form.get_field("name").get_return_string(),
            "project_type": form.get_field("project_type").get_return_string()
        }

        log_event(f"FORM DATA:{data}", "EditorUtility.create_project")
        if not data["name"].strip():
            form.set_error("Project name is required.")

            return

        return self.create_project_file(data)

    def load_project_file(self, filename):
        if not filename.exists():
            log_event(f"File does not exist: {filename}","EditorUtility.load_project_file")

            return False

        with filename.open("r") as file:
            data = json.load(file)

        project_type = data.get("type")

        if not self.is_supported_project_type(project_type):
            log_event(f"Unknown project type in file: {project_type}","EditorUtility.load_project_file")

            return False

        self.initialize_editor_for_type(project_type)

        editor = self.distant_realms.application.editor

        editor.active_filename = filename
        editor.active_file = data

        log_event(f"Loaded project file: {filename.resolve()}","EditorUtility.load_project_file")

        return data

    def load_project(self, filename, project_type="menu"):
        persistence = self.distant_realms.system.persistence

        if project_type == "menu":
            path = persistence.get_menu(filename)

        elif project_type == "form":
            path = persistence.get_form(filename)

        elif project_type == "game world":
            path = persistence.world / f"{filename}.json"

        elif project_type == "cell map":
            path = persistence.world / f"{filename}.json"

        else:
            log_event(f"Unknown project type: {project_type}","EditorUtility.load_project")

            return False

        if not path.exists():
            log_event(f"Project file does not exist: {path}","EditorUtility.load_project")

            return False

        with path.open("r") as file:
            data = json.load(file)

        file_type = data.get("type")

        if not self.is_supported_project_type(file_type):
            log_event(f"Unknown project type in file: {file_type}","EditorUtility.load_project")

            return False

        self.initialize_editor_for_type(file_type)
        editor = self.distant_realms.application.editor

        editor.active_filename = path
        editor.active_file = data

        if hasattr(editor, "load_canvas"):
            editor.load_canvas()

        log_event(f"Loaded project file: {path.resolve()}","EditorUtility.load_project")

        browser = self.distant_realms.application.ProjectBrowser

        if browser:
            self.distant_realms.application.ProjectBrowser = None

        self.show_editor_ui(file_type)

        return data

    def is_supported_project_type(self, project_type):
        return project_type in ("menu","form","game world","cell map")

    def initialize_editor_for_type(self, project_type):
        application = self.distant_realms.application

        if project_type == "menu":
            application.initialize_menu_editor()
            application.state.set_state(EDITOR_STATE.MENU)

        elif project_type == "form":
            application.initialize_form_editor()
            application.state.set_state(EDITOR_STATE.FORM)

        elif project_type == "game world":
            application.initialize_world_editor()
            application.state.set_state(EDITOR_STATE.GAMEWORLD)

        elif project_type == "cell map":
            application.initialize_cellmap_editor()
            application.state.set_state(EDITOR_STATE.CELLMAP)

    def show_editor_ui(self, project_type):
        if project_type == "menu":
            self.distant_realms.ui_controller.show_ui("editor_noprops")

        elif project_type == "form":
            self.distant_realms.ui_controller.show_ui("form_editor_noprops")

        elif project_type == "game world":
            self.distant_realms.ui_controller.show_ui("world_editor_controls")

        elif project_type == "cell map":
            self.distant_realms.ui_controller.show_ui("cell_map_editor_controls")

    def save_project_file(self, filename, data):
        if not filename.exists():
            log_event(f"Cannot save nonexistent project file: {filename}","EditorUtility.save_project_file")

            return False

        with filename.open("w") as file:
            json.dump(data, file, indent=4)

        log_event(f"Saved project file: {filename.resolve()}","EditorUtility.save_project_file")

        return True

    def get_projects(self, project_type):
        directory = self.get_project_directory(project_type)

        directory.mkdir(parents=True, exist_ok=True)

        return [path for path in directory.glob("*.json")]

    def display_volume(self, ui):
        if self.distant_realms.ui_controller.active_name != "editor_audio_settings":
            return

        music_vol = float(self.distant_realms.system.sound.volume)
        normal_mvol = str(int(music_vol * 10))

        sfx_vol = float(self.distant_realms.system.sound.sfx_volume)
        normal_sfxvol = str(int(sfx_vol * 10))

        for child in ui.children:
            if child.id == "music_volumeV":
                child.text = normal_mvol

            if child.id == "sfx_volumeV":
                child.text = normal_sfxvol

    def delete_project(self, name):
        project_name = str(name).strip()

        if not project_name:
            log_event("Cannot delete project: empty name","EditorUtility.delete_project")

            return False

        persistence = self.distant_realms.system.persistence

        directories = [
            persistence.workspace_forms,
            persistence.workspace_menus,
            persistence.world
        ]

        deleted = False

        for directory in directories:
            filename = directory / f"{project_name}.json"

            if not filename.exists():
                continue

            try:
                filename.unlink()

                log_event(f"Deleted project: {filename.resolve()}","EditorUtility.delete_project")

                deleted = True
                break

            except OSError as e:
                log_event(f"Failed to delete project {filename}: {e}","EditorUtility.delete_project")

                return False

        if not deleted:
            log_event(f"Project not found: {project_name}","EditorUtility.delete_project")

            return False

        browser = self.distant_realms.application.ProjectBrowser

        if browser:
            browser.refresh()

        return True