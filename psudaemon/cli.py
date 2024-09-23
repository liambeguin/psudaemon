import argparse
from psudaemon.client import PSUDaemonClient

try:
    from rich import print
except ImportError:
    pass


def parse_cmdline():
    def add_common(parser):
        parser.add_argument('--psu', default=None)
        parser.add_argument('-c', '--channel', default=None)

    parser = argparse.ArgumentParser(description='psudaemon Command line interface.')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', default='5000')
    parser.add_argument('--format', default='auto')
    add_common(parser)

    subpar = parser.add_subparsers(help='Possible actions', dest='action')
    parser.set_defaults(action='get')

    p = subpar.add_parser('get', help='read channel state')
    add_common(p)

    p = subpar.add_parser('set', help='write channel state')
    add_common(p)
    p.add_argument('--state', type=int, default=None)
    p.add_argument('--name', default=None)
    p.add_argument('--current-limit', metavar='A', type=float, default=None)
    p.add_argument('--voltage-limit', metavar='V', type=float, default=None)

    options = parser.parse_args()
    return options


def main():
    options = parse_cmdline()
    client = PSUDaemonClient(options.host, options.port, format=options.format)

    if options.action == 'get':
        client.get(
            psu=options.psu,
            channel=options.channel,
        )
    elif options.action == 'set':
        client.set(
            psu=options.psu,
            channel=options.channel,
            state=options.state,
            name=options.name,
            current_limit=options.current_limit,
            voltage_limit=options.voltage_limit,
        )
    else:
        raise RuntimeError('Invalid action')

    print(client)


if __name__ == '__main__':
    main()
