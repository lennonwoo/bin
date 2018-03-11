#!/usr/bin/env python
import os


def scripts_list():
    pwd = os.getcwd()
    scripts_dir = os.path.join(pwd, 'scripts')

    for file in os.listdir(scripts_dir):
        if not file.startswith('__'):
            yield os.path.join(scripts_dir, file), file


def install():
    home_dir = os.path.expanduser('~')
    bin_dir = os.path.join(home_dir, 'bin')
    if not os.path.exists(bin_dir):
        os.mkdir(bin_dir)

    for src_path, script in scripts_list():
        # remove the .py for symlink_path
        symlink_path = os.path.join(bin_dir, script[:-3] if script.endswith("py") else script)

        try:
            os.symlink(src_path, symlink_path)
        except FileExistsError as e:
            print("Pass cause just link", e)


if __name__ == '__main__':
    install()
