from ..base import Command
from typing import List

r"""https://www.gnu.org/software/wget/manual/wget.html"""


class Wget(Command):
    exe = 'wget'

    def url(self, url: str):
        self.set_action(None, None, value=url, positional=True)

    def urls(self, urls: List[str]):
        for url in urls:
            self.url(url)
            self.record()

    def rename(self, new_name: str):
        self.set_action(
            'O',
            None,
            value=str(new_name)
        )

    def background(self, enable=False):
        self.set_action('b', 'background', value=bool(enable))

    def retrie(self, num: int):
        self.set_action('t', None, value=int(num))

    def continue_download(self, c: bool = False):
        self.set_action('c', 'continue', value=bool(c))

    def quit(self, enable: bool = False):
        self.set_action('q', 'quite', value=bool(enable))

    def download_from_file(self, path: str):
        self.set_action('i', None, value=path)
