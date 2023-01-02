from commandflow import Command
from unittest import TestCase

class MyTestCommand(Command):
    exe = 'help'

    def input(
        self,
        arg1: str,
    ):
        self.set_action('a', 'apple', value=arg1)

class MyTestCommand1(Command):
    exe = 'help'
    long_dash = '@@'
    short_dash = '@'
    def input(
        self,
        arg1: str
    ):
        self.set_action('a', 'apple', value=arg1)
        self.set_action('b', None, value=arg1)

class TestCommand(TestCase):
    
    def test_exe(self):
        c = MyTestCommand()
        self.assertEqual(c.command, 'help')

    def test_arg(self):
        c = MyTestCommand()
        c.input(10)
        self.assertEqual(
            c.command,
            'help --apple 10'
        )

        c.input('abc')
        self.assertEqual(
            c.command,
            'help --apple abc'
        )

    def test_stdout(self):
        c = MyTestCommand()
        c.stdout('test.out')
        c.input(100)
        self.assertEqual(
            c.command,
            'help --apple 100 > test.out'
        )

        c = MyTestCommand()
        c.stdout('test.out')
        c.input('100')
        c.set_action(None, None, positional=True, value=[1,2,3])
        self.assertEqual(
            c.command,
            'help --apple 100 1 2 3 > test.out'
        )

    def test_change_exe(self):
        c = MyTestCommand()
        c.set_exe('hah')
        self.assertEqual(
            c.command,
            'hah'
        )

    def test_dash(self):
        c = MyTestCommand1()
        c.input(100)
        self.assertEqual(
            c.command,
            'help @@apple 100 @b 100'
        )

    def test_clear(self):
        c = MyTestCommand()
        c.input(100)
        c.clear()
        self.assertEqual('help', c.command)

    def test_record(self):
        c = MyTestCommand()
        for i in range(10):
            c.input(i)
            c.record()
        self.assertSequenceEqual(
            c.records,
            ['help --apple %d' % i for i in range(10)]
        )
