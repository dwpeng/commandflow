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
        stdout: Union[str, None] = None
    ):
        """ 
            Paramters:
                short_arg_name: e.g. `-a`、`-b`

                long_arg_name: e.g. `--apple`、 `--blue`

                value:  following arg value. e.g.: `--blue yes`

                positional: some arg does not need a arg name

                help: the description text
        """
        if stdout is None and short_arg_name is None and long_arg_name is None:
            raise ValueError('short or long arg name is required!')
        self.short_arg_name = short_arg_name
        self.long_arg_name = long_arg_name
        self.value = value
        self.positional = positional
        self.help = help
        self.stdout = stdout

    @abstractproperty
    def value_str(self) -> str:
        raise NotImplementedError

    def __str__(self) -> str:
        if self.long_arg_name is not None:
            args_name = '--%s' % self.long_arg_name
        else:
            args_name = '-%s' % self.short_arg_name

        if self.positional:
            return self.value_str

        return '%s %s' % (
            args_name,
            self.value_str
        )

    def diff(self, value):
        d = self.to_dict()
        action = ActionBase.from_dict(d)
        action.value = value

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
        sep: str = ' '
    ):
        super().__init__(
            short_arg_name,
            long_arg_name,
            value=value,
            positional=positional,
            help=help
        )
        assert type(sep) is str, 'sep should be a str type value'
        self.sep = sep

    @property
    def value_str(self) -> str:
        return self.sep.join(self.value)


class STDOUTAction(ActionBase):

    @property
    def value_str(self) -> str:
        return ''

    def __str__(self) -> str:
        return '> %s' % self.stdout
