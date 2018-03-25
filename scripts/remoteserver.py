#!/usr/bin/env python3
import asyncio

import i3


def show_VM():
    i3.scratchpad('show', title='^.*Oracle VM.*$')


async def server(reader, writer):
    command = await reader.read()
    command = command.decode('utf8')
    if command == "win2linux":
        print(command)
        show_VM()
    writer.write_eof()


async def main(addr):
    s = await asyncio.start_server(server, host=addr[0], port=addr[1])
    await s.wait_closed()


if __name__ == '__main__':
    addr = '127.0.0.1', 1090
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(addr))
