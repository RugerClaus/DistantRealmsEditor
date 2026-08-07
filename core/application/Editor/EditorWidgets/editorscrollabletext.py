from core.ui.font import FontEngine
from core.application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorScrollableText(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.font_size = data.get("font_size", 40)
        self.width = data.get("width", 0.8)
        self.height = data.get("height", 0.6)

        self.align = data.get("align", "left")
        self.line_spacing = data.get("line_spacing", 0.01)

        self.max_char_count = data.get("max_char_count", 90)

        self.font = FontEngine(self.font_size).font

        self.scale()

    def set_width(self, width):
        self.width = float(width)
        self.data["width"] = self.width

        self.scale()

    def set_height(self, height):
        self.height = float(height)
        self.data["height"] = self.height

        self.scale()

    def set_align(self, align):
        self.align = align
        self.data["align"] = align
        self.scale()

    def set_line_spacing(self, spacing):
        self.line_spacing = float(spacing)
        self.data["line_spacing"] = self.line_spacing
        self.scale()

    def set_text(self, text):
        self.lines = text
        self.data["lines"] = text
        self.scroll_offset = 0

    def scale(self):
        width = int(
            self.editor.canvas.get_width()
            * self.width
        )

        height = int(
            self.editor.canvas.get_height()
            * self.height
        )

        self.surface = self.system.window.make_surface(
            width,
            height,
            True
        )

        x = int(
            self.editor.canvas.get_width()
            * self.position[0]
        )

        y = int(
            self.editor.canvas.get_height()
            * self.position[1]
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):
        self.system.window.draw_rect(
            self.editor.canvas,
            (50, 50, 50),
            self.rect
        )

        self.system.window.draw_rect(
            self.editor.canvas,
            (200, 200, 200),
            self.rect,
            2
        )

        text = self.font.render(
            "Scrollable Text",
            True,
            self.color
        )

        self.editor.canvas.blit(
            text,
            text.get_rect(center=self.rect.center)
        )