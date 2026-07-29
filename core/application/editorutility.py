import json
from pathlib import Path


class EditorUtility:
    def __init__(self,app_interface):
        self.app_interface = app_interface

    def create_project_file(self, data):
        
        project_name = data["name"].strip().upper()
        project_type = data["project_type"]
        print("creating project: ",project_name,"of type: ",project_type)
        if project_type == "Menu":
            directory = Path("core/application/enginepersistence/menus")

        elif project_type == "Form":
            directory = Path("core/application/enginepersistence/forms")

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

        return filename

    def create_project(self):
            form = self.app_interface.ui_controller.get_active_ui()
    
            data = {
                "name": form.get_field("name").get_return_string(),
                "project_type": form.get_field("project_type").get_return_string()
            }

            print("FORM DATA:", data)

            if not data["name"]:
                form.set_error("Project name is required.")
                return
    
            self.create_project_file(data)
    