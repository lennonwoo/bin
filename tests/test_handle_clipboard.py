import pytest
from scripts.handle_clipboard import *

@pytest.mark.parametrize("url, clone_url, author_name, repo_name", [
    ('https://gitxxx.com/author_name/repo_name/?misc',
     'https://gitxxx.com/author_name/repo_name',
     'author_name',
     'repo_name'),
    ('https://github.com/brookhong/Surfingkeys/issues',
     'https://github.com/brookhong/Surfingkeys',
     'brookhong',
     'Surfingkeys'),
    ('https://gitlab.com/ImageMagick/ImageMagick/blob/master/ImageMagick/api/annotate.html',
     'https://gitlab.com/ImageMagick/ImageMagick',
     'ImageMagick',
     'ImageMagick')
])
def test_parse_git_url(url, clone_url, author_name, repo_name):
    assert parse_git_url(url) == (clone_url, author_name, repo_name)
