"""
Vengeance - text adventure game engine.
"""
from vengeance._direction import _Direction
from vengeance._game import _Game
from vengeance._room import _Room
from vengeance.game import GameFormatException


class _Struct:
    # Disable 'Too few public methods'
    # pylint: disable=R0903
    """
    A structure based on a dictionary.
    """
    def __init__(self, **entries):
        """
        :param self: The instance to initialize
        :param entries: The dictionary entries to be accessed
        """
        self.__dict__.update(entries)


def _direction_name_key():
    """
    :returns: The dictionary key for a direction name
    """
    return 'name'


def _direction_opposite_key():
    """
    :returns: The dictionary key for a direction opposite
    """
    return 'opposite'


def _create_directions(direction_data):
    """
    Creates the directions in the game.

    direction_data: Details of the directions in the game
    """
    directions = []
    for datum in direction_data:
        _check_direction_well_formed(datum)

        # Disable 'Used * or ** magic
        # pylint: disable=W0142
        direction = _Struct(**datum)
        direction_names = [d.name for d in directions]
        _check_direction_valid(direction, direction_names)

        # Disable 'Instance of '_Struct' has no 'name' member
        # Disable 'Instance of '_Struct' has no 'opposite' member
        # pylint: disable=E1101
        name = direction.name
        opposite = direction.opposite

        reserved_word = 'quit'
        name_key = _direction_name_key()
        _check_if_direction_is_reserved(reserved_word, name, name_key)
        opposite_key = _direction_opposite_key()
        _check_if_direction_is_reserved(reserved_word, opposite, opposite_key)

        direction = _Direction(name)
        opposite_direction = _Direction(opposite)
        direction.opposite = opposite_direction
        opposite_direction.opposite = direction
        directions.append(direction)
        directions.append(opposite_direction)

    return directions


def _check_direction_well_formed(direction):
    """
    Checks the structure of a direction dictionary.

    :param dict direction: The direction to check
    :raises: ``GameFormatException`` if direction structure is invalid
    """
    name_key = _direction_name_key()
    opposite_key = _direction_opposite_key()

    if name_key not in direction:
        if opposite_key not in direction:
            message = u'Missing name and opposite from direction'
            raise GameFormatException(message)
        else:
            message = u'Missing name from direction with opposite "{0}"'
            raise GameFormatException(message.format(direction[opposite_key]))
    elif opposite_key not in direction:
        message = u'Missing opposite from direction with name "{0}"'
        raise GameFormatException(message.format(direction[name_key]))


def _check_direction_valid(direction, direction_names):
    """
    Checks the validity of a direction dictionary.

    :param dict direction: The direction to check
    :param list direction_names: The current set of direction names
    """
    if direction.name == direction.opposite:
        message = u'Direction "{0}" cannot be its own opposite'
        raise GameFormatException(message.format(direction.name))

    if direction.name in direction_names:
        message = u'Redefinition of direction "{0}"'
        raise GameFormatException(message.format(direction.name))

    if direction.opposite in direction_names:
        message = u'Redefinition of direction "{0}" as an opposite'
        raise GameFormatException(message.format(direction.opposite))


def _check_if_direction_is_reserved(reserved_word, to_check, to_check_key):
    """
    Checks if a direction is using a reserved word.

    :param str reserved_word: The reserved word to check
    :param str to_check: The direction to check
    :param str to_check_key: The direction dictionary key of ``to_check``
    :raises: ``GameFormatException`` if direction is using a reserved word
    """
    if to_check == reserved_word:
        message = u'Direction {0} cannot use reserved word "{1}"'
        raise GameFormatException(message.format(to_check_key, reserved_word))


def _create_rooms(room_data):
    """
    Creates the rooms in the game.

    room_data: Details of the rooms in the game
    """
    rooms = []
    for room_datum in room_data:
        room_name = room_datum['name']

        if room_name in [r.name for r in rooms]:
            message = u'Redefinition of room "{0}"'
            raise GameFormatException(message.format(room_name))

        room = _Room(room_name, room_datum['description'])
        rooms.append(room)

    return rooms


