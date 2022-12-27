from abc import ABC
from copy import deepcopy
from functools import partial
from typing import List, Union

from .action import ActionBase, BoolAction, ListAction, STDOUTAction, StrAction


class CommandBase(ABC):
    """ 命令 """
    exe = None

    def __init__(self):
        self.exe = self.exe
        self.keyword_args: List[ActionBase] = []
        self.postional_arg: List[ActionBase] = []
        self.stdout_arg: Union[ActionBase, None] = None

    def set_exe(self, exe):
        self.exe = exe

    def set_action(
        self,
        short_arg_name: Union[str, None] = None,
        long_arg_name: Union[str, None] = None,
        value: Union[str, bool, List, None] = None,
        help: Union[str, None] = None,
        positional: bool = False,
        sep: str = ' ',
        stdout: Union[str, None] = None
    ):
        if stdout is not None:
            if type(stdout) is not str:
                raise TypeError('stdout should be a output name')
            self.stdout_arg = STDOUTAction(stdout=stdout)
            return self

        if type(value) is list:
            value = [str(i) for i in value]
            action = ListAction
            action = partial(action, sep=sep)
        elif type(value) is bool:
            action = BoolAction
        elif isinstance(value, (str, int, float)):
            value = str(value)
            action = StrAction
        else:
            raise TypeError('list/str/bool type is required.')

        action = action(
            short_arg_name=short_arg_name,
            long_arg_name=long_arg_name,
            value=value,
            help=help,
            positional=positional,
        )

        check_args = [
            self.keyword_args,
            self.postional_arg,
        ][action.positional]

        for index, exist_action in enumerate(check_args):
            if action == exist_action:
                check_args[index] = action
                return self

        if action.positional:
            self._set_positional_action(action)
        else:
            self._set_keyword_action(action)
        return self

    def _set_keyword_action(self, action: ActionBase):
        self.keyword_args.append(action)
        return self

    def _set_positional_action(self, action: ActionBase):
        self.postional_arg.append(action)
        return self

    def _create_args(self) -> str:
        """ 生成参数 """
        return '%s %s %s' % (
            ' '.join([str(i) for i in self.keyword_args]),
            ' '.join([str(i) for i in self.postional_arg]),
            self.stdout_arg if self.stdout_arg is not None else ''
        )

    @property
    def command(self) -> str:
        return '%s %s' % (
            self.exe,
            self._create_args()
        )

    def __str__(self) -> str:
        return '%s' % (
            self.command
        )

    def clear(self):
        self.keyword_args = []
        self.postional_arg = []
        self.stdout_arg = None


class Command(CommandBase):
    pass

    def stdout(self, output=None):
        if output is not None:
            self.set_action(stdout=output)
