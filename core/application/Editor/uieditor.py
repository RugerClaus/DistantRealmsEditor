from core.util.colors import *
from core.application.Editor.EditorWidgets.editorbutton import EditorButton
from core.application.Editor.EditorWidgets.editorlabel import EditorLabel

class UIEditor:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        self.active_file = None
        self.active_filename = None
        self.selected_element = None
        self.dragging = False
        self.drag_offset = None
        self.canvas_elements = []
        self.element_types = {
            "button": EditorButton,
            "label": EditorLabel,
            # "textbox": EditorTextBox,
            # "header": EditorHeader,
            # "image": EditorImage,
            # "query": EditorQuery,
            # "centertext": EditorCenterText,
            # "scrollabletext": EditorScrollableText,
            # "select": EditorSelect
            }
        self.load_canvas()
        self.load_widget_palette()
        self.load_options()


    def create_editor_element(self, data):
        element_type = data.get("type")

        element_class = self.element_types.get(element_type)

        if element_class is None:
            raise ValueError(f"Unknown editor element type: {element_type}")

        return element_class(self, data)


    def add_element(self, element_type):
        element_class = self.element_types.get(element_type)

        if element_class is None:
            raise ValueError(f"Unknown editor element type: {element_type}")

        defaults = {
            "button": {
                "id": "new_button",
                "type": "button",
                "font": "default",
                "text": "Button",
                "position": [0.5, 0.5],
                "action": None,
                "styles": None
            },

            "label": {
                "id": "new_label",
                "type": "label",
                "text": "Label",
                "position": [0.5, 0.5],
                "font_size": 30,
                "color": [255, 255, 255]
            }
        }

        data = defaults.get(element_type)

        if data is None:
            raise ValueError(f"No default data for editor element type: {element_type}")

        element = element_class(self, data)

        self.canvas_elements.append(element)

        if self.active_file is not None:
            self.active_file.setdefault("elements", []).append(element.data)

        return element

    def load_widget_palette(self):
        self.palette_x = 0.75
        self.palette_y = 0.0
        self.palette_w = 0.25
        self.palette_h = 0.5
        ww = self.app_interface.system.window.get_width()
        wh = self.app_interface.system.window.get_height()

        x = int(ww * self.palette_x)
        y = int(wh * self.palette_y)

        width = int(ww * self.palette_w)
        height = int(wh * self.palette_h)

        self.widget_palette = self.app_interface.system.window.make_surface(
            width,
            height
        )

        self.widget_palette_rect = self.canvas.get_rect(topleft=(x, y))

    def load_options(self):
            self.palette_x = 0.75
            self.palette_y = 0.5
            self.palette_w = 0.25
            self.palette_h = 0.5
            ww = self.app_interface.system.window.get_width()
            wh = self.app_interface.system.window.get_height()
    
            x = int(ww * self.palette_x)
            y = int(wh * self.palette_y)
    
            width = int(ww * self.palette_w)
            height = int(wh * self.palette_h)
    
            self.options = self.app_interface.system.window.make_surface(
                width,
                height
            )
    
            self.options_rect = self.canvas.get_rect(topleft=(x, y))

    def load_canvas(self,elements=None):
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
        if self.canvas_elements:
            self.canvas_elements.clear()
        if self.active_file:
            elements = self.active_file.get("elements", [])
            for element_data in elements:
                element = self.create_editor_element(element_data)
                self.dirty = True
                self.canvas_elements.append(element)

    def save(self):
        if self.active_file is None or self.active_filename is None:
            return

        self.app_interface.app_object.util.save_project_file(
            self.active_filename,
            self.active_file
        )

        self.dirty = False

    def draw_alignment_guides(self):
        if not self.dragging or self.selected_element is None:
            return

        x_ratio, y_ratio = self.selected_element.data["position"]

        if abs(x_ratio - 0.5) <= 0.005:
            x = self.canvas_rect.centerx

            self.app_interface.system.window.draw_line(
                self.canvas,
                (x, self.canvas_rect.top),
                (x, self.canvas_rect.bottom),
                red,
                1
            )

        if abs(y_ratio - 0.5) <= 0.005:
            y = self.canvas_rect.centery

            self.app_interface.system.window.draw_line(
                self.canvas,
                (0, y),
                (self.canvas.get_width(), y),
                red,
                5
            )

    def update_position_fields(self):
        if self.selected_element is None:
            return

        x, y = self.selected_element.data.get(
            "position",
            [0.5, 0.5]
        )

        x_field = self.app_interface.ui_controller.get_element("x")
        y_field = self.app_interface.ui_controller.get_element("y")
        id_field = self.app_interface.ui_controller.get_element("id")
        action_field = self.app_interface.ui_controller.get_element("action")

        if x_field:
            x_field.set_text(str(round(x * 100, 2)))

        if y_field:
            y_field.set_text(str(round(y * 100, 2)))

        if id_field:
            id_field.set_text(self.selected_element.data.get("id", ""))

        if action_field:
            action_field.set_text(self.selected_element.data.get("action", ""))


    def show_selected_properties(self):
        if self.selected_element is None:
            self.app_interface.ui_controller.show_ui("menu_editor_noprops")
            return

        element_type = self.selected_element.data.get("type")

        if element_type == "button":
            menu = "menu_editor_buttonprops"
        elif element_type == "label":
            menu = "menu_editor_labelprops"
        else:
            self.app_interface.ui_controller.show_ui("menu_editor_noprops")
            return

        self.app_interface.ui_controller.show_ui(menu)

        self.update_position_fields()

        if element_type == "button":
            text_field = self.app_interface.ui_controller.get_element("button_text")
            action_field = self.app_interface.ui_controller.get_element("action")

            if text_field:
                text_field.set_text(
                    self.selected_element.data.get("text", "")
                )

            if action_field:
                action_field.set_text(self.selected_element.data.get("action",""))

    def handle_event(self, event):
        if event.type == self.app_interface.system.input.video_resize_event():
            self.load_canvas()
            self.load_widget_palette()
            self.load_options()
            return

        if event.type == self.app_interface.system.input.mouse_button_down():
            if event.button == 1:
                if not self.canvas_rect.collidepoint(event.pos):
                    return

                for element in reversed(self.canvas_elements):
                    if element.contains_point(event.pos):
                        self.selected_element = element
                        self.show_selected_properties()
                        self.dragging = True

                        mouse_x, mouse_y = event.pos

                        self.drag_offset = (
                            mouse_x - element.rect.centerx,
                            mouse_y - element.rect.centery
                        )

                        break
                else:
                    self.app_interface.ui_controller.show_ui("menu_editor_noprops")
                    self.selected_element = None
                    self.dragging = False

        elif event.type == self.app_interface.system.input.mouse_button_up():
            if event.button == 1:
                self.dragging = False
                self.drag_offset = None

        elif event.type == self.app_interface.system.input.mouse_motion():
            if self.dragging and self.selected_element:
                self.drag_element(event.pos)

    def drag_element(self, mouse_pos):
        element = self.selected_element

        mouse_x, mouse_y = mouse_pos

        center_x = mouse_x - self.drag_offset[0]
        center_y = mouse_y - self.drag_offset[1]

        x_ratio = (
            center_x - self.canvas_rect.x
        ) / self.canvas_rect.width

        y_ratio = (
            center_y - self.canvas_rect.y
        ) / self.canvas_rect.height

        x_ratio = max(0.0, min(1.0, x_ratio))
        y_ratio = max(0.0, min(1.0, y_ratio))

        element.set_position((x_ratio, y_ratio))

        self.update_position_fields()

    def update_widget_properties(self, properties):
        element = self.selected_element

        if element is None:
            return

        current_x, current_y = element.data.get("position", [0.5, 0.5])

        x_value = properties.get("x", "")
        y_value = properties.get("y", "")

        x = current_x
        y = current_y

        if x_value.strip():
            x = max(0.0, min(1.0, float(x_value) / 100.0))

        if y_value.strip():
            y = max(0.0, min(1.0, float(y_value) / 100.0))

        element.set_position((x, y))

        properties.pop("x", None)
        properties.pop("y", None)

        for name, value in properties.items():
            setter = getattr(element, f"set_{name}", None)

            if setter:
                setter(value)

        self.save()

    def update(self):
        pass

    def draw(self):
        self.app_interface.system.window.fill((white))
        if self.canvas:
            self.canvas.fill((black))
            self.draw_alignment_guides()
            self.app_interface.system.window.blit(self.canvas,self.canvas_rect)
            for element in self.canvas_elements:
                element.draw()
            

        if self.widget_palette:
            self.widget_palette.fill((beige))
            self.app_interface.system.window.blit(self.widget_palette,self.widget_palette_rect)

        if self.options:
            self.options.fill((light_gray))
            self.app_interface.system.window.blit(self.options,self.options_rect)

        
