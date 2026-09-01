from core.util.colors import *
from core.ui.uicontroller import UIController
from core.ui.type import COMPOSABLE

class MapProperties:

    def __init__(self, distant_realms, world_editor):
        self.distant_realms = distant_realms
        self.world_editor = world_editor
        self.system = distant_realms.system
        self.ui_controller = UIController(self.system, self.distant_realms.ui)
        self.visible = False
        self.surface = None
        self.rect = None
        self.scale()

    def show(self):
        selected_map = self.world_editor.selected_map

        if selected_map is None:
            return

        if self.ui_controller.show_ui("map_properties_form"):
            self.ui_controller.scale()

        self.load_map_properties()
        self.visible = True
        self.scale()

    def hide(self):
        self.ui_controller.clear()
        self.visible = False

    def load_map_properties(self):
        selected_map = self.world_editor.selected_map

        if selected_map is None:
            return

        world = self.world_editor.active_file

        if world is None:
            return

        filename = getattr(selected_map, "filename", None)

        if filename is None:
            return

        world_map = None

        for map_data in world.get("maps", []):
            if map_data.get("file") == filename:
                world_map = map_data
                break

        if world_map is None:
            return

        form = self.ui_controller.get_active_ui()

        if form is None:
            return

        world_directory = self.system.os.path.dirname(self.world_editor.active_filename)
        map_path = self.system.os.path.join(world_directory, filename)
        map_width = 0
        map_height = 0

        try:
            with open(map_path, "r") as map_file:
                rows = [line.strip() for line in map_file if line.strip()]

            map_height = len(rows)

            if rows:
                map_width = len(rows[0].split(","))

        except (OSError, ValueError):
            map_width = world_map.get("width", 0)
            map_height = world_map.get("height", 0)

        velocity = world_map.get("velocity", [0, 0])

        if not isinstance(velocity, (list, tuple)) or len(velocity) < 2:
            velocity = [0, 0]

        values = {
            "filename": str(world_map.get("file", "")),
            "dimensions": f"{map_width}x{map_height}",
            "layer_z_position": world_map.get("z", 0),
            "world_x": world_map.get("world_x", 0),
            "world_y": world_map.get("world_y", 0),
            "velocity_x": velocity[0],
            "velocity_y": velocity[1],
            "camera_follow_x": world_map.get("camera_follow_x", True),
            "camera_follow_y": world_map.get("camera_follow_y", True),
            "wrap_x": world_map.get("wrap_x", True),
            "wrap_y": world_map.get("wrap_y", True)
        }

        if hasattr(form, "set_values"):
            form.set_values(values)

    def handle_event(self, event, command):
        if not self.visible:
            return

        self.ui_controller.handle_event(event)

        if event.type == self.system.input.keydown():
            if event.key == self.system.input.keys.return_key():
                self.submit()

            if event.key == self.system.input.keys.escape_key():
                self.hide()

    def update(self):
        if not self.visible:
            return

        self.ui_controller.update()

    def scale(self):
        width = self.world_editor.canvas_rect.width
        height = int(self.system.window.get_height() * 0.99)

        self.surface = self.system.window.make_surface(width, height)
        self.rect = self.surface.get_rect(
            topleft=(
                self.world_editor.canvas_rect.left,
                self.world_editor.coordinate_display_rect.bottom
            )
        )

        ui = self.ui_controller.get_active_ui()
        if ui:
            for element in ui.children:
                if element.type == "select":
                    element.set_padding(1)

        # if elements:
        #     for element in elements:
        #         if element.type == "select":
        #             element.set_padding(1)

        self.ui_controller.scale()


    def draw(self):
        if not self.visible:
            return

        self.surface.fill(dark_gray)
        self.system.window.blit(self.surface, self.rect)
        self.ui_controller.draw()


    def submit(self):
        if not self.visible:
            return None

        form = self.ui_controller.get_active_ui()

        if form is None:
            return None

        if not hasattr(form, "submit"):
            return None

        world_editor = self.world_editor

        if world_editor.active_file is None:
            return None

        if world_editor.active_filename is None:
            return None

        if world_editor.selected_map is None:
            return None

        world = world_editor.active_file
        values = form.submit()

        def error(message):
            if hasattr(form, "set_error"):
                form.set_error(message)

            print("MAP PROPERTIES ERROR:", message)

        def parse_int(value, name):
            try:
                return int(str(value).strip())
            except (TypeError, ValueError):
                error(f"{name} must be an integer.")
                return None

        def parse_float(value, name):
            try:
                return float(str(value).strip())
            except (TypeError, ValueError):
                error(f"{name} must be a number.")
                return None

        def parse_bool(value, name, default):
            if isinstance(value, bool):
                return value

            if value is None:
                return default

            if isinstance(value, str):
                value = value.strip().lower()

                if value == "true":
                    return True

                if value == "false":
                    return False

            error(f"{name} must be True or False.")
            return None

        z = parse_int(values.get("layer_z_position", 0), "Z index")

        if z is None:
            return None

        world_x = parse_int(values.get("world_x", 0), "World X")

        if world_x is None:
            return None

        world_y = parse_int(values.get("world_y", 0), "World Y")

        if world_y is None:
            return None

        velocity_x = parse_float(values.get("velocity_x", 0), "Velocity X")

        if velocity_x is None:
            return None

        velocity_y = parse_float(values.get("velocity_y", 0), "Velocity Y")

        if velocity_y is None:
            return None

        camera_follow_x = parse_bool(
            values.get("camera_follow_x"),
            "Camera Follow X",
            True
        )

        if camera_follow_x is None:
            return None

        camera_follow_y = parse_bool(
            values.get("camera_follow_y"),
            "Camera Follow Y",
            True
        )

        if camera_follow_y is None:
            return None

        wrap_x = parse_bool(
            values.get("wrap_x"),
            "Wrap X",
            True
        )

        if wrap_x is None:
            return None

        wrap_y = parse_bool(
            values.get("wrap_y"),
            "Wrap Y",
            True
        )

        if wrap_y is None:
            return None

        filename = getattr(world_editor.selected_map, "filename", None)

        if filename is None:
            error("Selected map has no filename.")
            return None

        world_map = None

        for map_data in world.get("maps", []):
            if map_data.get("file") == filename:
                world_map = map_data
                break

        if world_map is None:
            error("Could not find selected map in world.")
            return None

        world_map["z"] = z
        world_map["velocity"] = [velocity_x, velocity_y]
        world_map["camera_follow_x"] = camera_follow_x
        world_map["camera_follow_y"] = camera_follow_y
        world_map["wrap_x"] = wrap_x
        world_map["wrap_y"] = wrap_y
        world_map["world_x"] = world_x
        world_map["world_y"] = world_y

        try:
            self.distant_realms.application.util.save_project_file(
                world_editor.active_filename,
                world
            )
        except OSError as exception:
            error(f"Could not save world: {exception}")
            return None

        world_editor.dirty = False
        world_editor.reload_selected_map(filename)

        print("MAP PROPERTIES UPDATED:", filename)

        return world_map