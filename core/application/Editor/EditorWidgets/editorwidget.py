class EditorWidget:
    def __init__(self, editor, data):
        self.editor = editor
        self.system = editor.app_interface.system

        self.data = data

        self.id = data.get("id", "")
        self.type = data.get("type", "")
        self.font_size = data.get("font_size", "")
        self.color = tuple(data.get("color", ""))

        self.position = tuple(
            data.get("position", [0.5, 0.5])
        )

        self.rect = None

    def contains_point(self, point):
        return self.rect and self.rect.collidepoint(point)

    def set_property(self, name, value):
        setter = getattr(self, f"set_{name}", None)

        if setter:
            setter(value)

    def save_property(self, name, value):
        self.data[name] = value

    def set_id(self, id):
        self.id = str(id)
        self.data["id"] = self.id

    def set_font_size(self, fs):
        self.font_size = int(fs)
        self.data["font_size"] = self.font_size
        self.scale()

    def set_text(self, text):
        self.text = str(text)
        self.data["text"] = self.text
        self.scale()

    def set_position(self, position):
        self.position = tuple(position)
        self.data["position"] = list(position)
        self.scale()

    def set_color(self,color):
        self.color = tuple(color)
        self.data["color"] = list(color)
        self.scale()