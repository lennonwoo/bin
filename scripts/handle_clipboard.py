#!/usr/bin/env python
import os
import re
from configparser import ConfigParser

import pyperclip

__version__ = 0.13
__author__ = 'lennon'


def get_relative_path(filename):
    dirname = os.path.dirname(__file__)
    return os.path.join(dirname, filename)


def change_cur_dir(dir_path):
    os.chdir(dir_path)
    os.system("/bin/zsh")


class CD:
    """Context manager for changing the current working directory"""
    def __init__(self, new_path):
        self.new_path = os.path.expanduser(new_path)

    def __enter__(self):
        self.saved_path = os.getcwd()
        os.chdir(self.new_path)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.saved_path)


class Handler:
    def __init__(self, url, section_name=None):
        self.home_dir = os.path.expanduser('~')
        self.url = url

        if section_name is not None:
            config = ConfigParser()
            config.read(get_relative_path('config.ini'))
            section = config[section_name]

            self.location = section.get("location", None)
            self.parse_config(section)

    def handle(self):
        if self.condition():
            self.handle_basic()
            self.handle_extra()
            exit(0)

    def condition(self):
        raise NotImplemented

    def handle_basic(self):
        raise NotImplemented

    def handle_extra(self):
        pass

    def parse_config(self, config):
        pass


class GitHandler(Handler):
    def __init__(self, url):
        super(GitHandler, self).__init__(url, 'Git')

    def condition(self):
        return re.search(r'git', self.url)

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

    def handle_basic(self):
        git_dir = os.path.join(self.home_dir, self.location)
        clone_url, author_name, repo_name = self.parse_git_url()
        self.clone_dir = os.path.join(git_dir, author_name, repo_name)

        cmd = 'git clone %s %s' % (clone_url, self.clone_dir)
        os.system(cmd)

    def handle_extra(self):
        if self.cmd_extra:
            with CD(self.clone_dir):
                os.system(self.cmd_extra)
        else:
            change_cur_dir(self.clone_dir)

    def parse_config(self, section):
        self.cmd_extra = section.get('cmd_extra', None)


class DirHandler(Handler):
    def condition(self):
        return os.path.exists(self.url)

    def handle_basic(self):
        change_cur_dir(self.url)


class StreamHandler(Handler):
    def __init__(self, url):
        super(StreamHandler, self).__init__(url, 'Stream')

    def condition(self):
        pat = re.compile(r"""
        (youtube
        |bilibili
        )
        """, re.VERBOSE)
        return pat.search(self.url)

    def handle_basic(self):
        if re.search(r'youtube', self.url):
            proxy = '--proxy socks5://127.0.0.1:1080/'
        else:
            proxy = ''

        if self.extract_music:
            extra = '--extract-audio --audio-format mp3'
        else:
            extra = '--write-auto-sub'

        cmd = 'youtube-dl %s %s %s' % (proxy, extra, self.url)

        video_dir = os.path.join(self.home_dir, self.location)
        with CD(video_dir):
            os.system(cmd)

    def parse_config(self, section):
        self.extract_music = section.get('extract_music', None)


class ArchlinuxHandler(Handler):
    def condition(self):
        return re.search(r'archlinux', self.url)

    def parse_arch_url(self):
        for s in reversed(self.url.split('/')):
            if s != '':
                return s

    def handle_basic(self):
        pkg = self.parse_arch_url()
        pkg_manager = 'yaourt' if re.search(r'aur', self.url) else 'pacman'

        cmd = 'sudo %s -S %s' % (pkg_manager, pkg)
        print('The command is:\t', cmd)
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
