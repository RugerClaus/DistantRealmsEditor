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

        self.scroll_offset = 0
        self.row_height = 50
        self.scroll_speed = 40
        self.label = Label(self.dr.system,"map_selector_label","Cellmap Layers:",(0.85,0.53),color=black)

        self.create_viewport()

    def create_viewport(self):

        ww = self.dr.system.window.get_width()
        wh = self.dr.system.window.get_height()

        self.viewport_rect = self.dr.system.window.Rect(
            int(ww * 0.8),
            int(wh * 0.55),
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

            self.buttons.append(button)

        self.update_button_positions()

    def select_map(self, map):

        self.editor.selected_map = map

        print(
            "SELECTED MAP:",
            map.name
        )

    def update_button_positions(self):

        if not self.buttons:
            return

        # left_padding = self.viewport_rect.width - self.viewport_rect.width+50
        top_padding = self.buttons[0].surface.get_height() // 2

        for index, button in enumerate(self.buttons):

            y = (
                top_padding
                + index * self.row_height
                - self.scroll_offset
            )

            button.rect = button.surface.get_rect(
                center=(self.viewport_rect.width / 2, y)
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

        viewport_rect = self.viewport.get_rect()

        return viewport_rect.colliderect(
            button.rect
        )

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

        self.label.update()

    def draw(self):

        self.viewport.fill((0,0,0,0))

        for button in self.buttons:

            if self.button_visible(button):
                button.draw(self.viewport)

        self.dr.system.window.blit(
            self.viewport,
            self.viewport_rect
        )
        self.label.draw()