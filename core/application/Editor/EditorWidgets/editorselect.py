from core.ui.font import FontEngine
from core.util.colors import white, black
from core.application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorSelect(EditorWidget):

    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.options = data.get("options", [])

        self.selected_option = data.get(
            "selected_option",
            self.options[0] if self.options else None
        )

        self.font_size = data.get("font_size", 30)

        # Normalized dimensions relative to the editor canvas.
        self.width = data.get("width", 0.3)
        self.height = data.get("height", 0.06)

        self.padding = data.get("padding", 10)

        self.background_color = tuple(
            data.get("background_color", white)
        )

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()

    def set_options(self, options):
        self.options = options
        self.data["options"] = options

        if self.options and self.selected_option not in self.options:
            self.selected_option = self.options[0]
            self.data["selected_option"] = self.selected_option

        self.scale()

    def set_selected_option(self, option):
        self.selected_option = option
        self.data["selected_option"] = option

        self.scale()

    def set_font_size(self, size):
        self.font_size = int(size)
        self.data["font_size"] = self.font_size

        self.font = FontEngine(
            self.font_size
        ).font

        self.scale()

    def set_width(self, width):
        self.width = float(width)
        self.data["width"] = self.width

        self.scale()

    def set_height(self, height):
        self.height = float(height)
        self.data["height"] = self.height

        self.scale()

    def set_padding(self, padding):
        self.padding = int(padding)
        self.data["padding"] = self.padding

        self.scale()

    def scale(self):
        canvas_width = self.editor.canvas.get_width()
        canvas_height = self.editor.canvas.get_height()

        self.font = FontEngine(
            self.font_size
        ).font

        width = max(
            1,
            int(canvas_width * self.width)
        )

        height = max(
            1,
            int(canvas_height * self.height)
        )

        x = int(
            canvas_width * self.position[0]
        )

        y = int(
            canvas_height * self.position[1]
        )

        self.surface = self.system.window.make_surface(
            width,
            height,
            True
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):
        if self.surface is None or self.rect is None:
            return

        self.surface.fill(
            self.background_color
        )

        # Select box border
        self.system.window.draw_rect(
            self.surface,
            black,
            self.surface.get_rect(),
            2
        )

        # Selected option
        if self.selected_option is not None:
            surf = self.font.render(
                str(self.selected_option),
                False,
                black
            )

            text_rect = surf.get_rect(
                midleft=(
                    self.padding,
                    self.surface.get_height() // 2
                )
            )

            self.surface.blit(
                surf,
                text_rect
            )

        # Dropdown arrow
        arrow_x = self.surface.get_width() - 20
        arrow_y = self.surface.get_height() // 2

        self.system.window.draw_polygon(
            self.surface,
            black,
            [
                (arrow_x - 7, arrow_y - 3),
                (arrow_x + 7, arrow_y - 3),
                (arrow_x, arrow_y + 5)
            ]
        )

        self.system.window.blit(
            self.surface,
            self.rect
        )
