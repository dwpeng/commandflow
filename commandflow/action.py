from abc import ABC, abstractproperty
from typing import List, Union


class ActionBase(ABC):
    """ 动作 """
    def __init__(
        self,
        short_arg_name: Union[str, None] = None,
        long_arg_name: Union[str, None] = None,
        *,
        value: Union[List[str], str, None] = None,
        positional: bool = False,
        help: Union[str, None] = None,
        stdout: Union[str, None] = None,
        sep: str = ' ',
        command = None
    ):
        """ 
            Paramters:
                short_arg_name: e.g. `-a`、`-b`

                long_arg_name: e.g. `--apple`、 `--blue`

                value:  following arg value. e.g.: `--blue yes`

                positional: some arg does not need a arg name

                help: the description text
        """
        if positional:
            short_arg_name = None
            long_arg_name = None
            stdout = False
            
        if stdout is None and short_arg_name is None and long_arg_name is None:
            raise ValueError('short or long arg name is required!')
        self.short_arg_name = short_arg_name
        self.long_arg_name = long_arg_name
        self.value = value
        self.positional = positional
        self.help = help
        self.stdout = stdout
        self.sep = sep
        self.command = command

    @property
    def long_dash(self):
        if hasattr(self.command, 'long_dash'):
            return self.command.long_dash
        return '--'

    @property
    def short_dash(self):
        if hasattr(self.command, 'short_dash'):
            return self.command.short_dash
        return '-'

    @abstractproperty
    def value_str(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        if self.long_arg_name is not None:
            args_name = '%s%s' % (self.long_dash, self.long_arg_name)
        else:
            args_name = '%s%s' % (self.short_dash, self.short_arg_name)

        if self.positional:
            return self.value_str

        return '%s%s' % (
            args_name,
            ' ' + self.value_str if self.value_str else ''
        )

    def __eq__(self, o) -> bool:
        if not isinstance(o, ActionBase):
            return False
        if self.__class__ != o.__class__:
            return False
        if self.long_arg_name == o.long_arg_name and \
             self.short_arg_name == o.short_arg_name:
            return True
        return False


class BoolAction(ActionBase):

    @property
    def value_str(self) -> str:
        return ''

    def __str__(self) -> str:
        if self.value:
            return super().__str__()
        return ''

class StrAction(ActionBase):

    @property
    def value_str(self) -> str:
        return self.value

class ListAction(ActionBase):

    def __init__(
        self,
        short_arg_name: Union[str, None] = None,
        long_arg_name: Union[str, None] = None,
        *,
        value: Union[List[str], str, None] = None,
        positional: bool = False,
        help: Union[str, None] = None,
        sep: str = ' ',
        command = None
    ):
        super().__init__(
            short_arg_name,
            long_arg_name,
            value=value,
            positional=positional,
            help=help,
            command=command
        )
        assert type(sep) is str, 'sep should be a str type value'
        self.sep = sep

    @property
    def value_str(self) -> str:
        return self.sep.join([
            str(i) for i in self.value
        ])


class STDOUTAction(ActionBase):

    @property
    def value_str(self) -> str:
        return ''

    def __str__(self) -> str:
        return '> %s' % self.stdout
