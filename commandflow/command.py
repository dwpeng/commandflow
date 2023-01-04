from abc import ABC
from functools import partial
from typing import List, Union

from .action import ActionBase, BoolAction, ListAction, STDOUTAction, StrAction


class CommandBase(ABC):
    """ 命令 """
    long_dash = '--'
    short_dash = '-'
    exe = None

    def __init__(self):
        self.exe = self.exe
        self.keyword_args: List[ActionBase] = []
        self.postional_arg: List[ActionBase] = []
        self.stdout_arg: Union[ActionBase, None] = None
        self._records: List[str] = []

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
        stdout: Union[str, None] = None,
    ):
        command = self
        if stdout is not None:
            if type(stdout) is not str:
                raise TypeError('stdout should be a output name')
            self.stdout_arg = STDOUTAction(stdout=stdout, command=command)
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

        # 自动传入当前command
        action = partial(action, command=command)

        action = action(
            short_arg_name=short_arg_name,
            long_arg_name=long_arg_name,
            value=value,
            help=help,
            positional=positional,
        )

        # 检查是否存在重复的参数名
        # 存在的话，更新值
        # 否则，添加该参数
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
        args = '%s %s' % (
            ' '.join([str(i) for i in self.keyword_args]),
            ' '.join([str(i) for i in self.postional_arg]),
        )
        return '%s %s' % (
            args.strip(),
            str(self.stdout_arg) if self.stdout_arg is not None else ''
        )

    @property
    def command(self) -> str:
        return ('%s %s' % (
            self.exe,
            self._create_args()
        )).strip()

    def __str__(self) -> str:
        return self.command

    def clear(self):
        self.keyword_args = []
        self.postional_arg = []
        self.stdout_arg = None
        self._records = []

    def record(self):
        self._records.append(self.command)

    @property
    def records(self) -> List[str]:
        if not self._records:
            return [self.command]
        return [i for i in self._records]


class Command(CommandBase):

    def stdout(self, output: Union[str, None]=None):
        """ 自带一个标准输出的参数 """
        if output is not None:
            self.set_action(stdout=output)
