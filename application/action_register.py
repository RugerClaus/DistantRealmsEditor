from systemlogging import log_event

class ActionRegistrar:
    def __init__(self, distant_realms):
        self.distant_realms = distant_realms
        self.system = distant_realms.system

    def register(self):
        self.distant_realms.actions.register("create_project",self.distant_realms.application.util.create_project)

        self.distant_realms.actions.register("create_new_button", lambda: self.distant_realms.application.editor.add_element("button"))
        self.distant_realms.actions.register("create_new_label", lambda: self.distant_realms.application.editor.add_element("label"))
        self.distant_realms.actions.register("create_new_header", lambda: self.distant_realms.application.editor.add_element("header"))
        self.distant_realms.actions.register("create_new_query", lambda: self.distant_realms.application.editor.add_element("query"))
        self.distant_realms.actions.register("create_new_stxt", lambda: self.distant_realms.application.editor.add_element("scrollable_text"))
        self.distant_realms.actions.register("new_input_box", lambda: self.distant_realms.application.editor.add_element("textbox"))
        self.distant_realms.actions.register("create_new_select_box", lambda: self.distant_realms.application.editor.add_element("select"))

        #button editor:
        self.distant_realms.actions.register("button_hover_style_mode", lambda: self.distant_realms.application.editor.widgets.toggle_button_style_state())
        self.distant_realms.actions.register("button_idle_style_mode", lambda: self.distant_realms.application.editor.widgets.toggle_button_style_state())

        self.distant_realms.actions.register(
            "update_widget_properties",
            lambda: self.distant_realms.application.editor.update_widget_properties(
                self.distant_realms.ui_controller.get_active_ui().submit()
            )
        )
        self.distant_realms.actions.register("delete_selected_element", lambda: self.distant_realms.application.editor.delete_selected_element())
        self.distant_realms.actions.register("main_menu", self.distant_realms.application.navigation.main_menu)

        self.distant_realms.actions.register("new_project_form",lambda: self.distant_realms.ui_controller.show_ui("newprojectform"))
        self.distant_realms.actions.register("load_ui_projects", self.distant_realms.application.initialize_ui_project_browser)
        self.distant_realms.actions.register("load_world_projects", self.distant_realms.application.initialize_world_project_browser)
        self.distant_realms.actions.register("load_cell_map_projects", self.distant_realms.application.initialize_cellmap_project_browser)

        self.distant_realms.actions.register("create_new_map_layer", lambda: self.distant_realms.application.editor.create_new_map_layer())

        self.distant_realms.actions.register("cancel_map_generation", lambda: self.distant_realms.application.editor.map_creator.hide())

        self.distant_realms.actions.register("save_and_quit_world_editor", lambda: self.distant_realms.application.navigation.save_and_quit_we())
        self.distant_realms.actions.register("save_and_quit_cellmap_editor", lambda: self.distant_realms.application.navigation.save_and_quit_cme())

        self.distant_realms.actions.register("open_settings", lambda: self.distant_realms.ui_controller.show_ui("editor_settings_root"))
        self.distant_realms.actions.register("audio_settings", lambda: self.distant_realms.ui_controller.show_ui("editor_audio_settings"))

        self.distant_realms.actions.register("mvolup", self.distant_realms.system.sound.volume_up)
        self.distant_realms.actions.register("mvoldown", self.distant_realms.system.sound.volume_down)

        self.distant_realms.actions.register("sfxvolup", self.distant_realms.system.sound.sfx_volume_up)
        self.distant_realms.actions.register("sfxvoldown", self.distant_realms.system.sound.sfx_volume_down)

        self.distant_realms.actions.register("quit",self.system.quit)
