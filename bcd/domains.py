from .base import Base


class Domain(Base):
    __slots__ = ('address', 'data', 'expiration', 'level', 'name', 'network', 'timestamp')

    def __init__(self, address, data, expiration, level, name, network, timestamp):
        self.address = address
        self.data = data
        self.expiration = expiration
        self.level = level
        self.name = name
        self.network = network
        self.timestamp = timestamp

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<%s %s address=%r, expiration=%r, level=%r, name=%r, network=%r, timestamp=%r>' % (self.__class__.__name__, id(self), self.address, self.expiration, self.level, self.name, self.network, self.timestamp)

    @classmethod
    def from_api(cls, data):
        address = data['address']
        data = data['data']
        expiration = data['expiration']
        level = data['level']
        name = data['name']
        network = data['network']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(address, data, expiration, level, name, network, timestamp)

    @classmethod
    def get(cls, network, **kwargs):
        path = 'v1/domains/%s' % network
        optional_params = ('offset', 'size')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data['domains']]

    @classmethod
    def resolve(cls, network, **kwargs):
        path = 'v1/domains/%s/resolve' % network
        optional_params = ('name', 'address')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch accounts by network and address(es)')
    parser.add_argument('--network', type=str, default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Network to use')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--name', type=str, help='Name of domain to resolve')
    group.add_argument('--address', type=str, help='Address of domain to resolve')

    args = parser.parse_args()

    kwargs = dict()
    if args.name or args.address:
        if args.name:
            kwargs['name'] = args.name
        else:
            kwargs['address'] = args.address
        domain = Domain.resolve(args.network, **kwargs)
        print('%r' % domain)
    else:
        domains = Domain.get(args.network)
        print(domains)
        for domain in domains:
            print(domain)
