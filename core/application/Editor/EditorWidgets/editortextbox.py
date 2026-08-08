from core.ui.font import FontEngine
from core.application.Editor.EditorWidgets.editorwidget import EditorWidget
from core.util.colors import black, white


class EditorTextBox(EditorWidget):

    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.font_size = data.get("font_size", 30)

        self.text = str(
            data.get("text", "")
        )

        self.width, self.height = data.get(
            "dimensions",
            [0.1432, 0.0926]
        )

        self.background_color = tuple(
            data.get(
                "background_color",
                black
            )
        )

        self.text_color = tuple(
            data.get(
                "text_color",
                black
            )
        )

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()


    def set_text(self, text):
        self.text = str(text)[:21]
        self.data["text"] = self.text

        self.scale()


    def set_font_size(self, size):
        self.font_size = int(size)
        self.data["font_size"] = self.font_size

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()


    def set_dimensions(self, dimensions):
        self.width, self.height = dimensions

        self.data["dimensions"] = list(dimensions)

        self.scale()


    def set_background_color(self, color):
        self.background_color = tuple(color)

        self.data["background_color"] = list(color)

        self.scale()


    def set_text_color(self, color):
        self.text_color = tuple(color)

        self.data["text_color"] = list(color)

        self.scale()


    def scale(self):

        ww = self.editor.canvas.get_width()
        wh = self.editor.canvas.get_height()

        x = int(ww * self.position[0])
        y = int(wh * self.position[1])

        width = int(
            ww * self.width
        )

        height = int(
            wh * self.height
        )

        self.bounding_box = self.system.window.make_surface(
            width,
            height
        )

        self.bounding_box_rect = self.bounding_box.get_rect(
            center=(x, y)
        )

        border = 2

        text_width = max(
            1,
            width - border * 2
        )

        text_height = max(
            1,
            height - border * 2
        )

        self.text_box = self.system.window.make_surface(
            text_width,
            text_height
        )

        self.text_box_rect = self.text_box.get_rect(
            center=self.bounding_box_rect.center
        )


    def draw(self):

        self.bounding_box.fill(
            self.background_color
        )

        self.text_box.fill(
            white
        )

        self.system.window.draw_rect(
            self.bounding_box,
            black,
            self.bounding_box.get_rect(),
            2
        )

        self.system.window.blit(
            self.bounding_box,
            self.bounding_box_rect
        )

        self.system.window.blit(
            self.text_box,
            self.text_box_rect
        )

        surf = self.font.render(
            self.text,
            False,
            self.text_color
        )

        rect = surf.get_rect(
            center=self.text_box_rect.center
        )

        self.system.window.blit(
            surf,
            rect
        )