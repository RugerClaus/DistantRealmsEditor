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
            self.editor.app_interface.ui_controller.show_ui("menu_editor_button_hover_style_properties")
            self.editor.update_fields()
        elif self.editor.button_style_state.is_state(BUTTON_STYLE_STATE.HOVER):
            self.editor.button_style_state.set_state(BUTTON_STYLE_STATE.IDLE)
            self.editor.app_interface.ui_controller.show_ui("menu_editor_button_idle_style_properties")
            self.editor.update_fields()
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

    def populate_button_style_fields(self, styles):
        fields = {}

        for style_name, value in styles.items():

            if style_name in self.button_color_properties:
                fields[f"{style_name}_r"] = str(value[0])
                fields[f"{style_name}_g"] = str(value[1])
                fields[f"{style_name}_b"] = str(value[2])

            else:
                fields[style_name] = str(value)

        return fields


    def collect_button_style_fields(self, properties):

        styles = {}

        colors = {
            "background",
            "border",
            "text_color"
        }

        for name in list(properties.keys()):

            if name in colors:
                continue

            if name.endswith("_r"):
                base = name[:-2]

                r = int(properties.pop(f"{base}_r"))
                g = int(properties.pop(f"{base}_g"))
                b = int(properties.pop(f"{base}_b"))

                styles[base] = [r, g, b]

        return styles