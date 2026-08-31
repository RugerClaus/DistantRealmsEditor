from core.util.colors import *
from core.engine.world.loader import MapLoader

class CellPalette:

    def __init__(self, editor, cell_file):
        print("CELL PALETTE INIT:", cell_file)
        self.editor = editor
        self.dr = editor.distant_realms
        self.system = self.dr.system
        self.cells = {}
        self.rects = {}
        self.cell_size = 48
        self.padding = 6
        self.columns = 12
        self.selected_cell = None
        map_loader = MapLoader(self.system, None)
        self.cells = map_loader.def_loader.load(cell_file)
        print("CELL PALETTE CELLS:", self.cells)
        self.set_cells(self.cells)

    def set_cells(self, cells):
        self.cells = cells or {}
        self.rects.clear()

        for index, cell_id in enumerate(self.cells):
            column = index % self.columns
            row = index // self.columns
            x = self.padding + column * (self.cell_size + self.padding)
            y = self.padding + row * (self.cell_size + self.padding)
            self.rects[cell_id] = self.system.window.Rect(x, y, self.cell_size, self.cell_size)

    def handle_event(self, event):
        if event.type != self.system.input.mouse_button_down():
            return

        if event.button != 1:
            return

        mx, my = self.system.input.get_mouse_pos()

        if not self.editor.cell_palette_rect.collidepoint(mx, my):
            return

        local_x = mx - self.editor.cell_palette_rect.x
        local_y = my - self.editor.cell_palette_rect.y

        for cell_id, rect in self.rects.items():
            if rect.collidepoint(local_x, local_y):
                self.selected_cell = cell_id
                self.editor.selected_cell = cell_id
                print("SELECTED CELL:", cell_id)
                break

    def draw(self):
        print("CELL PALETTE DRAW:", len(self.cells))

        for cell_id, rect in self.rects.items():
            cell = self.cells[cell_id]
            color = cell.get("color")

            if color is None:
                color = light_gray

            self.system.window.draw_rect(self.editor.cell_palette, color, rect)
            self.system.window.draw_rect(self.editor.cell_palette, black, rect, 1)

            if cell_id == self.selected_cell:
                self.system.window.draw_rect(self.editor.cell_palette, white, rect, 3)

            surface = self.editor.coordinate_font.font.render(str(cell_id), True, black)
            text_rect = surface.get_rect(center=rect.center)
            self.editor.cell_palette.blit(surface, text_rect)