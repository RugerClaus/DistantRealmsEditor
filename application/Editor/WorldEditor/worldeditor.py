from core.util.colors import *
from core.state.ApplicationLayer.Editor.state import EDITOR_STATE
from core.state.ApplicationLayer.Editor.WorldEditor.state import WORLD_EDITOR_STATE
from core.state.ApplicationLayer.Editor.WorldEditor.statemanager import WorldEditorStateManager
from application.Editor.WorldEditor.editorworld import EditorWorld
from application.Editor.WorldEditor.mapselector import MapSelector
from application.Editor.WorldEditor.cellpalette import CellPalette


class WorldEditor:

    def __init__(self, distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system
        self.state = WorldEditorStateManager()
        self.system.input.CommandModule.sequences["save_project"] = [self.system.input.keys.l_ctrl_key(), self.system.input.keys.s_key()]
        self.system.input.CommandModule.sequences["reload_map_creator"] = [self.system.input.keys.l_ctrl_key(), self.system.input.keys.g_key()]
        self.active_file = None
        self.active_filename = None
        self.selected_map = None
        self.selected_layer = None
        self.selected_cell = 0
        self.dragging = False
        self.last_painted_cell = None
        self.drag_offset = None
        self.maps = []
        self.editor_world = EditorWorld(self.system)
        self.map_selector = MapSelector(self.distant_realms.application, self)
        self.map_properties = None
        self.cell_picker = None
        self.cell_palette_file = None
        self.world_width = self.editor_world.view_width
        self.world_height = self.editor_world.view_height
        self.draw_grid = True
        self.grid_color = gray
        self.grid_line_width = 1
        self.dirty = False
        self.distant_realms.ui_controller.show_ui("world_editor_controls")
        self.coordinate_font = 20
        self.canvas_position = None
        self.world_position = None
        self.map_position = None
        self.cell_position = None
        self.load_canvas()
        self.load_cell_palette()
        self.load_options()
        self.load_coordinate_display()
        self.initialize_map_creator()
        self.scale()
        self.ui_updated = False

    def update_ui(self):
        active_ui = self.distant_realms.ui_controller.get_active_ui()
        if active_ui is None:
            return
        if self.active_file is None:
            return
        world_name = str(self.active_file.get("name", ""))
        for element in active_ui.children:
            if element.id == "world_name":
                element.text = world_name
                break
        self.ui_updated = True

    def map_created(self, world_map):
        if world_map is None:
            return

        in_map_mode = self.state.is_state(WORLD_EDITOR_STATE.MAP)
        self.load_world()

        map_world_x = world_map.get("world_x", 0)
        map_world_y = world_map.get("world_y", 0)

        same_position = hasattr(self, "selected_world_position") and self.selected_world_position == (map_world_x, map_world_y)

        if in_map_mode:
            if same_position:
                maps = self.editor_world.get_maps_at(map_world_x, map_world_y)

                if maps:
                    maps.sort(key=lambda map: map.z_index)
                    self.map_selector.set_maps(maps)

                    for map in maps:
                        if map.z_index == world_map["z"] and map.world_x == world_map["world_x"] and map.world_y == world_map["world_y"]:
                            self.selected_map = map
                            break

                    if self.selected_map is not None:
                        self.canvas_view_x = self.selected_map.world_x
                        self.canvas_view_y = self.selected_map.world_y
                        self.canvas_view_width = self.selected_map.map_width
                        self.canvas_view_height = self.selected_map.map_height
        else:
            self.canvas_view_x = self.editor_world.view_x
            self.canvas_view_y = self.editor_world.view_y
            self.canvas_view_width = self.editor_world.view_width
            self.canvas_view_height = self.editor_world.view_height
            self.selected_map = None

        self.cell_position = None
        self.canvas.fill(black)

        if self.state.is_state(WORLD_EDITOR_STATE.WORLD):
            self.render_world()
        elif self.state.is_state(WORLD_EDITOR_STATE.MAP):
            self.render_selected_world_position()

            if self.selected_map is not None:
                self.render_hovered_cell()
        self.reset_world_canvas()

    def map_deleted(self, world_map):
        if world_map is None:
            return

        deleted_file = getattr(world_map, "filename", None)

        if self.selected_map is world_map:
            self.selected_map = None
        elif self.selected_map is not None:
            selected_file = getattr(self.selected_map, "filename", None)

            if selected_file == deleted_file:
                self.selected_map = None

        self.load_world()

        if self.state.is_state(WORLD_EDITOR_STATE.MAP):
            if hasattr(self, "selected_world_position"):
                world_x, world_y = self.selected_world_position
                maps = self.editor_world.get_maps_at(world_x, world_y)
                maps.sort(key=lambda map: map.z_index)
                self.map_selector.set_maps(maps)

                if maps:
                    self.selected_map = maps[0]
                    self.canvas_view_x = self.selected_map.world_x
                    self.canvas_view_y = self.selected_map.world_y
                    self.canvas_view_width = self.selected_map.map_width
                    self.canvas_view_height = self.selected_map.map_height
                else:
                    self.selected_map = None
                    self.canvas_view_x = self.editor_world.view_x
                    self.canvas_view_y = self.editor_world.view_y
                    self.canvas_view_width = self.editor_world.view_width
                    self.canvas_view_height = self.editor_world.view_height

            self.canvas.fill(black)

            if hasattr(self, "selected_world_position"):
                self.render_selected_world_position()
            else:
                self.render_world()

            if self.selected_map is not None:
                self.render_hovered_cell()

        elif self.state.is_state(WORLD_EDITOR_STATE.WORLD):
            self.selected_map = None
            self.canvas_view_x = self.editor_world.view_x
            self.canvas_view_y = self.editor_world.view_y
            self.canvas_view_width = self.editor_world.view_width
            self.canvas_view_height = self.editor_world.view_height
            self.canvas.fill(black)
            self.render_world()

        self.cell_position = None
        self.reset_world_canvas()

    def create_map(self, data):
        if self.active_file is None:
            return
        if self.active_filename is None:
            return

        map_filename = data["filename"]
        world_directory = self.system.os.path.dirname(self.active_filename)
        map_filename = self.system.os.path.join(world_directory, map_filename)

        map_data = {
            "width": data["width"],
            "height": data["height"],
            "cells": [[0 for _ in range(data["width"])] for _ in range(data["height"])]
        }

        with open(map_filename, "w") as file:
            self.system.json.dump(map_data, file, indent=4)

        self.active_file.setdefault("maps", []).append({
            "file": data["filename"],
            "z": data["z"],
            "velocity": data["velocity"],
            "width": data["width"],
            "height": data["height"],
            "camera_follow_x": data["camera_follow_x"],
            "camera_follow_y": data["camera_follow_y"],
            "wrap_x": data["wrap_x"],
            "wrap_y": data["wrap_y"],
            "world_x": data["world_x"],
            "world_y": data["world_y"]
        })

        self.save()
        self.load_world()

    def load_canvas(self):
        self.canvas_x = 0.0
        self.canvas_y = 0.03
        self.canvas_w = 0.75
        self.canvas_h = 9 / 16
        self.canvas_view_x = 0
        self.canvas_view_y = 0
        self.canvas_view_width = self.editor_world.view_width
        self.canvas_view_height = self.editor_world.view_height

    def load_cell_palette(self):
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

    def render_coordinate_display(self, canvas_position=None, world_position=None, map_position=None, cell_position=None):
        self.coordinate_display.fill(light_gray)

        canvas_text = "---"
        world_text = "---"
        map_text = "---"
        cell_text = "---"

        if canvas_position is not None:
            canvas_x = int(canvas_position[0] / 16)
            canvas_y = int(canvas_position[1] / 9)
            canvas_text = f"({canvas_x}, {canvas_y})"

        if world_position is not None:
            world_x = int(world_position[0] * 10)
            world_y = int(world_position[1] * 10)
            world_text = f"({world_x}, {world_y})"

        if map_position is not None:
            map_x = int(map_position[0] + 1)
            map_y = int(map_position[1] + 1)
            map_text = f"({map_x}, {map_y})"

        if cell_position is not None:
            cell_x = int(cell_position[0])
            cell_y = int(cell_position[1])
            cell_text = f"({cell_x}, {cell_y})"

        text = f"Canvas: {canvas_text}    World: {world_text}    Map: {map_text}    Cell: {cell_text}"
        surface = self.system.font.get_font(self.coordinate_font).render(text, True, black)
        text_rect = surface.get_rect(center=(self.coordinate_display.get_width() // 2, self.coordinate_display.get_height() // 2))
        self.coordinate_display.blit(surface, text_rect)

    def load_world(self):
        if self.active_filename is None:
            return
        self.editor_world.load(self.active_filename)
        self.world_width = self.editor_world.view_width
        self.world_height = self.editor_world.view_height

    def select_world_position(self, world_x, world_y):
        maps = self.editor_world.get_maps_at(world_x, world_y)

        if not maps:
            return

        maps.sort(key=lambda map: map.z_index)
        self.selected_world_position = (world_x, world_y)
        self.selected_map = maps[0]
        self.map_selector.set_maps(maps)
        self.canvas_view_x = self.selected_map.world_x
        self.canvas_view_y = self.selected_map.world_y
        self.canvas_view_width = self.selected_map.map_width
        self.canvas_view_height = self.selected_map.map_height
        self.state.set_state(WORLD_EDITOR_STATE.MAP)

        if not self.map_properties:
            self.initialize_map_properties()
        self.map_properties.show()

    def select_map_layer(self, selected_map):

        if selected_map is None:
            return

        self.selected_map = selected_map

        self.canvas_view_x = selected_map.world_x
        self.canvas_view_y = selected_map.world_y
        self.canvas_view_width = selected_map.map_width
        self.canvas_view_height = selected_map.map_height

        if self.map_properties:
            self.map_properties.load_map_properties()

    def save(self):
        if self.active_filename is None:
            return

        self.editor_world.save()
        self.distant_realms.application.util.save_project_file(self.active_filename, self.active_file)
        self.dirty = False
        print(f"Saved project file: {self.active_filename}")

    def set_cell(self, cell_position):
        if self.selected_map is None:
            return
        if self.selected_cell is None:
            return
        if cell_position is None:
            return

        column, row = cell_position
        self.selected_map.set_cell(column, row, self.selected_cell)
        self.dirty = True

    def reset_world_canvas(self):
        self.canvas_view_x = self.editor_world.view_x
        self.canvas_view_y = self.editor_world.view_y
        self.canvas_view_width = self.editor_world.view_width
        self.canvas_view_height = self.editor_world.view_height
        self.selected_map = None
        self.cell_position = None
        self.state.set_state(WORLD_EDITOR_STATE.WORLD)

        self.map_selector.set_maps([])
        self.map_properties.hide()

    def handle_event(self, event, command):

        # Map creator is a true modal UI layer.
        # Nothing underneath it should receive input.
        if self.map_creator.visible:

            if event.type == self.system.input.keydown():

                if event.key == self.system.input.keys.escape_key():
                    self.map_creator.hide()

            if command == "reload_map_creator":
                print("Reloading map creator modal...")
                self.initialize_map_creator()
                self.map_creator.visible = True

            self.map_creator.handle_event(event, command)

            return

        # The properties UI is NOT modal.
        # It receives its own events, but the rest of the editor
        # should continue receiving events as well.
        if self.map_properties and self.map_properties.visible:
            self.map_properties.handle_event(event, command)

        mouse_pos = self.system.input.get_mouse_pos()

        # Update canvas-relative mouse state.
        if self.canvas_rect.collidepoint(mouse_pos):

            self.canvas_position = self.get_canvas_position(mouse_pos)
            self.world_position = self.get_world_position(mouse_pos)
            self.map_position = self.get_world_cell(mouse_pos)

        else:

            self.canvas_position = None
            self.world_position = None
            self.map_position = None

        # Global editor commands.
        if command == "save_project":
            self.save()
            return

        # Cell picker remains independently interactive.
        if self.cell_picker:
            self.cell_picker.handle_event(event)

        # Map selector remains independently interactive.
        if self.state.is_state(WORLD_EDITOR_STATE.MAP):

            self.map_selector.handle_event(event, command)

            if event.type == self.system.input.keydown():

                if event.key == self.system.input.keys.escape_key():
                    self.reset_world_canvas()

        # World/canvas mouse interaction.
        if event.type == self.system.input.mouse_button_down():

            if event.button != 1:
                return

            if not self.canvas_rect.collidepoint(event.pos):
                return

            if self.state.is_state(WORLD_EDITOR_STATE.MAP):

                if self.cell_position is not None:

                    self.dragging = True
                    self.last_painted_cell = None

                    self.set_cell(self.cell_position)

                    self.last_painted_cell = self.cell_position

            elif self.state.is_state(WORLD_EDITOR_STATE.WORLD):

                world_x, world_y = self.get_world_position(event.pos)

                self.select_world_position(
                    int(world_x),
                    int(world_y)
                )

        elif event.type == self.system.input.mouse_button_up():

            if event.button == 1:

                self.dragging = False
                self.drag_offset = None
                self.last_painted_cell = None

        elif event.type == self.system.input.mouse_motion():

            if self.canvas_position is None:
                return

            if not self.dragging:
                return

            if not self.state.is_state(WORLD_EDITOR_STATE.MAP):
                return

            if self.cell_position is None:
                return

            if self.cell_position == self.last_painted_cell:
                return

            self.set_cell(self.cell_position)

            self.last_painted_cell = self.cell_position

    def update(self):
        if self.map_creator.visible:
            self.map_creator.update()

        if self.map_properties:
            if self.map_properties.visible:
                self.map_properties.update()

        if self.active_file and self.active_filename:
            if not self.ui_updated:
                self.update_ui()

            cell_palette_file = self.system.os.path.join(self.system.os.path.dirname(self.active_filename), 
                                                         self.active_file.get("cell_palette", ""))

            if self.cell_picker is None or self.cell_palette_file != cell_palette_file:
                self.cell_picker = CellPalette(self, cell_palette_file)
                self.cell_palette_file = cell_palette_file

        if self.state.is_state(WORLD_EDITOR_STATE.MAP):
            self.map_selector.update()
            if self.map_properties:
                if self.map_properties.visible:
                    self.map_properties.update()

    def draw(self):
        self.distant_realms.system.window.fill(white)

        if self.canvas:
            self.canvas.fill(black)

            if self.state.is_state(WORLD_EDITOR_STATE.WORLD):
                self.render_world()
            elif self.state.is_state(WORLD_EDITOR_STATE.MAP):
                self.render_selected_world_position()
                self.render_hovered_cell()

            self.distant_realms.system.window.blit(self.canvas, self.canvas_rect)

        if self.options:
            self.options.fill(light_gray)
            self.distant_realms.system.window.blit(self.options, self.options_rect)

        if self.state.is_state(WORLD_EDITOR_STATE.MAP):
            self.map_selector.draw()

        if self.cell_palette:
            self.cell_palette.fill(beige)

            if self.cell_picker is not None:
                self.cell_picker.draw()

            self.distant_realms.system.window.blit(
                self.cell_palette,
                self.cell_palette_rect
            )

            if self.cell_picker is not None:
                self.cell_picker.tooltip.draw()

        if self.map_creator.visible:
            self.map_creator.draw()

        if self.coordinate_display:
            self.render_coordinate_display(self.canvas_position, self.world_position, self.map_position, self.cell_position)
            self.distant_realms.system.window.blit(self.coordinate_display, self.coordinate_display_rect)

        if self.map_properties:
            if self.map_properties.visible:
                self.map_properties.draw()

    def render_world(self):
        for map in self.editor_world.maps:
            x, y = self.world_to_canvas(map.world_x, map.world_y)
            width, height = self.world_size_to_canvas(map.map_width, map.map_height)
            self.render_map(map, x, y, width, height)

        self.render_grid()

    def render_selected_world_position(self):
        if not hasattr(self, "selected_world_position"):
            return

        world_x, world_y = self.selected_world_position
        maps = self.editor_world.get_maps_at(world_x, world_y)

        if not maps:
            return

        maps.sort(key=lambda map: map.z_index)

        for map in maps:
            width, height = self.world_size_to_canvas(map.map_width, map.map_height)
            x, y = self.world_to_canvas(map.world_x, map.world_y)
            self.render_map(map, x, y, width, height)

            if map is self.selected_map:
                self.render_map_grid(map, x, y, width, height)

    def render_hovered_cell(self):
        if self.canvas_position is None:
            return

        if self.selected_map is None:
            return

        map = self.selected_map
        map_x, map_y = self.world_to_canvas(map.world_x, map.world_y)
        map_width, map_height = self.world_size_to_canvas(map.map_width, map.map_height)
        mouse_x, mouse_y = self.canvas_position

        if mouse_x < map_x or mouse_x >= map_x + map_width or mouse_y < map_y or mouse_y >= map_y + map_height:
            return

        cell_width = map_width / map.columns
        cell_height = map_height / map.rows
        column = int((mouse_x - map_x) / cell_width)
        row = int((mouse_y - map_y) / cell_height)
        self.cell_position = (column, row)

        cell_x = round(map_x + column * cell_width)
        cell_y = round(map_y + row * cell_height)
        cell_width = round(cell_width)
        cell_height = round(cell_height)

        overlay = self.distant_realms.system.window.make_surface(cell_width, cell_height, True)
        overlay.fill((255, 255, 255, 80))
        self.canvas.blit(overlay, (cell_x, cell_y))

    def render_map_grid(self, map, x, y, width, height):
        if not self.draw_grid:
            return

        for column in range(map.columns + 1):
            cell_x = round(x + column * width / map.columns)
            self.distant_realms.system.window.draw_line(self.canvas, (cell_x, y), (cell_x, y + height), self.grid_color, self.grid_line_width)

        for row in range(map.rows + 1):
            cell_y = round(y + row * height / map.rows)
            self.distant_realms.system.window.draw_line(self.canvas, (x, cell_y), (x + width, cell_y), self.grid_color, self.grid_line_width)

    def get_canvas_position(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        local_x = mouse_x - self.canvas_rect.left
        local_y = mouse_y - self.canvas_rect.top
        return local_x, local_y

    def get_world_position(self, mouse_pos):
        local_x, local_y = self.get_canvas_position(mouse_pos)
        width = self.canvas.get_width()
        height = self.canvas.get_height()
        return self.editor_world.view_x + local_x / width * self.editor_world.view_width, self.editor_world.view_y + local_y / height * self.editor_world.view_height

    def get_world_cell(self, mouse_pos):
        world_x, world_y = self.get_world_position(mouse_pos)
        column = int(world_x)
        row = int(world_y)

        if column < self.editor_world.view_x or column >= self.editor_world.view_x + self.editor_world.view_width or row < self.editor_world.view_y or row >= self.editor_world.view_y + self.editor_world.view_height:
            return None

        return column, row

    def reload_selected_map(self, filename=None):

        if self.active_filename is None:
            return

        if filename is None:

            if self.selected_map is None:
                return

            filename = getattr(
                self.selected_map,
                "filename",
                None
            )

        if filename is None:
            return

        # Preserve the current editor state.
        was_map_mode = self.state.is_state(
            WORLD_EDITOR_STATE.MAP
        )

        selected_world_position = getattr(
            self,
            "selected_world_position",
            None
        )

        # Reload the world data.
        self.load_world()

        if not was_map_mode:
            return

        if selected_world_position is None:
            return

        world_x, world_y = selected_world_position

        maps = self.editor_world.get_maps_at(
            world_x,
            world_y
        )

        if not maps:
            self.selected_map = None
            self.map_selector.set_maps([])
            return

        maps.sort(
            key=lambda map: map.z_index
        )

        self.map_selector.set_maps(maps)

        # Find the map we just edited.
        self.selected_map = None

        for map in maps:

            if getattr(
                map,
                "filename",
                None
            ) == filename:

                self.selected_map = map
                break

        if self.selected_map is None:
            self.selected_map = maps[0]

        # Restore the map viewport.
        self.canvas_view_x = (
            self.selected_map.world_x
        )

        self.canvas_view_y = (
            self.selected_map.world_y
        )

        self.canvas_view_width = (
            self.selected_map.map_width
        )

        self.canvas_view_height = (
            self.selected_map.map_height
        )

        # Keep MAP mode.
        self.state.set_state(
            WORLD_EDITOR_STATE.MAP
        )

        self.cell_position = None

        self.canvas.fill(black)

        self.render_selected_world_position()

        self.render_hovered_cell()

        self.reset_world_canvas = self.reset_world_canvas

    def scale(self):
        ww = self.distant_realms.system.window.get_width()
        wh = self.distant_realms.system.window.get_height()

        x = int(ww * self.canvas_x)
        y = int(wh * self.canvas_y)
        width = int(ww * self.canvas_w)
        height = int(width * self.canvas_h)
        self.canvas = self.distant_realms.system.window.make_surface(width, height)
        self.canvas_rect = self.canvas.get_rect(topleft=(x, y))

        x = int(ww * self.palette_x)
        y = int(wh * self.palette_y)
        width = int(ww * self.palette_w)
        height = int(wh * self.palette_h)
        self.cell_palette = self.distant_realms.system.window.make_surface(width, height)
        self.cell_palette_rect = self.cell_palette.get_rect(topleft=(x, y))

        x = int(ww * self.options_x)
        y = int(wh * self.options_y)
        width = int(ww * self.options_w)
        height = int(wh * self.options_h)
        self.options = self.distant_realms.system.window.make_surface(width, height)
        self.options_rect = self.options.get_rect(topleft=(x, y))

        coordinate_gap = 6
        coordinate_height = int(wh * self.coordinate_display_h)

        x = self.canvas_rect.left
        y = self.canvas_rect.bottom + coordinate_gap
        width = self.canvas_rect.width
        height = coordinate_height

        self.coordinate_display = self.distant_realms.system.window.make_surface(width, height)
        self.coordinate_display_rect = self.coordinate_display.get_rect(
            topleft=(x, y)
        )

        self.map_creator.scale()
        self.map_selector.scale()

        if self.cell_picker:
            self.cell_picker.scale()

        if self.map_properties:
            self.map_properties.scale()

    def clean_up_states(self):
        pass

    def render_grid(self):
        if not self.draw_grid:
            return

        width = self.canvas.get_width()
        height = self.canvas.get_height()

        for column in range(int(self.editor_world.view_width) + 1):
            world_x = self.editor_world.view_x + column
            x, _ = self.world_to_canvas(world_x, self.editor_world.view_y)
            self.distant_realms.system.window.draw_line(self.canvas, (x, 0), (x, height), self.grid_color, self.grid_line_width)

        for row in range(int(self.editor_world.view_height) + 1):
            world_y = self.editor_world.view_y + row
            _, y = self.world_to_canvas(self.editor_world.view_x, world_y)
            self.distant_realms.system.window.draw_line(self.canvas, (0, y), (width, y), self.grid_color, self.grid_line_width)

    def world_to_canvas(self, world_x, world_y):
        x = (world_x - self.canvas_view_x) / self.canvas_view_width * self.canvas.get_width()
        y = (world_y - self.canvas_view_y) / self.canvas_view_height * self.canvas.get_height()
        return round(x), round(y)

    def world_size_to_canvas(self, width, height):
        return round(width / self.canvas_view_width * self.canvas.get_width()), round(height / self.canvas_view_height * self.canvas.get_height())

    def render_map(self, map, x, y, width, height):
        map.render_layer()
        layer = map.layer_surface

        if layer.get_width() != width or layer.get_height() != height:
            layer = self.distant_realms.system.window.transform_scale(layer, width, height)

        self.canvas.blit(layer, (x, y))

    def render_cell_palette(self):
        if not self.editor_world.cell_palette:
            return

        padding = 10
        cell_size = 64
        x = padding
        y = padding

        for cell_id, cell in self.editor_world.cell_palette.items():
            color = cell.get("color")

            if color is None:
                color = black

            rect = self.distant_realms.system.window.Rect(x, y, cell_size, cell_size)
            self.distant_realms.system.window.draw_rect(self.cell_palette, color, rect)
            self.distant_realms.system.window.draw_rect(self.cell_palette, white, rect, 1)
            x += cell_size + padding

            if x + cell_size > self.cell_palette.get_width():
                x = padding
                y += cell_size + padding

    def initialize_map_creator(self):
        import importlib
        from application.Editor.modals import map_creator
        importlib.reload(map_creator)
        self.map_creator = map_creator.MapCreator(self.distant_realms, self)

    def initialize_map_properties(self):
        import importlib
        from application.Editor.WorldEditor import mapproperties

        importlib.reload(mapproperties)

        self.map_properties = mapproperties.MapProperties(
            self.distant_realms,
            self
        )