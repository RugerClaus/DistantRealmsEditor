from application.Editor.EditorWidgets.editorwidget import EditorWidget


class EditorCenterText(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.text = str(
            data.get("text", "Center Text")
        )

        self.font_size = data.get(
            "font_size",
            40
        )

        self.font = self.system.font.get_font(self.font_size)

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

        lines = self.text.split("\n")

        line_height = self.font.get_height()

        total_height = (
            len(lines)
            *
            line_height
            *
            1.2
        )

        start_y = (
            y
            -
            total_height // 2
        )

        rects = []

        for i, line in enumerate(lines):
            surf = self.font.render(
                line,
                True,
                (255, 255, 255)
            )

            rect = surf.get_rect(
                center=(
                    x,
                    start_y
                    +
                    i * line_height * 1.1
                )
            )

            rects.append(
                (
                    surf,
                    rect
                )
            )

        self.rendered_lines = rects

        if rects:
            self.rect = rects[0][1].unionall(
                [r for _, r in rects]
            )
        else:
            self.rect = None

    def draw(self):

        for surf, rect in self.rendered_lines:
            self.system.window.blit(
                surf,
                rect
            )