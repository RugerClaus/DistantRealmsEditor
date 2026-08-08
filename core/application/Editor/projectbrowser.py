import os
import json

from core.ui.widgets.button import Button


class ProjectBrowser:

    def __init__(self, application):
        self.application = application
        self.dr = application.app_interface

        self.files = []
        self.buttons = []

        self.scroll_offset = 0
        self.row_height = 70
        self.scroll_speed = 40

        self.create_viewport()
        self.get_project_dirs()
        self.create_buttons()


    def create_viewport(self):
        ww = self.dr.system.window.get_width()
        wh = self.dr.system.window.get_height()

        self.viewport_rect = self.dr.system.window.Rect(
            int(ww * 0.35), int(wh * 0.2),
            int(ww * 0.35), int(wh * 0.6)
        )

        self.viewport = self.dr.system.window.make_surface(
            self.viewport_rect.width, self.viewport_rect.height,True
        )


    def get_project_dirs(self):
        dirs = [
            self.dr.system.persistence.workspace_forms,
            self.dr.system.persistence.workspace_menus
        ]

        for directory in dirs:
            for filename in os.listdir(directory):

                path = os.path.join(directory, filename)

                if os.path.isfile(path):
                    with open(path, "r") as file:
                        data = json.load(file)

                    self.files.append({
                        "name": os.path.splitext(filename)[0],
                        "type": data.get("type")
                    })


    def create_buttons(self):
        for index, project in enumerate(self.files):

            button = Button(
                self.dr.system,
                f"project_{index}",
                project["name"],
                (0.5,0.5),
                font_size=30,
                action=lambda p=project: self.application.util.load_project(
                    p["name"], p["type"]
                )
            )

            self.buttons.append(button)

        self.update_button_positions()


    def update_button_positions(self):
        if not self.buttons:
            return

        x = self.viewport.get_width() // 2
        top_padding = self.buttons[0].surface.get_height() // 2

        for index, button in enumerate(self.buttons):
            y = (
                top_padding
                + index * self.row_height
                - self.scroll_offset
            )

            button.rect = button.surface.get_rect(
                center=(x, y)
            )


    def max_scroll(self):
        if not self.buttons:
            return 0

        button_height = self.buttons[0].surface.get_height()
        top_padding = button_height

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


        if event.type == self.dr.system.input.mouse_button_down() and event.button == 1:

            mx, my = self.dr.system.input.get_mouse_pos()

            if self.viewport_rect.collidepoint(mx,my):

                local_mouse = (
                    mx - self.viewport_rect.x,
                    my - self.viewport_rect.y
                )

                for button in self.buttons:
                    if self.button_visible(button) and button.is_clicked(local_mouse, True):
                        break


    def update(self):
        mx, my = self.dr.system.input.get_mouse_pos()

        if self.viewport_rect.collidepoint(mx,my):

            local_mouse = (
                mx - self.viewport_rect.x,
                my - self.viewport_rect.y
            )

            for button in self.buttons:
                if self.button_visible(button):
                    button.update(local_mouse)


    def draw(self):
        self.viewport.fill((0,0,0,0))

        for button in self.buttons:
            if self.button_visible(button):
                button.draw(self.viewport)

        self.dr.system.window.blit(self.viewport, self.viewport_rect)

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
            (80,80,80),
            track
        )

        ratio = self.viewport_rect.height / (len(self.buttons) * self.row_height)

        thumb_height = max(30, int(self.viewport_rect.height * ratio))

        scroll_ratio = self.scroll_offset / self.max_scroll()

        thumb_y = self.viewport_rect.top + int(
            (self.viewport_rect.height - thumb_height) * scroll_ratio
        )

        thumb = self.dr.system.window.Rect(
            x,
            thumb_y,
            12,
            thumb_height
        )

        self.dr.system.window.draw_rect(
            self.dr.system.window,
            (200,200,200),
            thumb
        )