#!/usr/bin/env python
import os
import re
import pyperclip

__version__ = 0.1
__author__ = 'lennon'

home_dir = os.path.expanduser('~')


def parse_git_url(url):
    # get the info we want from the url as follow
    # https://gitxxx.com/author_name/repo_name/?misc
    pat = re.compile(r"""
    \s*                           # Skip leading whitespace
    (?P<clone_url>                # The url for git clone
        https?://                 # HTTP or HTTPS
        (?P<website>git[^/]+)     # the website
        [.]com/                   # .com/
        (?P<author_name>[^/]+)    # The author's name
        /                         # / split
        (?P<repo_name>[^/]+)      # The repo's name
    )
    #/?.*$                        # Traling character
    """, re.VERBOSE)
    m = re.search(pat, url)
    clone_url = m.group('clone_url')
    author_name = m.group('author_name')
    repo_name = m.group('repo_name')
    return clone_url, author_name, repo_name


def git_clone(url):
    git_dir = os.path.join(home_dir, 'Git')
    clone_url, author_name, repo_name = parse_git_url(url)
    clone_dir = os.path.join(git_dir, author_name, repo_name)

    cmd = 'git clone %s %s' % (clone_url, clone_dir)
    os.system(cmd)


def jump_dir(path):
    os.chdir(path)
    os.system("/bin/zsh")


def video_dl(url):
    video_dir = os.path.join(home_dir, 'Video/')
    output = '-o %s/' % video_dir

    if re.search(r'youtube', url):
        proxy = '--proxy socks5://127.0.0.1:1080/'
        sub = '--write-auto-sub'
    else:
        proxy = ''
        sub = ''

    cmd = 'youtube-dl %s %s %s %s' % (output, proxy, sub, url)
    os.system(cmd)


def main():
    url = pyperclip.paste()

    if re.search(r'git', url):
        git_clone(url)
    elif os.path.exists(url):
        jump_dir(url)
    else:
        video_dl(url)


if __name__ == '__main__':
    main()
