import json
from pathlib import Path
from systemlogging import log_warning

from core.util.colors import red

from core.ui.widgets.button import Button


class UIProjectBrowser:

    def __init__(self, application):

        self.application = application
        self.dr = application.distant_realms

        self.files = []
        self.buttons = []
        self.delete_buttons = []

        self.scroll_offset = 0
        self.row_height = 70
        self.scroll_speed = 40

        self.create_viewport()

        self.get_project_dirs()

        log_warning(f"ProjectBrowser: files = {self.files}")

        self.create_buttons()


    def create_viewport(self):
        ww = self.dr.system.window.get_width()
        wh = self.dr.system.window.get_height()

        self.viewport_rect = self.dr.system.window.Rect(
            int(ww * 0.35),
            int(wh * 0.2),
            int(ww * 0.5),
            int(wh * 0.6)
        )

        self.viewport = self.dr.system.window.make_surface(
            self.viewport_rect.width,
            self.viewport_rect.height,
            True
        )

    def get_project_dirs(self):
        dirs = [
            self.dr.system.persistence.workspace_forms,
            self.dr.system.persistence.workspace_menus
        ]

        for directory in dirs:
            directory = Path(directory)

            if not directory.exists():
                log_warning(f"Missing project directory: {directory}")
                continue

            for path in directory.iterdir():

                if not path.is_file() or path.suffix.lower() != ".json":
                    continue

                try:
                    with path.open("r", encoding="utf-8") as file:
                        data = json.load(file)
                except (OSError, json.JSONDecodeError) as e:
                    log_warning(f"Skipping {path}: {e}")
                    continue

                project_type = data.get("type")

                if project_type not in ("menu", "form"):
                    continue

                self.files.append({
                    "name": path.stem,
                    "type": project_type
                })

    def create_buttons(self):
        for index, project in enumerate(self.files):

            button = Button(
                self.dr.system,
                f"project_{index}",
                project["name"],
                (0.5, 0.5),
                font_size=20,
                action=lambda p=project: self.application.util.load_project(
                    p["name"],
                    p["type"]
                )
            )

            delete_button = Button(
                self.dr.system,
                f"delete_project_{index}",
                "DELETE",
                (0.5, 0.5),
                font_size=20,
                action=lambda p=project: self.delete_project(p["name"]),
                styles={
                    "idle": {
                        "text_color": red
                    }
                }
            )

            self.buttons.append(button)
            self.delete_buttons.append(delete_button)

        self.update_button_positions()


    def delete_project(self, name):
        self.application.util.delete_project(name)
        self.refresh()


    def refresh(self):
        old_scroll_offset = self.scroll_offset

        self.files.clear()
        self.buttons.clear()
        self.delete_buttons.clear()

        self.get_project_dirs()
        self.create_buttons()

        self.scroll_offset = max(
            0,
            min(
                old_scroll_offset,
                self.max_scroll()
            )
        )
        
        self.update_button_positions()

    def update_button_positions(self):
        if not self.buttons:
            return

        left_padding = 20
        button_gap = 10
        top_padding = self.buttons[0].surface.get_height() // 2

        for index, button in enumerate(self.buttons):

            y = (
                top_padding
                + index * self.row_height
                - self.scroll_offset
            )

            button.rect = button.surface.get_rect(
                midleft=(left_padding, y)
            )

            delete_button = self.delete_buttons[index]

            delete_button.rect = delete_button.surface.get_rect(
                midleft=(
                    button.rect.right + button_gap,
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
                min(
                    self.max_scroll(),
                    self.scroll_offset
                )
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

        if self.viewport_rect.collidepoint(mx, my):

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

        self.draw_scrollbar()

    def draw_scrollbar(self):
        if self.max_scroll() <= 0:
            return

        x = self.viewport_rect.right + 10

        track = self.dr.system.window.Rect(
            x,
            self.viewport_rect.top,
            12,
            self.viewport_rect.height
        )

        self.dr.system.window.draw_rect(
            self.dr.system.window,
            (80, 80, 80),
            track
        )

        ratio = (
            self.viewport_rect.height
            / (len(self.buttons) * self.row_height)
        )

        thumb_height = max(
            30,
            int(self.viewport_rect.height * ratio)
        )

        scroll_ratio = (
            self.scroll_offset
            / self.max_scroll()
        )

        thumb_y = (
            self.viewport_rect.top
            + int(
                (self.viewport_rect.height - thumb_height)
                * scroll_ratio
            )
        )

        thumb = self.dr.system.window.Rect(
            x,
            thumb_y,
            12,
            thumb_height
        )

        self.dr.system.window.draw_rect(
            self.dr.system.window,
            (200, 200, 200),
            thumb
        )

