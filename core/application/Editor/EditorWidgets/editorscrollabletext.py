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

        self.lines = data.get("lines", [])
        self.scroll_offset = 0

        self.show_scrollbar = data.get(
            "show_scrollbar",
            True
        )

        self.scrollbar_width = data.get(
            "scrollbar_width",
            6
        )

        self.scrollbar_color = tuple(
            data.get(
                "scrollbar_color",
                [120, 120, 120]
            )
        )

        self.scrollbar_track_color = tuple(
            data.get(
                "scrollbar_track_color",
                [40, 40, 40]
            )
        )

        self.font = FontEngine(self.font_size).font

        self.scale()

    def set_font_size(self, size):
        self.font_size = int(size)
        self.data["font_size"] = self.font_size

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

    def visible_lines(self):

        line_height = self.font.get_height()

        spacing = int(
            self.editor.canvas.get_height()
            * self.line_spacing
        )

        return max(
            1,
            self.surface.get_height()
            //
            (line_height + spacing)
        )

    def draw(self):

        self.surface.fill((0, 0, 0, 0))

        line_height = self.font.get_height()

        spacing = int(
            self.editor.canvas.get_height()
            *
            self.line_spacing
        )

        visible = self.lines[
            self.scroll_offset:
            self.scroll_offset + self.visible_lines()
        ]

        for index, columns in enumerate(visible):

            draw_y = (
                line_height // 2
                +
                index * (line_height + spacing)
            )

            for text, normalized_x, color in columns:

                surf = self.font.render(
                    text,
                    True,
                    color
                )

                x_pos = int(
                    normalized_x
                    *
                    self.editor.canvas.get_width()
                )

                relative_x = (
                    x_pos
                    -
                    self.rect.x
                )

                if self.align == "center":
                    text_rect = surf.get_rect(
                        center=(
                            relative_x,
                            draw_y
                        )
                    )

                elif self.align == "right":
                    text_rect = surf.get_rect(
                        right=relative_x,
                        centery=draw_y
                    )

                else:
                    text_rect = surf.get_rect(
                        left=relative_x,
                        centery=draw_y
                    )

                self.surface.blit(
                    surf,
                    text_rect
                )

        if self.show_scrollbar:
            self.draw_scrollbar()

        self.system.window.blit(
            self.surface,
            self.rect
        )

    def draw_scrollbar(self):

        total = len(self.lines)
        visible = self.visible_lines()

        if total <= visible:
            return

        scrollbar_height = self.surface.get_height() - 50

        track = self.system.window.make_surface(
            self.scrollbar_width,
            scrollbar_height,
            True
        )

        track.fill(
            self.scrollbar_track_color
        )

        self.surface.blit(
            track,
            (
                self.surface.get_width()
                -
                self.scrollbar_width,
                0
            )
        )

        ratio = visible / total

        handle_height = max(
            20,
            int(scrollbar_height * ratio)
        )

        scroll_ratio = (
            self.scroll_offset
            /
            (total - visible)
        )

        handle_y = int(
            (
                scrollbar_height
                -
                handle_height
            )
            *
            scroll_ratio
        )

        handle = self.system.window.make_surface(
            self.scrollbar_width,
            handle_height,
            True
        )

        handle.fill(
            self.scrollbar_color
        )

        self.surface.blit(
            handle,
            (
                self.surface.get_width()
                -
                self.scrollbar_width,
                handle_y
            )
        )