from core.ui.font import FontEngine
from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE


class EditorButton:
    def __init__(self, editor, data):
        self.editor = editor
        self.system = editor.app_interface.system

        self.data = data

        # These are deliberately exposed.
        self.id = data.get("id", "button")
        self.text = data.get("text", "")
        self.font_size = data.get("font_size", 30)
        self.position = tuple(data.get("position", [0.5, 0.5]))
        self.action = data.get("action")

        self.state = BUTTON_STATE.IDLE

        self.styles = {
            BUTTON_STATE.IDLE: {
                "background": (40, 40, 40),
                "border": (255, 255, 255),
                "border_width": 2,
                "border_radius": 8,
                "text_color": (255, 255, 255),
                "padding": 5,
            },

            BUTTON_STATE.HOVER: {
                "background": (60, 60, 60),
                "border": (200, 20, 20),
                "border_width": 3,
                "border_radius": 8,
                "text_color": (255, 255, 255),
                "padding": 5,
            },

            BUTTON_STATE.PRESS: {
                "background": (20, 20, 20),
                "border": (255, 255, 255),
                "border_width": 2,
                "border_radius": 8,
                "text_color": (255, 255, 255),
                "padding": 5,
            },

            BUTTON_STATE.DISABLE: {
                "background": (20, 20, 20),
                "border": (100, 100, 100),
                "border_width": 2,
                "border_radius": 8,
                "text_color": (100, 100, 100),
                "padding": 5,
            },

            BUTTON_STATE.FOCUSED: {
                "background": (40, 40, 40),
                "border": (0, 255, 255),
                "border_width": 3,
                "border_radius": 8,
                "text_color": (255, 255, 255),
                "padding": 5,
            }
        }

        self.scale()

    def scale(self):
        style = self.styles[self.state]

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
        style = self.styles[self.state]

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

        self.surface.blit(
            self.text_surface,
            self.text_rect
        )

        self.system.window.blit(
            self.surface,
            self.rect
        )

    def contains_point(self, point):
        return self.rect.collidepoint(point)

    def set_state(self, state):
        if self.state != state:
            self.state = state
            self.scale()

    def set_action(self, action):
        self.data["action"] = action

    def set_text(self, text):
        self.text = str(text)
        self.data["text"] = self.text
        self.scale()

    def set_position(self, position):
        self.data["position"] = list(position)
        self.position = tuple(position)

        self.x_ratio, self.y_ratio = position
        self.scale()

    def set_id(self, element_id):
        self.id = element_id
        self.data["id"] = element_id