from core.state.ApplicationLayer.Editor.Button.Style.state import BUTTON_STYLE_STATE
from core.state.RuntimeLayer.UI.Button.state import BUTTON_STATE

class WidgetUtility:

    def __init__(self,editor):
        self.editor = editor

        self.button_color_properties = {
            "background": "background",
            "border": "border",
            "text_color": "text_color"
        }

    def toggle_button_style_state(self):
        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.IDLE):
            self.editor.button_style_state.set_state(BUTTON_STYLE_STATE.HOVER)
            self.editor.app_interface.ui_controller.show_ui("menu_editor_button_hover_properties")
            self.editor.update_fields()
        elif self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.HOVER):
            self.editor.button_style_state.set_state(BUTTON_STYLE_STATE.IDLE)
            self.editor.app_interface.ui_controller.show_ui("menu_editor_button_idle_properties")
            self.editor.update_fields()
        self.editor.refresh_selected_element()
        self.editor.show_selected_properties()

    def default_button_styles(self):
        return {
            "idle": {
                "background": [40, 40, 40],
                "border": [255, 255, 255],
                "border_width": 2,
                "border_radius": 8,
                "text_color": [255, 255, 255],
                "padding": 5
            },
            "hover": {
                "background": [60, 60, 60],
                "border": [200, 20, 20],
                "border_width": 3,
                "border_radius": 8,
                "text_color": [255, 255, 255],
                "padding": 5
            },
            "press": {
                "background": [20, 20, 20],
                "border": [255, 255, 255],
                "border_width": 2,
                "border_radius": 8,
                "text_color": [255, 255, 255],
                "padding": 5
            },
            "disable": {
                "background": [20, 20, 20],
                "border": [100, 100, 100],
                "border_width": 2,
                "border_radius": 8,
                "text_color": [100, 100, 100],
                "padding": 5
            },
            "focused": {
                "background": [40, 40, 40],
                "border": [0, 255, 255],
                "border_width": 3,
                "border_radius": 8,
                "text_color": [255, 255, 255],
                "padding": 5
            }
        }

    def populate_color_fields(self, element):
        fields = {}

        if element.type == "button":
            style_state = self.editor.button_style_state.state.name.lower()
            styles = element.data["styles"].get(style_state, {})

            for name, value in styles.items():
                if name in self.button_color_properties:
                    fields[f"{name}_r"] = str(value[0])
                    fields[f"{name}_g"] = str(value[1])
                    fields[f"{name}_b"] = str(value[2])
                else:
                    fields[name] = str(value)

        elif "color" in element.data:
            r, g, b = element.data["color"]
            fields["color_r"] = str(r)
            fields["color_g"] = str(g)
            fields["color_b"] = str(b)

        return fields

    def get_button_runtime_style_state(self):
        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.IDLE):
            return BUTTON_STATE.IDLE

        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.HOVER):
            return BUTTON_STATE.HOVER

        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.PRESS):
            return BUTTON_STATE.PRESS

        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.DISABLE):
            return BUTTON_STATE.DISABLE

        if self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.FOCUSED):
            return BUTTON_STATE.FOCUSED 

    def populate_color_fields(self, element):

        fields = {}

        if element.type == "button":
            style_name = self.editor.button_style_state.state.name.lower()

            styles = element.data["styles"].get(style_name, {})

            for name, value in styles.items():

                if name in self.button_color_properties:
                    fields[f"{name}_r"] = str(value[0])
                    fields[f"{name}_g"] = str(value[1])
                    fields[f"{name}_b"] = str(value[2])
                else:
                    fields[name] = str(value)

        elif "color" in element.data:
            r, g, b = element.data["color"]

            fields["color_r"] = str(r)
            fields["color_g"] = str(g)
            fields["color_b"] = str(b)

        return fields

    def collect_color_properties(self, element, properties):

        collected = {}

        if element.type == "button":

            for base in self.button_color_properties:

                r = properties.pop(f"{base}_r", None)
                g = properties.pop(f"{base}_g", None)
                b = properties.pop(f"{base}_b", None)

                if r is not None and g is not None and b is not None:
                    collected[base] = (
                        int(r or 0),
                        int(g or 0),
                        int(b or 0)
                    )

        else:

            r = properties.pop("color_r", None)
            g = properties.pop("color_g", None)
            b = properties.pop("color_b", None)

            if r is not None and g is not None and b is not None:
                collected["color"] = (
                    int(r or 0),
                    int(g or 0),
                    int(b or 0)
                )

        return collected