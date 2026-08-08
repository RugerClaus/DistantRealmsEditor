from core.ui.font import FontEngine
from core.application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorLabel(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.text = str(data.get("text", "Label"))
        self.font_size = data.get("font_size", 30)
        self.color = tuple(
            data.get("color", [255, 255, 255])
        )

        self.font = FontEngine(self.font_size).font

        self.scale()

    def set_color(self, color):
        self.color = tuple(color)
        self.data["color"] = list(color)

        self.scale()

    def scale(self):
        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()
        self.font = FontEngine(self.font_size).font

        x = int(ww * self.position[0])
        y = int(wh * self.position[1])

        self.surface = self.font.render(
            self.text,
            False,
            self.color
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):
        self.system.window.blit(
            self.surface,
            self.rect
        )