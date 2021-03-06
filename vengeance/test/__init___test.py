import unittest

import vengeance
from vengeance import game


class InitTest(unittest.TestCase):

    def test_game_data_none_raises(self):
        self.assert_run_game_raises(None, 'game_data must be a dictionary')

    def test_game_data_not_dictionary_raises(self):
        self.assert_run_game_raises([], 'game_data must be a dictionary')

    def test_missing_directions_raises(self):
        self.assert_run_game_raises({
        }, 'Missing directions list')

    def test_matching_direction_name_and_opposite_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'up', 'opposite': 'up'}
            ]
        }, 'Direction "up" cannot be its own opposite')

    def test_non_unique_direction_name_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'east', 'opposite': 'west'},
                {'name': 'east', 'opposite': 'north'}
            ]
        }, 'Redefinition of direction "east"')

    def test_non_unique_opposite_direction_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
                {'name': 'in', 'opposite': 'down'}
            ]
        }, 'Redefinition of direction "down" as an opposite')

    def test_direction_name_redefined_as_opposite_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'north', 'opposite': 'south'},
                {'name': 'west', 'opposite': 'north'}
            ]
        }, 'Redefinition of direction "north" as an opposite')

    def test_direction_opposite_redefined_as_name_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'in', 'opposite': 'out'},
                {'name': 'out', 'opposite': 'down'}
            ]
        }, 'Redefinition of direction "out"')

    def test_missing_direction_name_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'opposite': 'in'}
            ]
        }, 'Missing name from direction with opposite "in"')

    def test_missing_direction_opposite_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'west'}
            ]
        }, 'Missing opposite from direction with name "west"')

    def test_missing_name_and_opposite_from_direction_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {}
            ]
        }, 'Missing name and opposite from direction')

    def test_direction_name_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': False, 'opposite': 'down'}
            ]
        }, 'Direction name must be a string')

    def test_direction_opposite_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'up', 'opposite': []}
            ]
        }, 'Direction opposite must be a string')

    def test_use_of_quit_as_direction_name_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'quit', 'opposite': 'north'}
            ]
        }, 'Direction name cannot use reserved word "quit"')

    def test_use_of_quit_as_direction_opposite_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'up', 'opposite': 'quit'}
            ]
        }, 'Direction opposite cannot use reserved word "quit"')

    def test_non_unique_room_name_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'Entrance Hall', 'description': 'A description'},
                {'name': 'Entrance Hall', 'description': 'B description'}
            ]
        }, 'Redefinition of room "Entrance Hall"')

    def test_missing_rooms_raises(self):
        self.assert_run_game_raises({
            'directions': []
        }, 'Missing rooms list')

    def test_zero_rooms_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': []
        }, 'Rooms list must contain at least one room')

    def test_missing_room_name_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'description': 'No name'}
            ]
        }, 'Missing name from room with description "No name"')

    def test_room_name_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': {}, 'description': 'Bad name'}
            ]
        }, 'Room name must be a string')

    def test_missing_room_description_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'No Description'}
            ]
        }, 'Missing description from room with name "No Description"')

    def test_room_description_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'Bad Description', 'description': []}
            ]
        }, 'Room description must be a string')

    def test_missing_room_name_and_description_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {}
            ]
        }, 'Missing name and description from room')

    def test_missing_exit_to_room_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'left', 'opposite': 'right'}
            ],
            'rooms': [
                {'name': 'T-Junction',
                 'description': 'A fork in the road',
                 'exits': [
                     {'direction': 'right'}
                 ]}
            ]
        }, 'Missing to room from exit with direction '
           '"right" from room "T-Junction"')

    def test_missing_exit_direction_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'The Cellar',
                 'description': 'A dark, damp basement',
                 'exits': [
                     {'to': 'The Sewers'}
                 ]},
                {'name': 'The Sewers',
                 'description': 'The city waste disposal system'}
            ]
        }, 'Missing direction from exit to room "The Sewers" '
           'from room "The Cellar"')

    def test_missing_exit_to_room_and_direction_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'The Tower',
                 'description': 'A room at the top of the tallest tower',
                 'exits': [
                     {}
                 ]}
            ]
        }, 'Missing to room and direction from exit from room "The Tower"')

    def test_exit_to_room_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'in', 'opposite': 'out'}
            ],
            'rooms': [
                {'name': 'A Coffin',
                 'description': 'An ancient, dusty sarcophagus',
                 'exits': [
                     {'to': False, 'direction': 'out'}
                 ]}
            ]
        }, 'Exit to room must be a string')

    def test_exit_direction_not_string_raises(self):
        self.assert_run_game_raises({
            'directions': [
            ],
            'rooms': [
                {'name': 'Dining Room',
                 'description': 'The main eatery',
                 'exits': [
                     {'to': 'Hallway', 'direction': 8}
                 ]}
            ]
        }, 'Exit direction must be a string')

    def test_exit_one_way_exit_not_boolean_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'up', 'opposite': 'down'}
            ],
            'rooms': [
                {'name': 'Stairwell',
                 'description': 'Up and down steps',
                 'exits': [
                     {'to': 'Landing', 'direction': 'up', 'one_way': 'Yes'}
                 ]}
            ]
        }, 'Exit one_way must be a boolean')

    def test_undefined_room_in_exit_raises(self):
        self.assert_run_game_raises({
            'directions': [
                {'name': 'north', 'opposite': 'south'}
            ],
            'rooms': [
                {'name': 'A Room',
                 'description': 'An empty room',
                 'exits': [
                     {'to': 'B Room', 'direction': 'north'}
                 ]}
            ]
        }, 'Unknown exit room "B Room" from "A Room"')

    def test_undefined_direction_in_exit_raises(self):
        self.assert_run_game_raises({
            'directions': [],
            'rooms': [
                {'name': 'A Room',
                 'description': 'An empty room',
                 'exits': [
                     {'to': 'B Room', 'direction': 'up'}
                 ]},
                {'name': 'B Room',
                 'description': 'Another empty room'}
            ]
        }, 'Unknown exit direction "up" from room "A Room"')

    def assert_run_game_raises(self, game_data, expected_message):
        try:
            vengeance.run_game(game_data)
            self.fail()
        except game.GameFormatException as e:
            self.assertEqual(expected_message, e.message)

    def test_one_way_exit(self):
        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': 'Room B', 'direction': 'down', 'one_way': True}
                 ]},
                {'name': 'Room B',
                 'description': 'B'}
            ]
        })

        room_a = game.find_location('Room A')
        self.assertEqual(1, len(room_a.exits))
        room_b = game.find_location('Room B')
        self.assertEqual(0, len(room_b.exits))

    def test_two_way_exit(self):
        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': 'Room B', 'direction': 'down'}
                 ]},
                {'name': 'Room B',
                 'description': 'B'}
            ]
        })

        room_a = game.find_location('Room A')
        self.assertEqual(1, len(room_a.exits))
        room_b = game.find_location('Room B')
        self.assertEqual(1, len(room_b.exits))

    def test_exit_location(self):
        to_location_name = 'Room B'

        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': 'down'},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': to_location_name, 'direction': 'down'}
                 ]},
                {'name': to_location_name,
                 'description': 'B'}
            ]
        })

        exit = game.find_location('Room A').exits[0]
        self.assertEqual(to_location_name, exit.to_location.name)

    def test_exit_direction(self):
        exit_direction = 'down'

        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': exit_direction},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': 'Room B', 'direction': exit_direction}
                 ]},
                {'name': 'Room B',
                 'description': 'B'}
            ]
        })

        exit = game.find_location('Room A').exits[0]
        self.assertEqual(exit_direction, exit.direction.name)

    def test_directions_have_initials_as_synonyms(self):
        exit_direction = 'down'

        game = vengeance.create_game({
            'directions': [
                {'name': 'up', 'opposite': exit_direction},
            ],
            'rooms': [
                {'name': 'Room A',
                 'description': 'A',
                 'exits': [
                     {'to': 'Room B', 'direction': exit_direction}
                 ]},
                {'name': 'Room B',
                 'description': 'B'}
            ]
        })

        game.process_input(exit_direction[0])

        self.assertEqual('Room B', game.character.current_location.name)


if __name__ == '__main__':
    unittest.main()
