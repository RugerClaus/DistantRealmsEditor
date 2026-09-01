from core.util.colors import *
from core.engine.world.loader import MapLoader
from core.ui.widgets.tooltip import Tooltip


class CellPalette:

    def __init__(self, editor, cell_file):
        self.editor = editor
        self.dr = editor.distant_realms
        self.system = self.dr.system
        self.cells = {}
        self.rects = {}
        self.cell_size = self.system.window.get_width() // 60
        self.padding = 6
        self.columns = 1
        self.selected_cell = None
        self.hovered_cell = None
        map_loader = MapLoader(self.system, None)
        self.cells = map_loader.def_loader.load(cell_file)
        self.tooltip = Tooltip(self.system, background_color=dark_gray, text_color=white)
        self.set_cells(self.cells)

    def scale(self):
        self.cell_size = self.system.window.get_width() // 60
        self.set_cells(self.cells)
        self.tooltip.scale()

    def set_cells(self, cells):
        self.cells = cells or {}
        self.rects.clear()
        palette_width = self.editor.cell_palette.get_width()
        self.columns = max(1, (palette_width - self.padding) // (self.cell_size + self.padding))

        for index, cell_id in enumerate(self.cells):
            column = index % self.columns
            row = index // self.columns
            x = self.padding + column * (self.cell_size + self.padding)
            y = self.padding + row * (self.cell_size + self.padding)
            self.rects[cell_id] = self.system.window.Rect(x, y, self.cell_size, self.cell_size)

    def handle_event(self, event):
        if event.type == self.system.input.mouse_motion():
            mx, my = self.system.input.get_mouse_pos()

            if not self.editor.cell_palette_rect.collidepoint(mx, my):
                self.hovered_cell = None
                self.tooltip.hide()
                return

            local_x = mx - self.editor.cell_palette_rect.x
            local_y = my - self.editor.cell_palette_rect.y
            self.hovered_cell = None

            for cell_id, rect in self.rects.items():
                if not rect.collidepoint(local_x, local_y):
                    continue

                self.hovered_cell = cell_id
                cell = self.cells.get(cell_id, {})
                name = cell.get("name", str(cell_id))
                self.tooltip.set_text(name)
                self.tooltip.set_topright((mx - 5, my))
                self.tooltip.show()
                break

            if self.hovered_cell is None:
                self.tooltip.hide()

            return

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
                break

    def draw(self):
        for cell_id, rect in self.rects.items():
            cell = self.cells[cell_id]
            color = cell.get("color")

            if color is None:
                color = light_gray

            self.system.window.draw_rect(self.editor.cell_palette, color, rect)
            self.system.window.draw_rect(self.editor.cell_palette, black, rect, 1)

            if cell_id == self.selected_cell:
                self.system.window.draw_rect(self.editor.cell_palette, white, rect, 3)

            surface = self.system.font.get_font(20).render(str(cell_id), True, black)
            text_rect = surface.get_rect(center=rect.center)
            self.editor.cell_palette.blit(surface, text_rect)