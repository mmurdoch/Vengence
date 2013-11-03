import unittest

from vengeance.game import Command
from vengeance.game import Direction
from vengeance.game import Game
from vengeance.game import Location
from vengeance.game import PlayerCharacter


class CommandTest(unittest.TestCase):
    def test_name_set_in_constructor(self):
        arbitrary_name = 'name'
        command = self._create_command(arbitrary_name)

        self.assertEquals(arbitrary_name, command.name)

    def test_func_called_by_run(self):
        context = []
        command = Command('name', _fake_func, context)

        command.run(PlayerCharacter(Location('a')))

        self.assertEquals('called', context[0])

    def _create_command(self, name):
        return Command(name, _fake_func, [])


def _fake_func(character, context):
    context.append('called')


class DirectionTest(unittest.TestCase):
    def test_setting_opposite(self):
        east = Direction('east')
        west = Direction('west')

        east.opposite = west

        self.assertEquals(west.name, east.opposite.name)

    def test_setting_opposite_also_sets_reverse(self):
        east = Direction('east')
        west = Direction('west')

        east.opposite = west

        self.assertEquals(east.name, west.opposite.name)


class GameTest(unittest.TestCase):
    def test_find_location(self):
        name = 'Arbitrary name'
        description = 'Arbitrary description'
        game = Game([Location(name, description)])

        location = game.find_location(name)

        self.assertEqual(description, location.description)

    def test_first_location_is_character_start(self):
        first_location_name = 'one'
        first_location = Location(first_location_name)
        second_location = Location('two')
        game = Game([first_location, second_location])

        starting_location = game.character.current_location

        self.assertEqual(first_location_name, starting_location.name)

    def test_movement(self):
        location_one = Location('L1')
        location_two = Location('L2')
        location_one.add_one_way_exit(Direction('west'), location_two)
        game = Game([location_one, location_two])

        game.process_input('w')

        self.assertEqual('L2', game.character.current_location.name)

    def test_find_game_command_by_name(self):
        game = self._arbitrary_game()
        quit_command_name = 'quit'

        command = game.find_command(quit_command_name)

        self.assertEqual(quit_command_name, command.name)

    def test_find_game_command_by_synonym(self):
        game = self._arbitrary_game()
        quit_command_name = 'quit'

        command = game.find_command(quit_command_name[0])

        self.assertEqual(quit_command_name, command.name)

    def test_missing_command(self):
        game = self._arbitrary_game()

        command = game.find_command('missing')

        self.assertEqual(None, command)

    def test_multiple_found_commands_return_none(self):
        location_one = Location('L1')
        location_two = Location('L2')
        location_one.add_one_way_exit(Direction('quick'), location_two)
        game = Game([location_one, location_two])

        command = game.find_command('q')

        self.assertEqual(None, command)

    def test_no_locations_throws(self):
        try:
            Game([])
            self.fail()
        except ValueError:
            # Success
            pass

    def _arbitrary_game(self):
        return Game([Location('L1', '')])


class LocationTest(unittest.TestCase):
    def test_name(self):
        name = 'a name'
        location = Location(name, 'arbitrary description')

        self.assertEqual(name, location.name)

    def test_description(self):
        description = 'a description'
        location = Location('arbitrary name', description)

        self.assertEqual(description, location.description)

    def test_default_description_is_empty_string(self):
        location = Location('arbitrary name')

        self.assertEqual('', location.description)

if __name__ == '__main__':
    unittest.main()