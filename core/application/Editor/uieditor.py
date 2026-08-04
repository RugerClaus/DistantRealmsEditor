from core.ui.widgets.label import Label
class UIEditor:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        self.load_canvas()
        self.selected_element = None
        self.dragging = False
        self.drag_offset = None

    def load_canvas(self):
        self.canvas_x = 0.0
        self.canvas_y = 0.0
        self.canvas_w = 0.75
        self.canvas_h = 9/16
        ww = self.app_interface.system.window.get_width()
        wh = self.app_interface.system.window.get_height()

        x = int(ww * self.canvas_x)
        y = int(wh * self.canvas_y)

        width = int(ww * self.canvas_w)
        height = int(width * self.canvas_h)

        self.canvas = self.app_interface.system.window.make_surface(
            width,
            height
        )

        self.canvas_rect = self.canvas.get_rect(topleft=(x, y))


    def handle_event(self,event):
        if event.type == self.app_interface.system.input.video_resize_event():
            self.load_canvas()
        if event.type == self.app_interface.system.input.keydown():
            if event.key == self.app_interface.system.input.keys.t_key():
                print(self.canvas_rect.width,self.canvas_rect.height)

    def update(self):
        pass

    def draw(self):
        self.app_interface.system.window.fill((255,255,255))
        if self.canvas:
            self.canvas.fill((0,0,0))
            self.app_interface.system.window.blit(self.canvas,self.canvas_rect)