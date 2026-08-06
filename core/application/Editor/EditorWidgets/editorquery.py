from core.ui.font import FontEngine
from core.util.colors import white
from core.application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorQuery(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.text = str(
            data.get("text", "Query")
        )

        self.font_size = data.get(
            "font_size",
            40
        )

        self.color = tuple(
            data.get(
                "color",
                white
            )
        )

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()

    def set_text(self, text):
        self.text = str(text)
        self.data["text"] = self.text

        self.scale()

    def set_font_size(self, font_size):
        self.font_size = int(font_size)
        self.data["font_size"] = self.font_size

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()

    def set_color(self, color):
        self.color = tuple(color)
        self.data["color"] = list(color)

        self.scale()

    def scale(self):
        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()

        x = int(
            ww * self.position[0]
        )

        y = int(
            wh * self.position[1]
        )

        self.surface = self.font.render(
            self.text,
            False,
            self.color
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):

        if self.text is None:
            return

        self.system.window.blit(
            self.surface,
            self.rect
        )