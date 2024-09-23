import json
import sys

import requests

try:
    from rich.console import Console, ConsoleOptions, RenderResult
    from rich.json import JSON
    from rich.table import Table
except ImportError:
    pass


class PSUDaemonClient:
    '''PSUDaemon Client interface.'''
    def __init__(self, host, port=5000, format='auto'):
        self.host, self.port = host, port
        self.baseurl = f'http://{self.host}:{self.port}/'

        if format == 'auto':
            self.format = 'table' if sys.stdout.isatty() else 'json'

        self._data = []

    def get(self, psu=None, channel=None):
        path = 'monitoring/channels'
        if psu is not None and channel is not None:
            path = f'units/{psu}/{channel}'

        r = requests.get(self.baseurl + path)
        self._data = r.json()
        return r

    def set(self, psu, channel, state=None, name=None, current_limit=None, voltage_limit=None):
        payload = {}
        path = f'units/{psu}/{channel}'
        headers = {
            'accept': 'application/json',
        }

        if psu is None or channel is None:
            raise RuntimeError('need `psu` and `channel` to be set parameters')

        if state is not None:
            payload['state'] = bool(state)
        if name is not None:
            payload['name'] = name
        if current_limit is not None:
            payload['current_limit'] = current_limit
        if voltage_limit is not None:
            payload['voltage_limit'] = voltage_limit

        r = requests.post(self.baseurl + path, headers=headers, params=payload)
        self._data = r.json()
        return r

    def __getitem__(self, key):
        return self._data[key]

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        def _fmt_one(value):
            return f'{value: >6.3f}' if value is not None else str(value)

        if self.format == 'table':
            table = Table(show_header=True)

            headers = [
                'PSU Name',
                'Channel Name',
                'Index',
                'State',
                'Voltage',
                'Voltage Limit',
                'Current',
                'Current Limit',
            ]

            for h in headers:
                table.add_column(h)

            for row in self._data:
                table.add_row(
                    row['psu.name'],
                    row['name'],
                    str(row['index']),
                    '[green]ON[/green]' if row['state'] else '[red]OFF[/red]',
                    _fmt_one(row['voltage']),
                    _fmt_one(row['voltage_limit']),
                    _fmt_one(row['current']),
                    _fmt_one(row['current_limit']),
                )
            yield table
        else:
            yield JSON(json.dumps(self._data))

    def __str__(self):
        return json.dumps(self._data)
