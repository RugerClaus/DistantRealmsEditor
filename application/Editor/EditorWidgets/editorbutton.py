from core.ui.font import FontEngine
from application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorButton(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        if not self.data.get("styles"):
            self.data["styles"] = self.editor.widgets.default_button_styles()

        self.text = data.get("text", "")
        self.action = data.get("action")
        self.color = None

        self.styles = self.editor.widgets.default_button_styles()

        self.load_styles()

        self.scale()

    def load_styles(self):
        saved_styles = self.data.get("styles", {})

        for state_name, values in saved_styles.items():
            if state_name not in self.styles:
                continue

            for key, value in values.items():
                if key in ("background", "border", "text_color"):
                    value = tuple(value)

                self.styles[state_name][key] = value

    def get_current_style(self):
        state_name = self.editor.button_style_state.state.name.lower()
        return state_name, self.styles[state_name]

    def scale(self, state_name=None):
        if state_name is None:
            state_name, style = self.get_current_style()
        else:
            style = self.styles[state_name]

        self.font = FontEngine(self.font_size).font

        self.text_surface = self.font.render(
            str(self.text),
            True,
            style["text_color"]
        )

        self.width = (
            self.text_surface.get_width()
            + style["padding"] * 2
        )

        self.height = (
            self.text_surface.get_height()
            + style["padding"] * 2
        )

        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()

        x = int(ww * self.position[0])
        y = int(wh * self.position[1])

        self.surface = self.system.window.make_surface(
            self.width,
            self.height,
            True
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

        self.text_rect = self.text_surface.get_rect(
            center=self.surface.get_rect().center
        )

    def draw(self):
        _, style = self.get_current_style()

        self.surface.fill((0, 0, 0, 0))

        self.system.window.draw_rect(
            self.surface,
            style["background"],
            self.surface.get_rect(),
            border_radius=style["border_radius"]
        )

        if style["border_width"]:
            self.system.window.draw_rect(
                self.surface,
                style["border"],
                self.surface.get_rect(),
                width=style["border_width"],
                border_radius=style["border_radius"]
            )

        text_surface = self.font.render(
            str(self.text),
            True,
            style["text_color"]
        )

        text_rect = text_surface.get_rect(
            center=self.surface.get_rect().center
        )

        self.surface.blit(text_surface, text_rect)

        self.system.window.blit(
            self.surface,
            self.rect
        )


    def set_action(self, action):
        self.action = action
        self.data["action"] = action

    def set_style(self, state_name, key, value):
        self.styles[state_name][key] = value

        self.data.setdefault("styles", {})
        self.data["styles"].setdefault(state_name, {})

        self.data["styles"][state_name][key] = value

        self.scale()

    def set_color(self):
        pass