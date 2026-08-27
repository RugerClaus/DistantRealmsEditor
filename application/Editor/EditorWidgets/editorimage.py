from application.Editor.EditorWidgets.editorwidget import EditorWidget
from helper import asset


class EditorImage(EditorWidget):
    def __init__(self, editor, data):
        super().__init__(editor, data)

        self.image = data.get(
            "image",
            None
        )

        self.scale_ratio = data.get(
            "scale",
            None
        )

        self.original_surf = None
        self.surface = None

        self.load_image()

        self.scale()

    def load_image(self):

        if self.image is None:
            self.original_surf = None
            return

        image_path = asset(
            self.image
        )

        if image_path is None:
            self.original_surf = None
            return

        self.original_surf = self.system.window.load_image(
            image_path
        )

    def set_image(self, image):

        self.image = image
        self.data["image"] = image

        self.load_image()
        self.scale()

    def set_scale(self, scale):

        if scale is None or scale == "":
            self.scale_ratio = None
        else:
            self.scale_ratio = float(scale)

        self.data["scale"] = self.scale_ratio

        self.scale()

    def scale(self):

        if self.original_surf is None:
            self.surface = None
            self.rect = None
            return

        if self.scale_ratio:

            width = int(
                self.editor.canvas.get_width()
                *
                self.scale_ratio
            )

            factor = (
                width
                /
                self.original_surf.get_width()
            )

            height = int(
                self.original_surf.get_height()
                *
                factor
            )

            self.surface = self.system.window.transform_scale(
                self.original_surf,
                width,
                height
            )

        else:

            self.surface = self.original_surf

        x = int(
            self.editor.canvas.get_width()
            *
            self.position[0]
        )

        y = int(
            self.editor.canvas.get_height()
            *
            self.position[1]
        )

        self.rect = self.surface.get_rect(
            center=(x, y)
        )

    def draw(self):

        if self.surface is None:
            return

        self.system.window.blit(
            self.surface,
            self.rect
        )