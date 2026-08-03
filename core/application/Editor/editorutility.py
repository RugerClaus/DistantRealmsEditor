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
            else:
                self.app_interface.app_object.state.set_state(EDITOR_STATE.FORM)

        return filename

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