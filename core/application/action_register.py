from systemlogging import log_event

class ActionRegistrar:
    def __init__(self, app_interface):
        self.app_interface = app_interface
        self.system = app_interface.system

    def register(self):
        self.app_interface.actions.register("create_project",self.app_interface.app_object.util.create_project)

        self.app_interface.actions.register("create_new_button", lambda: self.app_interface.app_object.editor.add_element("button"))
        self.app_interface.actions.register("create_new_label", lambda: self.app_interface.app_object.editor.add_element("label"))
        self.app_interface.actions.register("create_new_header", lambda: self.app_interface.app_object.editor.add_element("header"))

        #button editor:
        self.app_interface.actions.register("button_hover_style_mode", lambda: self.app_interface.app_object.editor.widgets.toggle_button_style_state())
        self.app_interface.actions.register("button_idle_style_mode", lambda: self.app_interface.app_object.editor.widgets.toggle_button_style_state())

        self.app_interface.actions.register(
            "update_widget_properties",
            lambda: self.app_interface.app_object.editor.update_widget_properties(
                self.app_interface.ui_controller.get_active_ui().submit()
            )
        )
        self.app_interface.actions.register("delete_selected_element", lambda: self.app_interface.app_object.editor.delete_selected_element())
        self.app_interface.actions.register("main_menu", self.app_interface.app_object.navigation.main_menu)

        self.app_interface.actions.register("new_project_form",lambda: self.app_interface.ui_controller.show_ui("newprojectform"))
        self.app_interface.actions.register("load_project", self.app_interface.app_object.initialize_project_browser)

        self.app_interface.actions.register("open_settings", lambda: self.app_interface.ui_controller.show_ui("editor_settings_root"))
        self.app_interface.actions.register("audio_settings", lambda: self.app_interface.ui_controller.show_ui("editor_audio_settings"))

        self.app_interface.actions.register("quit",self.system.quit)
