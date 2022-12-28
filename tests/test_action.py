from commandflow import *
from unittest import TestCase


class TestAction(TestCase):

    def test_str_action(self):
        action1 = StrAction(
            'a',
            'apple',
            value='abc'
        )
        self.assertEqual(
            str(action1),
            '--apple abc'
        )

        action2 = StrAction(
            None,
            'apple',
            value='abc'
        )
        self.assertEqual(
            str(action2),
            '--apple abc'
        )

        action3 = StrAction(
            'a',
            None,
            value='abc'
        )
        self.assertEqual(
            str(action3),
            '-a abc'
        )

    def test_bool_action(self):
        action1 = BoolAction(
            'a',
            'apple',
            value=True
        )

        self.assertEqual(
            str(action1),
            '--apple'
        )
        action2 = BoolAction(
            'a',
            'apple',
            value=False
        )

        self.assertEqual(
            str(action2),
            ''
        )

        action3 = BoolAction(
            'a',
            None,
            value=True
        )

        self.assertEqual(
            str(action3),
            '-a'
        )

    def test_list_action(self):
        action1 = ListAction(
            'a',
            'apple',
            value=[1, 2, 3]
        )

        self.assertEqual(
            str(action1),
            '--apple 1 2 3'
        )

        action2 = ListAction(
            'a',
            'apple',
            value=[1.2, 5, 'abc']
        )

        self.assertEqual(
            str(action2),
            '--apple 1.2 5 abc'
        )

        action3 = ListAction(
            'a',
            'apple',
            value=[1, 2, 3],
            sep='#'
        )

        self.assertEqual(
            str(action3),
            '--apple 1#2#3'
        )

    def test_stdout_action(self):
        action1 = STDOUTAction(
            stdout='ssss'
        )

        self.assertEqual(
            str(action1),
            '> ssss'
        )
