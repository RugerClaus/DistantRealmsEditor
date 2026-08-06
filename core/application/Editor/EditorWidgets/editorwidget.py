class EditorWidget:
    def __init__(self, editor, data):
        self.editor = editor
        self.system = editor.app_interface.system

        self.data = data

        self.id = data.get("id", "")
        self.type = data.get("type", "")

        self.position = tuple(
            data.get("position", [0.5, 0.5])
        )

        self.rect = None

    def set_position(self, position):
        self.position = tuple(position)
        self.data["position"] = list(position)
        self.scale()

    def contains_point(self, point):
        return self.rect and self.rect.collidepoint(point)

    def set_property(self, name, value):
        setter = getattr(self, f"set_{name}", None)

        if setter:
            setter(value)

    def save_property(self, name, value):
        self.data[name] = value