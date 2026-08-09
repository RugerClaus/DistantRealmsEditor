import ast
from core.util.colors import *
from core.application.Editor.EditorWidgets.widgetutility import WidgetUtility
from core.application.Editor.EditorWidgets.editorbutton import EditorButton
from core.application.Editor.EditorWidgets.editorlabel import EditorLabel
from core.application.Editor.EditorWidgets.editorheader import EditorHeader
from core.application.Editor.EditorWidgets.editorcentertext import EditorCenterText
from core.application.Editor.EditorWidgets.editorimage import EditorImage
from core.application.Editor.EditorWidgets.editorquery import EditorQuery
from core.application.Editor.EditorWidgets.editorscrollabletext import EditorScrollableText
from core.application.Editor.EditorWidgets.editorselect import EditorSelect
from core.application.Editor.EditorWidgets.editortextbox import EditorTextBox

from core.state.ApplicationLayer.Editor.Button.Style.state import BUTTON_STYLE_STATE
from core.state.ApplicationLayer.Editor.Button.Style.statemanager import ButtonStyleStateManager

from core.state.ApplicationLayer.Editor.state import EDITOR_STATE

class UIEditor:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        system = app_interface.system

        system.input.CommandModule.sequences["save_project"] = [system.input.keys.l_ctrl_key(),system.input.keys.s_key()]
        system.input.CommandModule.sequences["delete_element"] = [system.input.keys.delete_key()]

        self.active_file = None
        self.active_filename = None

        self.button_style_state = ButtonStyleStateManager()

        self.widgets = WidgetUtility(self)

        self.selected_element = None
        self.dragging = False
        self.drag_offset = None
        self.canvas_elements = []
        self.element_types = {
            "button": EditorButton,
            "label": EditorLabel,
            "textbox": EditorTextBox,
            "header": EditorHeader,
            "image": EditorImage,
            "query": EditorQuery,
            "centertext": EditorCenterText,
            "scrollable_text": EditorScrollableText,
            "select": EditorSelect
            }
        self.load_canvas()
        self.load_widget_palette()
        self.load_options()

    def create_editor_element(self, data):
        element_type = data.get("type")

        element_class = self.element_types.get(element_type)

        if element_class is None:
            if element_type == "image":
                return None

            raise ValueError(
                f"Unknown editor element type: {element_type}"
            )

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
                "font_size": 30,
                "action": None,
                "styles": self.widgets.default_button_styles()
            },

            "label": {
                "id": "new_label",
                "type": "label",
                "text": "Label",
                "position": [0.5, 0.5],
                "font_size": 30,
                "color": [255, 255, 255]
            },
            "header": {
                "id": "new_header",
                "type": "header",
                "text": "Header",
                "position": [0.5, 0.1],
                "font_size": 60,
                "color": [255, 255, 255]
            },
            "query": {
                "id": "new_query",
                "type": "query",
                "text": "Query",
                "position": [0.5,0.5],
                "font_size": 20,
                "color": [255,255,255]
            },
            "scrollable_text": {
                "id": "new_stxt",
                "type": "scrollable_text",
                "text": "",
                "position": [0.5,0.5],
                "color": [255,255,255],
                "width": 0.4,
                "height":0.4,
                "align": "left",
                "line_spacing": 0.01,
                "font_size": 20
            },
            "textbox": {
                "type": "textbox",
                "id": "new_textbox",
                "field": "default",
                "position": [0.1, 0.83],
                "dimensions": [0.1, 0.03],
                "font_size": 25,
                "max_chars": 21
            },
            "select": {
                "type": "select",
                "id": "new_select",
                "options": ["Option 1", "Option 2", "Option 3"],
                "selected_option": "Option 1",
                "position": [0.5, 0.5],
                "font_size": 30,
                "width": 0.1,
                "height": 0.05,
                "padding": 10,
                "field": "default"
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

    def delete_selected_element(self):
        if self.selected_element is None:
            return

        element = self.selected_element

        if element in self.canvas_elements:
            self.canvas_elements.remove(element)

        if self.active_file is not None:
            elements = self.active_file.get("elements", [])

            if element.data in elements:
                elements.remove(element.data)

        self.selected_element = None
        self.dragging = False
        self.drag_offset = None

        if self.app_interface.app_object.state.is_state(EDITOR_STATE.MENU):
            self.app_interface.ui_controller.show_ui("editor_noprops")
        elif self.app_interface.app_object.state.is_state(EDITOR_STATE.FORM):
            self.app_interface.ui_controller.show_ui("form_editor_noprops")

        self.dirty = True
        self.save()

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

    def refresh_selected_element(self):
        element = self.selected_element

        if element and element.type == "button":
            element.scale()

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

    def update_fields(self):
        if self.selected_element is None:
            return

        x, y = self.selected_element.data.get(
            "position",
            [0.5, 0.5]
        )

        fields = {
            "x": str(round(x * 100, 2)),
            "y": str(round(y * 100, 2)),
            "id": self.selected_element.data.get("id", ""),
            "font_size": self.selected_element.data.get("font_size", ""),
            "text": self.selected_element.data.get("text", "")
        }

        if self.selected_element.type == "scrollable_text":
            fields["width"] = str(
                self.selected_element.data.get("width", 0.8)
            )
            fields["height"] = str(
                self.selected_element.data.get("height", 0.6)
            )

        
        if self.selected_element.type == "select":
            fields["width"] = str(
                self.selected_element.data.get("width", 0.3)
            )

            fields["height"] = str(
                self.selected_element.data.get("height", 0.06)
            )

            fields["field"] = self.selected_element.data.get(
                "field",
                "default"
            )

            fields["options"] = str(
                self.selected_element.data.get(
                    "options",
                    ["Option 1", "Option 2", "Option 3"]
                )
            )

            fields["selected_option"] = str(
                self.selected_element.data.get(
                    "selected_option",
                    ""
                )
            )


        if self.selected_element.type == "textbox":
            w, h = self.selected_element.data.get(
                "dimensions",
                [0.5, 0.5]
            )

            fields["field"] = self.selected_element.data.get(
                "field",
                "default"
            )

            fields["max_chars"] = str(
                self.selected_element.data.get(
                    "max_chars",
                    100
                )
            )

            fields["width"] = str(w)
            fields["height"] = str(h)

        if self.selected_element.type == "button":
            fields["action"] = self.selected_element.data.get("action", "")

        fields.update(
            self.widgets.populate_color_fields(self.selected_element)
        )

        for name, value in fields.items():
            field = self.app_interface.ui_controller.get_element(name)
            if field:
                field.set_text(value)

    def show_selected_properties(self):
        if self.selected_element is None:
            if self.app_interface.app_object.state.is_state(EDITOR_STATE.MENU):
                self.app_interface.ui_controller.show_ui("editor_noprops")
            elif self.app_interface.app_object.state.is_state(EDITOR_STATE.FORM):
                self.app_interface.ui_controller.show_ui("form_editor_noprops")
            return

        element_type = self.selected_element.data.get("type")

        if self.app_interface.app_object.state.is_state(EDITOR_STATE.MENU):
            if element_type == "button":
                if self.button_style_state.is_state(BUTTON_STYLE_STATE.IDLE):
                    menu = "menu_editor_button_idle_properties"
                elif self.button_style_state.is_state(BUTTON_STYLE_STATE.HOVER):
                    menu = "menu_editor_button_hover_properties"
            elif element_type == "label":
                menu = "menu_editor_label_properties"
            elif element_type == "header":
                menu = "menu_editor_header_properties"
            elif element_type == "query":
                menu = "menu_editor_query_properties"
            elif element_type == "scrollable_text":
                menu = "menu_editor_stext_properties"
            else:
                menu = "editor_noprops"
                return

        elif self.app_interface.app_object.state.is_state(EDITOR_STATE.FORM):
            if element_type == "button":
                if self.button_style_state.is_state(BUTTON_STYLE_STATE.IDLE):
                    menu = "form_editor_button_idle_properties"
                elif self.button_style_state.is_state(BUTTON_STYLE_STATE.HOVER):
                    menu = "form_editor_button_hover_properties"
            elif element_type == "label":
                menu = "form_editor_label_properties"
            elif element_type == "header":
                menu = "form_editor_header_properties"
            elif element_type == "query":
                menu = "form_editor_query_properties"
            elif element_type == "scrollable_text":
                menu = "form_editor_stext_properties"
            elif element_type == "textbox":
                menu = "form_editor_input_properties"
            elif element_type == "select":
                menu = "form_editor_select_properties"
            else:
                menu = "form_editor_noprops"
                return

        self.app_interface.ui_controller.show_ui(menu)

        self.update_fields()

    def handle_event(self, event,command):

        if command == "save_project":
            self.update_widget_properties(self.app_interface.ui_controller.get_active_ui().submit())
            self.save()
        elif command == "delete_element":
            self.delete_selected_element()

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
                        if self.selected_element != element:
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
                    if self.app_interface.app_object.state.is_state(EDITOR_STATE.MENU):
                        self.app_interface.ui_controller.show_ui("editor_noprops")
                    elif self.app_interface.app_object.state.is_state(EDITOR_STATE.FORM):
                        self.app_interface.ui_controller.show_ui("form_editor_noprops")
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

        self.update_fields()

    def update_widget_properties(self, properties):
        element = self.selected_element

        if element is None:
            return

        style_name = self.button_style_state.state.name.lower()

        properties.update(
            self.widgets.collect_color_properties(
                element,
                properties
            )
        )

        if "x" in properties:
            element.set_position((
                float(properties.pop("x")) / 100,
                element.data["position"][1]
            ))

        if "y" in properties:
            element.set_position((
                element.data["position"][0],
                float(properties.pop("y")) / 100
            ))

        if "id" in properties:
            element.set_id(str(properties.pop("id")))

        if "font_size" in properties:
            element.set_font_size(
                int(properties.pop("font_size"))
            )

        if "text" in properties:
            element.set_text(
                str(properties.pop("text"))
            )

        if "color" in properties and hasattr(element, "set_color"):
            element.set_color(
                tuple(properties.pop("color"))
            )

        if element.type == "button":

            if "action" in properties:
                element.data["action"] = properties.pop("action")

            for name, value in properties.items():

                if name not in element.styles.get(style_name, {}):
                    continue

                if name in (
                    "background",
                    "border",
                    "text_color"
                ):
                    value = tuple(value)

                elif name in (
                    "border_width",
                    "border_radius",
                    "padding"
                ):
                    value = int(value)

                element.set_style(
                    style_name,
                    name,
                    value
                )

        elif element.type == "textbox":

            if "width" in properties or "height" in properties:
                width, height = element.data.get(
                    "dimensions",
                    [0.5, 0.5]
                )

                if "width" in properties:
                    width = float(
                        properties.pop("width")
                    )

                if "height" in properties:
                    height = float(
                        properties.pop("height")
                    )

                element.set_dimensions(
                    (width, height)
                )

            if "field" in properties:
                element.set_field(
                    properties.pop("field")
                )
            
            if "max_chars" in properties:
                element.set_max_chars(
                    properties.pop("max_chars")
                )

        elif element.type == "select":

            if "width" in properties:
                element.set_width(
                    float(properties.pop("width"))
                )

            if "height" in properties:
                element.set_height(
                    float(properties.pop("height"))
                )

            if "padding" in properties:
                element.set_padding(
                    int(properties.pop("padding"))
                )

            if "options" in properties:
                options = properties.pop("options")

                # The form field contains the Python-style
                # list as text, so convert it back into a list.
                if isinstance(options, str):
                    try:
                        options = ast.literal_eval(options)
                    except (ValueError, SyntaxError):
                        options = [
                            option.strip()
                            for option in options.split(",")
                            if option.strip()
                        ]

                if not isinstance(options, list):
                    options = [str(options)]

                element.set_options(options)

            if "selected_option" in properties:
                element.set_selected_option(
                    properties.pop("selected_option")
                )

        else:

            for name, value in properties.items():
                setter = getattr(
                    element,
                    f"set_{name}",
                    None
                )

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

        
    def clean_up_states(self):
        self.app_interface.system.clean_up_states([self.button_style_state.state])