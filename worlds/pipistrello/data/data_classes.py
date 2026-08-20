from dataclasses import dataclass, field


@dataclass
class RoomData:
    room_label: str
    """The full room label in the spreadsheet (e.g. South Plaza (X-2, Y-3) - ren223 (Main))."""
    room_area: str
    """The map area in-game (e.g. South Plaza)."""
    region_name: str
    """The Archipelago region name."""
    global_room_id: str
    """The global room ID (e.g. city/ren223 (Main))."""
    sort_key: str
    """The custom sort key for the room."""


@dataclass
class ConnectionData:
    start_region_name: str
    """The connection start's Archipelago region name."""
    end_region_name: str
    """The connection end's Archipelago region name."""
    rule_strs: list[str]
    """The list of rule strings."""


@dataclass
class LocationData:
    region_name: str
    """The Archipelago region name."""
    location_name: str
    """The Archipelago location name (excluding region name)."""
    global_object_id: str
    """The global object ID in-game (e.g. city/ren223/yug2063)."""
    map_name: str
    """The Canva map name (e.g. Moneybag 1)."""
    room_area: str
    """The map area in-game (e.g. South Plaza)."""
    rule_strs: list[str]
    """The list of rule strings."""
    full_location_name: str = field(init=False, repr=False)
    """The full Archipelago location name (including region name)."""

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"


@dataclass
class EventData:
    region_name: str
    """The Archipelago region name."""
    location_name: str
    """The Archipelago location name (excluding region name)."""
    global_object_id: str
    """The global object ID in-game (e.g. city/ren223/yug5535)."""
    map_name: str
    """The Canva map name (e.g. Moneybag 1)."""
    room_area: str
    """The map area in-game (e.g. South Plaza)."""
    rule_strs: list[str]
    """The list of rule strings."""
    full_location_name: str = field(init=False, repr=False)
    """The full Archipelago location name (including region name)."""
    full_item_name: str = field(init=False, repr=False)
    """The full Archipelago item name (including region/location name)."""

    def __post_init__(self) -> None:
        self.full_location_name = f"{self.region_name}: {self.location_name}"
        self.full_item_name = self.full_location_name
