import json
from systemlogging import log_event

from core.state.ApplicationLayer.Editor.state import EDITOR_STATE


class EditorUtility:
    def __init__(self, app_interface):
        self.app_interface = app_interface

    def create_project_file(self, data):
        project_name = data["name"].strip().upper()
        project_type = data["project_type"]

        log_event(f"Creating project: {project_name}, of type: {project_type}" , "EditorUtility.create_project_file")

        persistence = self.app_interface.system.persistence

        if project_type == "Menu":
            directory = persistence.workspace_menus
        elif project_type == "Form":
            directory = persistence.workspace_forms
        else:
            raise ValueError(f"Unknown project type: {project_type}")

        directory.mkdir(parents=True, exist_ok=True)

        project_data = {
            "type": project_type.lower(),
            "name": project_name,
            "elements": []
        }

        filename = directory / f"{project_name}.json"

        with filename.open("w") as file:
            json.dump(project_data, file, indent=4)

        log_event(f"Created: {filename.resolve()}", "EditorUtility.create_project_file")

        if self.app_interface.app_object:
            if project_type == "Menu":
                self.app_interface.app_object.state.set_state(EDITOR_STATE.MENU)
                self.app_interface.ui_controller.clear()
                self.app_interface.ui_controller.show_ui("editor_noprops")
            else:
                self.app_interface.app_object.state.set_state(EDITOR_STATE.FORM)
                self.app_interface.ui_controller.clear()
                self.app_interface.ui_controller.show_ui("editor_noprops")

        self.app_interface.app_object.editor.active_file = self.load_project_file(filename)

    def create_project(self):
        form = self.app_interface.ui_controller.get_active_ui()

        data = {
            "name": form.get_field("name").get_return_string(),
            "project_type": form.get_field("project_type").get_return_string()
        }

        log_event(f"FORM DATA:{data}","EditorUtility.create_project")

        if not data["name"].strip():
            form.set_error("Project name is required.")
            return

        return self.create_project_file(data)

    def load_project_file(self, filename):
        if not filename.exists():
            log_event(
                f"File does not exist: {filename}",
                "EditorUtility.load_project_file"
            )
            return False

        with filename.open("r") as file:
            data = json.load(file)

        project_type = data.get("type")

        if project_type == "menu":
            self.app_interface.app_object.initialize_menu_editor()
            self.app_interface.app_object.state.set_state(EDITOR_STATE.MENU)
        elif project_type == "form":
            self.app_interface.app_object.initialize_form_editor()
            self.app_interface.app_object.state.set_state(EDITOR_STATE.FORM)
        else:
            log_event(
                f"Unknown project type in file: {project_type}",
                "EditorUtility.load_project_file"
            )
            return False

        editor = self.app_interface.app_object.editor

        editor.active_filename = filename
        editor.active_file = data

        log_event(
            f"Loaded project file: {filename.resolve()}",
            "EditorUtility.load_project_file"
        )

        return data

    def load_project(self, filename, project_type="menu"):
            persistence = self.app_interface.system.persistence
    
            if project_type == "menu":
                path = persistence.get_menu(filename)
            elif project_type == "form":
                path = persistence.get_form(filename)
            else:
                log_event(
                    f"Unknown project type: {project_type}",
                    "EditorUtility.load_project_file"
                )
                return False
    
            if not path.exists():
                log_event(
                    f"Project file does not exist: {path}",
                    "EditorUtility.load_project_file"
                )
                return False
    
            with path.open("r") as file:
                data = json.load(file)
    
            file_type = data.get("type")
    
            if file_type == "menu":
                self.app_interface.app_object.initialize_menu_editor()
                self.app_interface.app_object.state.set_state(EDITOR_STATE.MENU)
                self.app_interface.ui_controller.clear()
            elif file_type == "form":
                self.app_interface.app_object.initialize_form_editor()
                self.app_interface.app_object.state.set_state(EDITOR_STATE.FORM)
                self.app_interface.ui_controller.clear()
            else:
                log_event(
                    f"Unknown project type in file: {file_type}",
                    "EditorUtility.load_project_file"
                )
                return False
    
            editor = self.app_interface.app_object.editor
    
            editor.active_filename = path
            editor.active_file = data
            editor.load_canvas()
    
            log_event(
                f"Loaded project file: {path.resolve()}",
                "EditorUtility.load_project_file"
            )

            browser = self.app_interface.app_object.ProjectBrowser

            if browser:
                self.app_interface.app_object.ProjectBrowser = None

            self.app_interface.ui_controller.show_ui("editor_noprops")
    
            return data

    def save_project_file(self, filename, data):
        if not filename.exists():
            log_event(
                f"Cannot save nonexistent project file: {filename}",
                "EditorUtility.save_project_file"
            )
            return False

        with filename.open("w") as file:
            json.dump(data, file, indent=4)

        log_event(
            f"Saved project file: {filename.resolve()}",
            "EditorUtility.save_project_file"
        )

        return True

    def get_projects(self,type):
        pass