def _create_exit_data(room_data):
    """
    Creates exit data for the game.

    room_data: Details of the rooms in the game
    """
    exit_data = []
    for room_datum in room_data:
        room_name = room_datum['name']
        room_datum.setdefault('exits', [])
        for current_exit in room_datum['exits']:
            current_exit.setdefault('one_way', False)
            exit_datum = {
                'from': room_name,
                'to': current_exit['to'],
                'direction': current_exit['direction'],
                'one_way': current_exit['one_way']
            }
            exit_data.append(exit_datum)

    return exit_data


def _find_room(name, rooms):
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


def _add_exits(rooms, directions, exit_data):
    """
    Adds exits to rooms.

    rooms: The rooms to which to add exits
    directions: The directions in which exits can lead
    exit_data: Details of the exits in the game
    """
    for datum in exit_data:
        from_name = datum['from']
        from_room = _find_room(from_name, rooms)
        to_name = datum['to']
        to_room = _find_room(to_name, rooms)
        if to_room is None:
            print('Unknown exit room ' + to_name +
                  ' from ' + from_name + "'")
            #sys.exit()

        direction_name = datum['direction']
        the_exit = None
        for direction in directions:
            if direction.name == direction_name:
                the_exit = direction
        if the_exit is None:
            print('Unknown direction ' + direction_name)
            #sys.exit()

        one_way = datum['one_way']
        add_exit_func = None
        if one_way:
            add_exit_func = _Room.add_one_way_exit
        else:
            add_exit_func = _Room.add_exit
        add_exit_func(from_room, the_exit, to_room)


def _load_rooms(game_data):
    """
    Loads rooms, and wires up their exits.

    game_data: Details of the rooms in the game
    """
    if 'directions' not in game_data:
        raise GameFormatException(u'Missing "directions" list')

    directions = _create_directions(game_data['directions'])
    room_data = game_data['rooms']
    rooms = _create_rooms(room_data)
    exit_data = _create_exit_data(room_data)
    _add_exits(rooms, directions, exit_data)

    return rooms


def _create_game(game_data):
    """
    Creates a game.

    :param dict game_data: Details of the rooms in the game
    :raises: GameFormatException if the ``game_data`` structure is invalid
    """
    if not isinstance(game_data, dict):
        raise GameFormatException(u'game_data must be a dictionary')

    rooms = _load_rooms(game_data)

    if len(rooms) > 0:
        return _Game(rooms[0])

    return None


def run_game(game_data):
    """
    Runs a game.

    :param dict game_data: Details of the rooms in the game
    :raises: ``GameFormatException`` if the ``game_data`` structure is invalid

    ``game_data`` is a dictionary containing two key-value pairs, one with key
    ``'directions'`` and the other with key ``'rooms'``. Each of these keys
    has a list as its value.

    The ``'directions'`` list contains a sequence of dictionaries, each with
    two key-value pairs: one with key ``'name'`` and the other with key
    ``'opposite'``. The values of each key are strings which the player can
    type to move in that direction. All direction ``'name'`` and
    ``'opposite'`` values must be unique.

    The ``'rooms'`` list also contains a sequence of dictionaries. Each of
    these dictionaries must contain a ``'name'`` key with a string value. No
    two rooms can have the same name. Each dictionary must also contain a
    ``'description'`` key which again must have a string value. In addition,
    each dictionary may optionally contain an ``'exits'`` key.

    The value of the ``'exits'`` key is (again!) a list of dictionaries which
    contain a ``'to'`` key (the value of which must be the ``'name'`` of a
    room) and a ``'direction'`` key (the value of which must contain the
    ``'name'`` or ``'opposite'`` of a direction). Also, optionally, each
    dictionary may contain a ``'one_way'`` key, the value of which must be a
    boolean (the default is ``False``).

    Phew! An example might help::

        vengeance.run_game({
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

    """
    game = _create_game(game_data)
    game.run()