from core.application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorScrollableText(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.width = data.get("width", 0.8)
        self.height = data.get("height", 0.6)

        self.align = data.get("align", "left")
        self.font_size = data.get("font_size", 20)
        self.line_spacing = data.get("line_spacing", 0.01)
        self.max_char_count = data.get("max_char_count", 90)

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

    def scale(self):
        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()

        self.width_px = int(ww * self.width)
        self.height_px = int(wh * self.height)

        x = int(ww * self.position[0])
        y = int(wh * self.position[1])

        self.surface = self.system.window.make_surface(
            self.width_px,
            self.height_px,
            True
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):
        self.surface.fill((0, 0, 0, 0))

        self.system.window.draw_rect(
            self.surface,
            (50, 50, 50),
            self.surface.get_rect()
        )

        self.system.window.draw_rect(
            self.surface,
            (200, 200, 200),
            self.surface.get_rect(),
            width=2
        )

        self.system.window.blit(
            self.surface,
            self.rect
        )