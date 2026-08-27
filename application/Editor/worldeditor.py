from core.util.colors import *
from core.ui.font import FontEngine

from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.state.ApplicationLayer.Editor.WorldEditor.state import WORLD_EDITOR_STATE
from core.state.ApplicationLayer.Editor.WorldEditor.statemanager import WorldEditorStateManager


class WorldEditor:

    def __init__(self, distant_realms):

        self.distant_realms = distant_realms
        self.system = distant_realms.system
        self.state = WorldEditorStateManager()

        self.system.input.CommandModule.sequences["save_project"] = [self.system.input.keys.l_ctrl_key(),self.system.input.keys.s_key()]

        self.system.input.CommandModule.sequences["reload_map_creator"] = [self.system.input.keys.l_ctrl_key(),self.system.input.keys.g_key()]

        self.active_file = None
        self.active_filename = None

        self.selected_map = None
        self.selected_layer = None
        self.selected_cell = None

        self.dragging = False
        self.drag_offset = None

        self.maps = []

        self.world_width = 9
        self.world_height = 9

        self.draw_grid = True
        self.grid_color = gray
        self.grid_line_width = 1

        self.dirty = False

        self.coordinate_font = FontEngine(20)
        self.canvas_position = None
        self.world_position = None
        self.map_position = None

        self.load_canvas()
        self.load_cell_pallete()
        self.load_options()
        self.load_coordinate_display()
        self.initialize_map_creator()

        self.scale()

    def create_new_map_layer(self):
        self.map_creator.show()
        
    def load_canvas(self):
        self.canvas_x = 0.0
        self.canvas_y = 0.03
        self.canvas_w = 0.75
        self.canvas_h = 9 / 16

    def load_cell_pallete(self):
        self.palette_x = 0.75
        self.palette_y = 0.03
        self.palette_w = 0.25
        self.palette_h = 0.5

    def load_options(self):
        self.options_x = 0.75
        self.options_y = 0.5
        self.options_w = 0.25
        self.options_h = 0.5

    def load_coordinate_display(self):
        self.coordinate_display_x = self.canvas_x
        self.coordinate_display_centerx = self.canvas_w / 2
        self.coordinate_display_y = self.canvas_y
        self.coordinate_display_centery = self.canvas_h / 2
        self.coordinate_display_w = self.canvas_w / 2
        self.coordinate_display_h = 0.02

    def render_coordinate_display(
        self,
        canvas_position=None,
        world_position=None,
        map_position=None
    ):

        self.coordinate_display.fill(light_gray)

        if (
            canvas_position is None
            or world_position is None
            or map_position is None
        ):
            return

        canvas_x = int(canvas_position[0] / 16)
        canvas_y = int(canvas_position[1] / 9)

        world_x = int(world_position[0] * 10)
        world_y = int(world_position[1] * 10)

        map_x = int(map_position[0] + 1)
        map_y = int(map_position[1] + 1)

        text = (
            f"Canvas: ({canvas_x}, {canvas_y})    "
            f"World: ({world_x}, {world_y})    "
            f"Map: ({map_x}, {map_y})"
        )

        surface = self.coordinate_font.font.render(
            text,
            True,
            black
        )

        text_rect = surface.get_rect(
            center=(
                self.coordinate_display.get_width() // 2,
                self.coordinate_display.get_height() // 2
            )
        )

        self.coordinate_display.blit(
            surface,
            text_rect
        )

    def load_world(self):
        if self.active_file is None:
            return

        self.maps.clear()

    def save(self):

        if self.active_file is None:
            return

        if self.active_filename is None:
            return

        self.distant_realms.application.util.save_project_file(
            self.active_filename,
            self.active_file
        )

        self.dirty = False

    def handle_event(self, event, command):
        mouse_pos = self.system.input.get_mouse_pos()

        if self.canvas_rect.collidepoint(mouse_pos):

            self.canvas_position = self.get_canvas_position(mouse_pos)
            self.world_position = self.get_world_position(mouse_pos)
            self.map_position = self.get_world_cell(mouse_pos)

        else:

            self.canvas_position = None
            self.world_position = None
            self.map_position = None

        if command == "save_project":
            self.save()
            return

        if event.type == self.distant_realms.system.input.mouse_button_down():

            if event.button != 1:
                return

            if not self.canvas_rect.collidepoint(event.pos):
                return

        elif event.type == self.distant_realms.system.input.mouse_button_up():

            if event.button == 1:
                self.dragging = False
                self.drag_offset = None

        elif event.type == self.distant_realms.system.input.mouse_motion():

            if self.canvas_position is None:
                return

            if self.dragging:
                pass

        

        if self.map_creator.visible:
            if event.type == self.system.input.keydown():
                if event.key == self.system.input.keys.escape_key():
                    self.hide()
            if command == "reload_map_creator":
                print("Reloading map creator modal...")
                self.initialize_map_creator()
                self.map_creator.visible = True
            self.map_creator.handle_event(event,command)

    def update(self):
        if self.map_creator.visible:
            self.map_creator.update()

    def draw(self):
        self.distant_realms.system.window.fill(white)

        if self.canvas:
            self.canvas.fill(black)

            self.render_grid()

            self.distant_realms.system.window.blit(
                self.canvas,
                self.canvas_rect
            )

        if self.cell_pallete:
            self.cell_pallete.fill(beige)

            self.distant_realms.system.window.blit(
                self.cell_pallete,
                self.cell_pallete_rect
            )

        if self.options:
            self.options.fill(light_gray)

            self.distant_realms.system.window.blit(
                self.options,
                self.options_rect
            )

        if self.coordinate_display:

            self.render_coordinate_display(
                self.canvas_position,
                self.world_position,
                self.map_position
            )

            self.distant_realms.system.window.blit(
                self.coordinate_display,
                self.coordinate_display_rect
            )

        if self.map_creator.visible:
            self.map_creator.draw()

    def get_canvas_position(self, mouse_pos):

        mouse_x, mouse_y = mouse_pos

        local_x = mouse_x - self.canvas_rect.left
        local_y = mouse_y - self.canvas_rect.top

        return local_x, local_y

    def get_world_position(self, mouse_pos):
        local_x, local_y = self.get_canvas_position(mouse_pos)

        width = self.canvas.get_width()
        height = self.canvas.get_height()

        return (
            local_x / width * self.world_width,
            local_y / height * self.world_height
        )

    def get_world_cell(self, mouse_pos):
        world_x, world_y = self.get_world_position(mouse_pos)

        column = int(world_x)
        row = int(world_y)

        if (
            column < 0
            or column >= self.world_width
            or row < 0
            or row >= self.world_height
        ):
            return None

        return column, row
        
    def scale(self):

        ww = self.distant_realms.system.window.get_width()
        wh = self.distant_realms.system.window.get_height()

        x = int(ww * self.canvas_x)
        y = int(wh * self.canvas_y)

        width = int(ww * self.canvas_w)
        height = int(width * self.canvas_h)

        self.canvas = self.distant_realms.system.window.make_surface(
            width,
            height
        )

        self.canvas_rect = self.canvas.get_rect(
            topleft=(x, y)
        )

        x = int(ww * self.palette_x)
        y = int(wh * self.palette_y)

        width = int(ww * self.palette_w)
        height = int(wh * self.palette_h)

        self.cell_pallete = self.distant_realms.system.window.make_surface(
            width,
            height
        )

        self.cell_pallete_rect = self.cell_pallete.get_rect(
            topleft=(x, y)
        )

        x = int(ww * self.options_x)
        y = int(wh * self.options_y)

        width = int(ww * self.options_w)
        height = int(wh * self.options_h)

        self.options = self.distant_realms.system.window.make_surface(
            width,
            height
        )

        self.options_rect = self.options.get_rect(
            topleft=(x, y)
        )

        x = self.canvas_rect.left
        y = self.canvas_rect.bottom + self.coordinate_display_h / 2

        width = self.canvas_rect.width
        height = int(wh * self.coordinate_display_h)

        self.coordinate_display = self.distant_realms.system.window.make_surface(
            width,
            height
        )

        self.coordinate_display_rect = self.coordinate_display.get_rect(
            center=(self.canvas_rect.width/2, y)
        )

    def clean_up_states(self):
        pass


    def render_grid(self):
        if not self.draw_grid:
            return

        width = self.canvas.get_width()
        height = self.canvas.get_height()

        for column in range(self.world_width + 1):

            x = round(
                column * width / self.world_width
            )

            self.distant_realms.system.window.draw_line(
                self.canvas,
                (x, 0),
                (x, height),
                self.grid_color,
                self.grid_line_width
            )

        for row in range(self.world_height + 1):

            y = round(
                row * height / self.world_height
            )

            self.distant_realms.system.window.draw_line(
                self.canvas,
                (0, y),
                (width, y),
                self.grid_color,
                self.grid_line_width
            )

    def initialize_map_creator(self):
        import importlib
        from application.Editor.modals import map_creator
        importlib.reload(map_creator)
        self.map_creator = map_creator.MapCreator(self.distant_realms)
