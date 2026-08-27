from core.util.colors import *

class MapCreator:
    def __init__(self, distant_realms):

        self.distant_realms = distant_realms
        self.system = distant_realms.system

        self.visible = False

        self.surface = None
        self.rect = None

        self.scale()

    def scale(self):

        width = self.system.window.get_width()
        height = self.system.window.get_height()

        self.surface = self.system.window.make_surface(width / 3,height / 1.5)

        self.rect = self.surface.get_rect(center=(width / 2, height / 2))

    def show(self):
        self.distant_realms.ui_controller.show_ui("map_creator_form")
        self.visible = True

    def hide(self):
        
        self.visible = False

    def handle_event(self, event, command):
        if not self.visible:
            return

    def update(self):
        if not self.visible:
            return

    def draw(self):
        if not self.visible:
            return

        self.surface.fill(gray)

        self.system.window.blit(
            self.surface,
            self.rect
        )