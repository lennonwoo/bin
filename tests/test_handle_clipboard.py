import pytest
from scripts.handle_clipboard import cond_func, parse_git_url, git_clone
from scripts.handle_clipboard import jump_dir, video_dl, arch_pkg


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
    assert parse_git_url(url) == (clone_url, author_name, repo_name)


@pytest.mark.parametrize("url, func_assert", [
    ('https://gitxxx.com/author_name/repo_name/?misc',
     git_clone,
     ),
    ('/opt/pyenv/completions/',
     jump_dir,
     ),
    ('https://www.youtube.com/watch?v=X1VWFhC6G-0',
     video_dl,
     ),
    ('http://www.bilibili.com/video/av7594007/',
     video_dl,
     ),
    ('https://www.archlinux.org/packages/extra/x86_64/dbus-glib/',
     arch_pkg,
     ),
    ('https://aur.archlinux.org/packages/ros-kinetic-simulators/',
     arch_pkg,
     ),
])
def test_condition_func(url, func_assert):
    for cond, func in cond_func:
        if cond(url):
            assert func == func_assert
