from core.util.colors import *
from core.ui.widgets.button import Button
from core.ui.widgets.label import Label

class MapSelector:

    def __init__(self, application, editor):
        self.application = application
        self.editor = editor
        self.dr = application.distant_realms
        self.maps = []
        self.buttons = []
        self.delete_buttons = []
        self.scroll_offset = 0
        self.row_height = 50
        self.scroll_speed = 40
        self.label = Label(
            self.dr.system,
            "map_selector_label",
            "Cellmap Layers:",
            (0.85, 0.55),
            color=black
        )
        self.create_viewport()

    def scale(self):
        self.create_viewport()
        self.label.scale()
        for button in self.buttons:
            button.scale()
        for button in self.delete_buttons:
            button.scale()
        self.update_button_positions()

    def create_viewport(self):
        ww = self.dr.system.window.get_width()
        wh = self.dr.system.window.get_height()
        self.viewport_rect = self.dr.system.window.Rect(
            int(ww * 0.8),
            int(wh * 0.58),
            int(ww * 0.15),
            int(wh * 0.4)
        )
        self.viewport = self.dr.system.window.make_surface(
            self.viewport_rect.width,
            self.viewport_rect.height,
            True
        )

    def set_maps(self, maps):
        self.maps = list(maps)
        self.buttons.clear()
        self.delete_buttons.clear()
        self.scroll_offset = 0
        self.create_buttons()

    def create_buttons(self):
        for index, map in enumerate(self.maps):
            button = Button(
                self.dr.system,
                f"map_{index}",
                map.name,
                (0.5, 0.5),
                font_size=30,
                action=lambda m=map: self.select_map(m)
            )
            delete_button = Button(
                self.dr.system,
                f"delete_map_{index}",
                "Delete",
                (0.5, 0.5),
                font_size=24,
                action=lambda m=map: self.delete_map(m),
                styles={
                    "idle": {
                        "text_color": red
                    }
                }
            )
            self.buttons.append(button)
            self.delete_buttons.append(delete_button)
        self.update_button_positions()

    def select_map(self, map):
        self.editor.selected_map = map
        self.editor.select_map_layer(map)

    def delete_map(self, map):
        world_editor = self.editor

        if world_editor.active_file is None:
            return

        if world_editor.active_filename is None:
            return

        map_filename = getattr(map, "name", None)

        if not map_filename:
            map_filename = getattr(map, "file", None)

        if not map_filename:
            print("MAP SELECTOR ERROR: Map has no filename.")
            return

        if not map_filename.endswith(".map"):
            map_filename += ".map"

        world_directory = self.dr.system.os.path.dirname(
            world_editor.active_filename
        )

        map_path = self.dr.system.os.path.join(
            world_directory,
            map_filename
        )

        maps = world_editor.active_file.get("maps", [])
        remaining_maps = []

        for world_map in maps:
            if world_map.get("file") != map_filename:
                remaining_maps.append(world_map)

        world_editor.active_file["maps"] = remaining_maps

        try:
            if self.dr.system.os.path.exists(map_path):
                self.dr.system.os.remove(map_path)

            self.dr.application.util.save_project_file(
                world_editor.active_filename,
                world_editor.active_file
            )
            world_editor.map_deleted(map)

        except OSError as exception:
            print(
                "MAP SELECTOR ERROR:",
                f"Could not delete map: {exception}"
            )
            return

        if world_editor.selected_map is map:
            world_editor.selected_map = None
            world_editor.selected_cell = 0
            world_editor.cell_position = None

        world_editor.load_world()

        self.maps = [
            existing_map
            for existing_map in self.maps
            if existing_map is not map
        ]

        self.buttons.clear()
        self.delete_buttons.clear()
        self.create_buttons()

        print("MAP DELETED:", map_path)

    def update_button_positions(self):
        if not self.buttons:
            return

        button_height = self.buttons[0].surface.get_height()
        top_padding = button_height // 2

        for index, button in enumerate(self.buttons):
            y = (
                top_padding
                + index * self.row_height
                - self.scroll_offset
            )
            button.rect = button.surface.get_rect(
                center=(
                    self.viewport_rect.width * 0.42,
                    y
                )
            )

            delete_button = self.delete_buttons[index]
            delete_button.rect = delete_button.surface.get_rect(
                center=(
                    self.viewport_rect.width * 0.86,
                    y
                )
            )

    def max_scroll(self):
        if not self.buttons:
            return 0

        button_height = self.buttons[0].surface.get_height()
        top_padding = button_height // 2
        content_height = (
            top_padding
            + (len(self.buttons) - 1) * self.row_height
            + top_padding
        )

        return max(
            0,
            content_height - self.viewport_rect.height
        )

    def button_visible(self, button):
        return self.viewport.get_rect().colliderect(button.rect)

    def handle_event(self, event, command):
        if event.type == self.dr.system.input.mouse_scroll_event():
            self.scroll_offset -= event.y * self.scroll_speed
            self.scroll_offset = max(
                0,
                min(self.max_scroll(), self.scroll_offset)
            )
            self.update_button_positions()

        if (
            event.type == self.dr.system.input.mouse_button_down()
            and event.button == 1
        ):
            mx, my = self.dr.system.input.get_mouse_pos()

            if self.viewport_rect.collidepoint(mx, my):
                local_mouse = (
                    mx - self.viewport_rect.x,
                    my - self.viewport_rect.y
                )

                for button in self.buttons:
                    if (
                        self.button_visible(button)
                        and button.is_clicked(local_mouse, True)
                    ):
                        break

                for button in self.delete_buttons:
                    if (
                        self.button_visible(button)
                        and button.is_clicked(local_mouse, True)
                    ):
                        break

    def update(self):
        mx, my = self.dr.system.input.get_mouse_pos()

        if not self.viewport_rect.collidepoint(mx, my):
            return

        local_mouse = (
            mx - self.viewport_rect.x,
            my - self.viewport_rect.y
        )

        for button in self.buttons:
            if self.button_visible(button):
                button.update(local_mouse)

        for button in self.delete_buttons:
            if self.button_visible(button):
                button.update(local_mouse)

        self.label.update()

    def draw(self):
        self.viewport.fill((0, 0, 0, 0))

        for button in self.buttons:
            if self.button_visible(button):
                button.draw(self.viewport)

        for button in self.delete_buttons:
            if self.button_visible(button):
                button.draw(self.viewport)

        self.dr.system.window.blit(
            self.viewport,
            self.viewport_rect
        )

        self.label.draw()