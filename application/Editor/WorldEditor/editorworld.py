from core.engine.world.loader import MapLoader

class EditorWorld:

    def __init__(self, system):

        self.system = system
        self.maps = []

        self.view_x = 0
        self.view_y = 0
        self.view_width = 9
        self.view_height = 9

        self.map_loader = MapLoader(system, None)

        self.filename = None

    def load(self, filename):

        self.filename = filename
        self.maps.clear()

        loader = MapLoader(self.system, None)
        self.maps = loader.load(filename)

        if not self.maps:
            self.view_x = 0
            self.view_y = 0
            self.view_width = 1
            self.view_height = 1
            return

        self.view_x = min(map.world_x for map in self.maps)
        self.view_y = min(map.world_y for map in self.maps)

        right = max(
            map.world_x + map.map_width
            for map in self.maps
        )

        bottom = max(
            map.world_y + map.map_height
            for map in self.maps
        )

        self.view_width = right - self.view_x
        self.view_height = bottom - self.view_y

    def save(self):

        if self.filename is None:
            return

        base_path = self.system.os.path.dirname(self.filename)

        print("EDITOR WORLD SAVE")
        print("  filename:", self.filename)
        print("  maps:", len(self.maps))

        for map in self.maps:

            if not hasattr(map, "filename") or map.filename is None:
                print(f"  map: {map.name}")
                print("    ERROR: map has no filename")
                continue

            filepath = self.system.os.path.join(
                base_path,
                map.filename
            )

            print(f"  map: {map.name}")
            print(f"    saving: {filepath}")

            with open(filepath, "w") as file:
                for row in map.cell_map:
                    file.write(
                        ",".join(str(cell) for cell in row) + "\n"
                    )

        print("Saved world to", self.filename)

    def add_map(self, map):
        self.maps.append(map)

    def get_maps_at(self, world_x, world_y):

        return [
            map for map in self.maps
            if map.world_x == world_x
            and map.world_y == world_y
        ]
