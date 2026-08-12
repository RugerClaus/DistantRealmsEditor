import json
from systemlogging import log_event

from core.state.ApplicationLayer.Editor.state import EDITOR_STATE


class EditorUtility:
    def __init__(self, distant_realms):
        self.distant_realms = distant_realms

    def create_project_file(self, data):
        project_name = data["name"].strip().upper()
        project_type = data["project_type"]

        log_event(f"Creating project: {project_name}, of type: {project_type}" , "EditorUtility.create_project_file")

        persistence = self.distant_realms.system.persistence

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

        if self.distant_realms.application:
            if project_type == "Menu":
                self.distant_realms.application.state.set_state(EDITOR_STATE.MENU)
                self.distant_realms.ui_controller.clear()
                self.distant_realms.ui_controller.show_ui("editor_noprops")
            else:
                self.distant_realms.application.state.set_state(EDITOR_STATE.FORM)
                self.distant_realms.ui_controller.clear()
                self.distant_realms.ui_controller.show_ui("form_editor_noprops")

        self.distant_realms.application.editor.active_file = self.load_project_file(filename)

    def create_project(self):
        form = self.distant_realms.ui_controller.get_active_ui()

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
            self.distant_realms.application.initialize_menu_editor()
            self.distant_realms.application.state.set_state(EDITOR_STATE.MENU)
        elif project_type == "form":
            self.distant_realms.application.initialize_form_editor()
            self.distant_realms.application.state.set_state(EDITOR_STATE.FORM)
        else:
            log_event(
                f"Unknown project type in file: {project_type}",
                "EditorUtility.load_project_file"
            )
            return False

        editor = self.distant_realms.application.editor

        editor.active_filename = filename
        editor.active_file = data

        log_event(
            f"Loaded project file: {filename.resolve()}",
            "EditorUtility.load_project_file"
        )

        return data

    def load_project(self, filename, project_type="menu"):
            persistence = self.distant_realms.system.persistence
    
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
                self.distant_realms.application.initialize_menu_editor()
                self.distant_realms.application.state.set_state(EDITOR_STATE.MENU)
                self.distant_realms.ui_controller.clear()
            elif file_type == "form":
                self.distant_realms.application.initialize_form_editor()
                self.distant_realms.application.state.set_state(EDITOR_STATE.FORM)
                self.distant_realms.ui_controller.clear()
            else:
                log_event(
                    f"Unknown project type in file: {file_type}",
                    "EditorUtility.load_project_file"
                )
                return False
    
            editor = self.distant_realms.application.editor
    
            editor.active_filename = path
            editor.active_file = data
            editor.load_canvas()
    
            log_event(
                f"Loaded project file: {path.resolve()}",
                "EditorUtility.load_project_file"
            )

            browser = self.distant_realms.application.ProjectBrowser

            if browser:
                self.distant_realms.application.ProjectBrowser = None

            if self.distant_realms.application.state.is_state(EDITOR_STATE.MENU):
                self.distant_realms.ui_controller.show_ui("editor_noprops")
            elif self.distant_realms.application.state.is_state(EDITOR_STATE.FORM):
                self.distant_realms.ui_controller.show_ui("form_editor_noprops")
    
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

    def display_volume(self,ui):
        

        if self.distant_realms.ui_controller.active_name == "editor_audio_settings":

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
            log_event(
                "Cannot delete project: empty name",
                "EditorUtility.delete_project"
            )
            return False

        persistence = self.distant_realms.system.persistence

        directories = [
            persistence.workspace_forms,
            persistence.workspace_menus
        ]

        deleted = False

        for directory in directories:
            directory = directory

            filename = directory / f"{project_name}.json"

            if not filename.exists():
                continue

            try:
                filename.unlink()

                log_event(
                    f"Deleted project: {filename.resolve()}",
                    "EditorUtility.delete_project"
                )

                deleted = True
                break

            except OSError as e:
                log_event(
                    f"Failed to delete project {filename}: {e}",
                    "EditorUtility.delete_project"
                )
                return False

        if not deleted:
            log_event(
                f"Project not found: {project_name}",
                "EditorUtility.delete_project"
            )
            return False

        browser = self.distant_realms.application.ProjectBrowser

        if browser is not None:
            browser.refresh()

        return True
