from core.util.colors import *
from core.ui.uicontroller import UIController


class MapCreator:

    def __init__(self, distant_realms, world_editor):

        self.distant_realms = distant_realms
        self.world_editor = world_editor
        self.system = distant_realms.system

        self.ui_controller = UIController(
            self.system,
            self.distant_realms.ui
        )

        self.visible = False

        self.surface = None
        self.rect = None

        self.scale()

    def scale(self):

        width = self.system.window.get_width()
        height = self.system.window.get_height()

        print(
            "SCALING MAP CREATOR",
            id(self),
            width,
            height
        )

        self.surface = self.system.window.make_surface(
            int(width / 3.5),
            int(height / 2)
        )

        self.rect = self.surface.get_rect(
            center=(
                width // 2,
                height // 2
            )
        )

        self.ui_controller.scale()

    def show(self):

        if self.ui_controller.show_ui("map_creator_form"):
            self.ui_controller.scale()

        self.visible = True

    def hide(self):

        self.ui_controller.clear()
        self.visible = False

    def handle_event(self, event, command):

        self.ui_controller.handle_event(event)

        if event.type == self.system.input.keydown():
            if event.key == self.system.input.keys.return_key():
                self.submit()

    def update(self):

        if not self.visible:
            return

        self.ui_controller.update()

    def draw(self):

        if not self.visible:
            return

        self.surface.fill(gray)

        self.system.window.blit(
            self.surface,
            self.rect
        )

        self.ui_controller.draw()

    def submit(self):

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

        world = world_editor.active_file
        values = form.submit()

        def error(message):

            if hasattr(form, "set_error"):
                form.set_error(message)

            print(
                "MAP CREATOR ERROR:",
                message
            )

        # ---------------------------------------------------------
        # Filename
        # ---------------------------------------------------------

        filename = str(
            values.get("filename", "")
        ).strip()

        if not filename:
            error("A map filename is required.")
            return None

        if "/" in filename or "\\" in filename:
            error("Map filename cannot contain a path.")
            return None

        if filename.endswith(".map"):
            map_filename = filename
        else:
            map_filename = filename + ".map"

        # ---------------------------------------------------------
        # Dimensions
        # ---------------------------------------------------------

        dimensions = str(
            values.get("dimensions", "")
        ).strip().lower()

        try:

            width, height = (
                int(value)
                for value in dimensions.split("x", 1)
            )

        except (ValueError, AttributeError):

            error("Invalid map dimensions.")
            return None

        if width <= 0 or height <= 0:

            error(
                "Map dimensions must be greater than zero."
            )

            return None

        # ---------------------------------------------------------
        # Integer fields
        # ---------------------------------------------------------

        def parse_int(value, name):

            try:

                return int(
                    str(value).strip()
                )

            except (TypeError, ValueError):

                error(
                    f"{name} must be an integer."
                )

                return None

        z = parse_int(
            values.get("layer_z_position", 0),
            "Z index"
        )

        if z is None:
            return None

        world_x = parse_int(
            values.get("world_x", 0),
            "World X"
        )

        if world_x is None:
            return None

        world_y = parse_int(
            values.get("world_y", 0),
            "World Y"
        )

        if world_y is None:
            return None

        # ---------------------------------------------------------
        # Float fields
        # ---------------------------------------------------------

        def parse_float(value, name):

            try:

                return float(
                    str(value).strip()
                )

            except (TypeError, ValueError):

                error(
                    f"{name} must be a number."
                )

                return None

        velocity_x = parse_float(
            values.get("velocity_x", 0),
            "Velocity X"
        )

        if velocity_x is None:
            return None

        velocity_y = parse_float(
            values.get("velocity_y", 0),
            "Velocity Y"
        )

        if velocity_y is None:
            return None

        # ---------------------------------------------------------
        # Boolean fields
        # ---------------------------------------------------------

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

            error(
                f"{name} must be True or False."
            )

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

        # ---------------------------------------------------------
        # Check active world maps
        # ---------------------------------------------------------

        maps = world.setdefault(
            "maps",
            []
        )

        for existing_map in maps:

            if existing_map.get("file") == map_filename:

                error(
                    f"A map named '{map_filename}' already exists."
                )

                return None

        # ---------------------------------------------------------
        # Create map data
        # ---------------------------------------------------------

        map_data = {
            "width": width,
            "height": height,
            "cells": [
                [0] * width
                for y in range(height)
            ]
        }

        # ---------------------------------------------------------
        # Create world map entry
        # ---------------------------------------------------------

        world_map = {
            "file": map_filename,
            "z": z,
            "velocity": [
                velocity_x,
                velocity_y
            ],
            "width": width,
            "height": height,
            "camera_follow_x": camera_follow_x,
            "camera_follow_y": camera_follow_y,
            "wrap_x": wrap_x,
            "wrap_y": wrap_y,
            "world_x": world_x,
            "world_y": world_y
        }

        # ---------------------------------------------------------
        # Create map file and update active world
        # ---------------------------------------------------------

        world_directory = self.system.os.path.dirname(
            world_editor.active_filename
        )

        map_path = self.system.os.path.join(
            world_directory,
            map_filename
        )

        try:

            # Write ONLY the cell grid to the .map file.
            with open(
                map_path,
                "w",
                encoding="utf-8"
            ) as file:

                for row in map_data["cells"]:

                    file.write(
                        ",".join(
                            str(cell)
                            for cell in row
                        )
                    )

                    file.write("\n")

            # Add the map reference to the active world.
            world["maps"].append(world_map)

            # Save ONLY the world JSON.
            self.distant_realms.application.util.save_project_file(
                world_editor.active_filename,
                world
            )

        except OSError as exception:

            error(
                f"Could not create map file: {exception}"
            )

            return None

        world_editor.dirty = False

        print(
            "MAP CREATED:",
            map_path
        )

        print(
            "WORLD UPDATED:",
            world_editor.active_filename
        )
        world_editor.map_created(world_map)

        self.hide()

        return world_map