import pytest
from scripts.handle_clipboard import *


@pytest.mark.parametrize("url, clone_url, author_name, repo_name", [
    ('https://gitxxx.com/author_name/repo_name/?misc',
     'https://gitxxx.com/author_name/repo_name',
     'author_name',
     'repo_name',
     ),
    ('https://github.com/brookhong/Surfingkeys/issues',
     'https://github.com/brookhong/Surfingkeys',
     'brookhong',
     'Surfingkeys',
     ),
    ('https://gitlab.com/ImageMagick/ImageMagick/blob/master/ImageMagick/api/annotate.html',
     'https://gitlab.com/ImageMagick/ImageMagick',
     'ImageMagick',
     'ImageMagick',
     ),
    ('https://gist.github.com/zchee/9c78f91cc5ad771c1f5d',
     'https://gist.github.com/zchee/9c78f91cc5ad771c1f5d',
     'zchee',
     '9c78f91cc5ad771c1f5d'
     ),
])
def test_parse_git_url(url, clone_url, author_name, repo_name):
    assert GitHandler(url).parse_git_url() == (clone_url, author_name, repo_name)


@pytest.mark.parametrize("url, assert_handler", [
    ('https://gitxxx.com/author_name/repo_name/?misc',
     GitHandler,
     ),
    ('/opt/pyenv/completions/',
     DirHandler,
     ),
    ('https://www.youtube.com/watch?v=X1VWFhC6G-0',
     VideoDownloadHandler,
     ),
    ('http://www.bilibili.com/video/av7594007/',
     VideoDownloadHandler,
     ),
    ('https://www.archlinux.org/packages/extra/x86_64/dbus-glib/',
     ArchlinuxHandler,
     ),
    ('https://aur.archlinux.org/packages/ros-kinetic-simulators/',
     ArchlinuxHandler,
     ),
])
def test_condition(url, assert_handler):
    for handler in Handler.__subclasses__():
        if handler(url).condition():
            assert handler == assert_handler
