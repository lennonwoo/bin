#!/usr/bin/env python
import os
import re
import pyperclip

__version__ = 0.11
__author__ = 'lennon'

home_dir = os.path.expanduser('~')

cond_func = []


def collect(condition):
    def decorate(func):
        global cond_func
        cond_func += [[condition, func]]

        return func
    return decorate


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


def git_clone_cond(url):
    return re.search(r'git', url)


@collect(git_clone_cond)
def git_clone(url):
    git_dir = os.path.join(home_dir, 'Git')
    clone_url, author_name, repo_name = parse_git_url(url)
    clone_dir = os.path.join(git_dir, author_name, repo_name)

    cmd = 'git clone %s %s' % (clone_url, clone_dir)
    os.system(cmd)


def jump_dir_cond(path):
    return os.path.exists(path)


@collect(jump_dir_cond)
def jump_dir(path):
    os.chdir(path)
    os.system("/bin/zsh")


def video_dl_cond(url):
    pat = re.compile(r"""
    (youtube
    |bilibili
    )
    """)
    return re.search(pat, url)


@collect(video_dl_cond)
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


def arch_pkg_cond(url):
    return re.search(r'archlinux', url)


@collect(arch_pkg_cond)
def arch_pkg(url):
    # like this '' is [-1] we choose [-2]
    # 'https://aur.archlinux.org/packages/ros-kinetic-simulators/'
    pkg = url.split('/')[-2]
    pkg_manager = 'yaourt' if re.search(r'aur', url) else 'pacman'

    cmd = 'sudo %s -S %s' % (pkg_manager, pkg)
    os.system(cmd)


def handle_url(url):
    for cond, func in cond_func:
        if cond(url):
            func(url)
            return


def main():
    url = pyperclip.paste()
    handle_url(url)


if __name__ == '__main__':
    main()