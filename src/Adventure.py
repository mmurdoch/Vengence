"""
A playground in which to try out text adventure ideas.
"""
from Direction import Direction
from Game import Game
from Room import Room

def create_directions(direction_data):
    """
    Creates the directions in the game.

    direction_data: Details of the directions in the game
    """
    directions = []
    for datum in direction_data:
        direction = Direction(datum["name"])
        opposite_direction = Direction(datum["opposite"])
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        directions.append(direction)
        directions.append(opposite_direction)

    return directions


def create_rooms(room_data):
    """
    Creates the rooms in the game.

    room_data: Details of the rooms in the game
    """
    rooms = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room = Room(room_name, room_datum['description'])
        rooms.append(room)

    return rooms


def create_exit_data(room_data):
    """
    Creates exit data for the game.

    room_data: Details of the rooms in the game
    """
    exit_data = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room_datum.setdefault('exits', [])
        for current_exit in room_datum['exits']:
            exit_datum = {
                'from': room_name,
                'to': current_exit['to'],
                'direction': current_exit['direction']
            }
            exit_data.append(exit_datum)

    return exit_data


def find_room(name, rooms):
    """
    Finds a room by name.

    Returns the room or None if the room was not found.

    name: The name of the room to find
    rooms: The rooms in which to search
    """
    for room in rooms:
        if room.name == name:
            return room

    return None


def add_exits(rooms, directions, exit_data):
    """
    Adds exits to rooms.

    rooms: The rooms to which to add exits
    directions: The directions in which exits can lead
    exit_data: Details of the exits in the game
    """
    for datum in exit_data:
        from_name = datum["from"]
        from_room = find_room(from_name, rooms)
        to_name = datum["to"]
        to_room = find_room(to_name, rooms)
        if to_room is None:
            print("Unknown exit room '" + to_name +
                  "' from '" + from_name + "'")
            sys.exit()

        direction_name = datum["direction"]
        the_exit = None
        for direction in directions:
            if direction.name == direction_name:
                the_exit = direction
        if the_exit is None:
            print("Unknown direction '" + direction_name + "'")
            sys.exit()

        datum.setdefault('one_way', False)
        one_way = datum["one_way"]
        add_exit_func = None
        if one_way:
            add_exit_func = Room.add_one_way_exit
        else:
            add_exit_func = Room.add_exit
        add_exit_func(from_room, the_exit, to_room)


def run_game(game_data):
    """
    Runs the game.

    game_data: Details of the rooms in the game
    """
    directions = create_directions(game_data['directions'])
    room_data = game_data['rooms']
    rooms = create_rooms(room_data)
    exit_data = create_exit_data(room_data)
    add_exits(rooms, directions, exit_data)

    if len(rooms) > 0:
        game = Game(rooms[0])
        game.run()

run_game({
    'directions': [
        {'name': 'up', 'opposite': 'down'},
        {'name': 'in', 'opposite': 'out'},
        {'name': 'west', 'opposite': 'east'}
    ],
    'rooms': [
        {'name': 'A Church',
         'description': 'Tiny place of worship',
         'exits': [
             {'to': 'The Crypt', 'direction': 'down'}
         ]},
        {'name': 'The Crypt',
         'description': 'Dusty tomb filled with empty sarcophagi',
         'exits': [
             {'to': 'A Coffin', 'direction': 'in', 'one_way': True},
             {'to': 'A Cave', 'direction': 'west'}
         ]},
        {'name': 'A Coffin',
         'description': 'A tight squeeze and pitch dark'},
        {'name': 'A Cave',
         'description': 'A dark and dingy place'}
    ],
})