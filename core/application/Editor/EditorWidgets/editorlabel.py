from core.ui.font import FontEngine

class EditorLabel:
    def __init__(self, editor, data):
        self.editor = editor
        self.system = editor.app_interface.system

        self.data = data

        self.id = data["id"]
        self.text = str(data.get("text", "Label"))
        self.font_size = data.get("font_size", 30)
        self.color = tuple(data.get("color", (255, 255, 255)))

        self.position = tuple(data.get("position", [0.5, 0.5]))
        self.x_ratio, self.y_ratio = self.position

        self.font = FontEngine(self.font_size).font

        self.rect = None

        self.scale()

    def set_position(self, position):
        self.position = tuple(position)
        self.x_ratio, self.y_ratio = self.position

        self.data["position"] = list(position)

        self.scale()

    def set_text(self, text):
        self.text = str(text)
        self.data["text"] = self.text

        self.scale()

    def set_font_size(self, font_size):
        self.font_size = int(font_size)
        self.data["font_size"] = self.font_size

        self.font = FontEngine(self.font_size).font
        self.scale()

    def set_color(self, color):
        self.color = tuple(color)
        self.data["color"] = list(color)

        self.scale()

    def scale(self):
        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()

        x = int(ww * self.x_ratio)
        y = int(wh * self.y_ratio)

        self.rect = self.font.render(
            self.text,
            False,
            self.color
        ).get_rect(center=(x, y))

    def contains_point(self, position):
        return self.rect.collidepoint(position)

    def draw(self):
        surf = self.font.render(
            self.text,
            False,
            self.color
        )

        rect = surf.get_rect(center=self.rect.center)

        self.system.window.blit(surf, rect)