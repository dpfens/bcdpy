from .base import Base


class Search(Base):
    __slots__ = ('body', 'group', 'highlights', 'type', 'value')

    def __init__(self, body, group, highlights, type, value):
        self.body = body
        self.group = group
        self.highlights = highlights
        self.type = type
        self.value = value

    def __repr__(self):
        return '<%s %s type=%r, value=%r, group=%r>' % (self.__class__.__name__, id(self), self.type, self.value, self.group)

    @classmethod
    def from_api(cls, data):
        body = data['body']
        group = data.get('group')
        highlights = data.get('highlights')
        type = data['type']
        value = data['value']
        return cls(body, group, highlights, type, value)

    @classmethod
    def query(cls, q, **kwargs):
        path = 'v1/search'
        optional_params = ('f', 'n', 'o', 's', 'e', 'g', 'i', 'l')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        params['q'] = q
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data['items']]


if __name__ == '__main__':
    import argparse
    from datetime import datetime
    parser = argparse.ArgumentParser(description='Search data in contracts, operations, and big map diff')
    parser.add_argument('-q', '--query', type=str, help='Query to use in search')
    parser.add_argument('-f', '--field', type=str, metavar='N', nargs='+', help='Field names among which to search')
    parser.add_argument('-n', '--network', type=str, metavar='N', nargs='+', default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Networks to use in search')
    parser.add_argument('-s', '--since', type=str, required=False, help='Return search result since given timestamp (YYYY-MM-DD)')
    parser.add_argument('-e', '--before', type=str, required=False, help='Return search result before given timestamp (YYYY-MM-DD)')
    parser.add_argument('-g', '--group', type=int, required=False, help='Group by contracts similarity (0=False, any others=True)')
    parser.add_argument('-i', '--index', type=str, metavar='N', nargs='+', choices=('contract', 'operation', 'bigmapdiff'), help='Indices for searching')
    parser.add_argument('-l', '--language', type=str, metavar='N', nargs='+', choices=('smartpy', 'liquidity', 'ligo', 'lorentz', 'michelson'), help='Languages for searching')

    args = parser.parse_args()
    kwargs = dict()
    if args.since:
        kwargs['s'] = datetime.strptime(args.since, '%Y-%m-%d')

    if args.before:
        kwargs['e'] = datetime.strptime(args.before, '%Y-%m-%d')

    if args.network:
        kwargs['n'] = ','.join(args.network)

    if args.field:
        kwargs['f'] = ','.join(args.field)

    if args.group is not None:
        kwargs['g'] = args.group

    if args.index:
        kwargs['i'] = ','.join(args.index)

    if args.language:
        kwargs['l'] = ','.join(args.language)

    search_results = Search.query(args.query, **kwargs)
    for result in search_results:
        print(result)
