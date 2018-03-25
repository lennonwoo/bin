# bin
The scripts for everyday use

## how to use

### handle_clipboard

1. Copy a url/path from somewhere
2. Git clone/download video from the url or jump to the path in your shell

### remoteserver & win2linux.ahk

1. Put ahk folder in your windows VM
2. Use Autohotkey to start win2linux.ahk script
3. Start the server in your linux localhost

## Install

First install
[youtube-dl](https://github.com/rg3/youtube-dl)
[i3](https://github.com/i3/i3)
[pipenv](https://github.com/pypa/pipenv)

Then
```
pipenv install
```

Finally run to symlink the src to your ~bin/ directory
```
python tools/install.py
```

## Credit
[Socket.ahk](https://github.com/G33kDude/Socket.ahk)
