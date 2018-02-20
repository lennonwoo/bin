#!/usr/bin/env python
import os
import re
import pyperclip

__version__ = 0.12
__author__ = 'lennon'


class Handler():
    def __init__(self, url):
        self.home_dir = os.path.expanduser('~')
        self.url = url

    def handle(self):
        if self.condition():
            self.handle_basic()
            self.handle_extra()
            exit(0)

    def condition(self):
        pass

    def handle_basic(self):
        pass

    def handle_extra(self):
        pass


class GitHandler(Handler):
    def parse_git_url(self):
        # get the info we want from the url as follow
        # https://misc/gitxxx.com/author_name/repo_name/?misc
        pat = re.compile(r"""
        \s*                          # Skip leading whitespace
        (?P<clone_url>               # The url for git clone
            https?://                # HTTP or HTTPS
            .*                       # support sites like gist
            (?P<website>git[^/]+)    # the website
            [.]com/                  # .com/
            (?P<author_name>[^/]+)   # The author's name
            /                        # / split
            (?P<repo_name>[^/]+)     # The repo's name
        )
        #/?.*$                       # Traling character
        """, re.VERBOSE)
        m = re.search(pat, self.url)
        clone_url = m.group('clone_url')
        author_name = m.group('author_name')
        repo_name = m.group('repo_name')
        return clone_url, author_name, repo_name

    def condition(self):
        return re.search(r'git', self.url)

    def handle_basic(self):
        git_dir = os.path.join(self.home_dir, 'Git')
        clone_url, author_name, repo_name = self.parse_git_url()
        self.clone_dir = os.path.join(git_dir, author_name, repo_name)

        cmd = 'git clone %s %s' % (clone_url, self.clone_dir)
        os.system(cmd)

    def handle_extra(self):
        os.chdir(self.clone_dir)
        os.system("/bin/zsh")


class DirHandler(Handler):
    def condition(self):
        return os.path.exists(self.url)

    def handle_basic(self):
        os.chdir(self.url)
        os.system("/bin/zsh")


class VideoDownloadHandler(Handler):
    def __init__(self, url):
        super().__init__(url)

    def condition(self):
        pat = re.compile(r"""
        (youtube
        |bilibili
        )
        """)
        return re.search(pat, self.url)

    def handle_basic(self):
        video_dir = os.path.join(self.home_dir, 'Video/')
        output = '-o %s/' % video_dir

        if re.search(r'youtube', self.url):
            proxy = '--proxy socks5://127.0.0.1:1080/'
            sub = '--write-auto-sub'
        else:
            proxy = ''
            sub = ''

        cmd = 'youtube-dl %s %s %s %s' % (output, proxy, sub, self.url)
        os.system(cmd)


class ArchlinuxHandler(Handler):
    def condition(self):
        return re.search(r'archlinux', self.url)

    def handle_basic(self):
        # like this '' is [-1] we choose [-2]
        # 'https://aur.archlinux.org/packages/ros-kinetic-simulators/'
        pkg = self.url.split('/')[-2]
        pkg_manager = 'yaourt' if re.search(r'aur', self.url) else 'pacman'

        cmd = '%s -S %s' % (pkg_manager, pkg)
        os.system(cmd)


def handle_url(url):
    for handler in Handler.__subclasses__():
        h = handler(url)
        h.handle()


def main():
    url = pyperclip.paste()
    handle_url(url)


if __name__ == '__main__':
    main()
