from pathlib import Path

from systemlogging import log_event

from core.guts.persistence.save import Save
from core.guts.persistence.load import Load
from core.state.RuntimeLayer.DevTools.DeveloperMode.state import DEVELOPER_MODE

class Persistence:
    def __init__(self, system, project_root=None, engine_root="enginepersistence"):
        self.system = system

        self.engine_root = Path(engine_root)
        self.project_root = Path(project_root) if project_root else None

        self.engine_menus = self.engine_root / "menus"
        self.engine_forms = self.engine_root / "forms"

        self.project_engine_root = self.project_root / "enginepersistence" if self.project_root else None

        self.project_menus = self.project_engine_root / "menus" if self.project_engine_root else None
        self.project_forms = self.project_engine_root / "forms" if self.project_engine_root else None

        self.save = Save()
        self.load = Load()

    def developer_mode(self):
        return self.system.control_state.is_state(DEVELOPER_MODE.ON)

    def can_edit_engine_ui(self):
        return self.developer_mode()

    def get_menu(self, name):
        filename = f"{name.upper()}.json"

        if self.project_menus:
            path = self.project_menus / filename
            log_event("Checking project engine menu:", path.resolve())
            if path.exists():
                log_event("Found project engine menu")
                return path

        path = self.engine_menus / filename
        log_event("Checking engine menu:", path.resolve())
        log_event("Exists:", path.exists())
        return path

    def get_form(self, name):
        filename = f"{name.upper()}.json"

        if self.project_forms:
            path = self.project_forms / filename
            if path.exists():
                return path

        return self.engine_forms / filename

    def save_engine_ui(self, path, data):
        if not self.can_edit_engine_ui():
            log_event("Blocked engine UI write: developer mode disabled")
            return False

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        import json
        with open(path, "w") as file:
            json.dump(data, file, indent=4)

        log_event("Saved engine UI:", path)
        return True