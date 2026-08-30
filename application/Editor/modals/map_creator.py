from core.util.colors import *

from core.ui.uicontroller import UIController

class MapCreator:

    def __init__(self, distant_realms):

        self.distant_realms = distant_realms
        self.system = distant_realms.system

        self.ui_controller = UIController(
            self.system,
            self.distant_realms.ui
        )

        self.visible = False

        self.surface = None
        self.rect = None

        self.scale()

    def scale(self):

        width = self.system.window.get_width()
        height = self.system.window.get_height()

        print(
            "SCALING MAP CREATOR",
            id(self),
            width,
            height
        )

        self.surface = self.system.window.make_surface(
            int(width / 3.5),
            int(height / 2)
        )

        self.rect = self.surface.get_rect(
            center=(
                width // 2,
                height // 2
            )
        )

        self.ui_controller.scale()
    def show(self):

        if self.ui_controller.show_ui("map_creator_form"):
            self.ui_controller.scale()

        self.visible = True

    def hide(self):

        self.ui_controller.clear()
        self.visible = False

    def handle_event(self, event, command):

        if not self.visible:
            return

        self.ui_controller.handle_event(event)

    def update(self):

        if not self.visible:
            return

        self.ui_controller.update()

    def draw(self):

        if not self.visible:
            return

        self.surface.fill(gray)

        self.system.window.blit(
            self.surface,
            self.rect
        )

        self.ui_controller.draw()