from .base import Base


class Balance(Base):

    def __init__(self, artifact_uri, balance, contract, creators, decimals, description, display_uri, external_uri, formats, is_boolean_amount, is_transferable, level, name, network, should_prefer_symbol, symbol, tags, thumbnail_uri, timestamp, token_id, token_info, volume_24_hours):
        self.artifact_uri = artifact_uri
        self.balance = balance
        self.contract = contract
        self.creators = creators
        self.decimals = decimals
        self.description = description
        self.display_uri = display_uri
        self.external_uri = external_uri
        self.formats = formats
        self.is_boolean_amount = is_boolean_amount
        self.is_transferable = is_transferable
        self.level = level
        self.name = name
        self.network = network
        self.should_prefer_symbol = should_prefer_symbol
        self.symbol = symbol
        self.tags = tags
        self.thumbnail_uri = thumbnail_uri
        self.timestamp = timestamp
        self.token_id = token_id
        self.token_info = token_info
        self.volume_24_hours = volume_24_hours

    def __repr__(self):
        return '<%s %s name=%r, symbol=%r, balance=%r, is_boolean_amount=%r, contract=%r, token_id=%r, level=%r>' % (self.__class__.__name__, id(self), self.name, self.symbol, self.balance, self.is_boolean_amount, self.contract, self.token_id, self.level)

    @classmethod
    def from_api(cls, data):
        artifact_uri = data.get('artifact_uri')
        balance = data['balance']
        contract = data['contract']
        creators = data.get('creators', [])
        decimals = data.get('decimals')
        description = data.get('description')
        display_uri = data.get('display_uri')
        external_uri = data.get('external_uri')
        formats = data.get('formats', [])
        is_boolean_amount = data.get('is_boolean_amount')
        is_transferable = data.get('is_transferable')
        level = data.get('level')
        name = data.get('name')
        network = data['network']
        should_prefer_symbol = data.get('should_prefer_symbol')
        symbol = data.get('symbol')
        tags = data.get('tags', [])
        thumbnail_uri = data.get('thumbnail_uri')
        timestamp = data.get('timestamp')
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        token_id = data['token_id']
        token_info = data.get('token_info')
        volume_24_hours = data.get('volume_24_hours')
        return cls(artifact_uri, balance, contract, creators, decimals, description, display_uri, external_uri, formats, is_boolean_amount, is_transferable, level, name, network, should_prefer_symbol, symbol, tags, thumbnail_uri, timestamp, token_id, token_info, volume_24_hours)

    @classmethod
    def batch(cls, network, *address):
        path = 'v1/account/%s' % network
        params = dict(address=','.join(address))
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        results = dict()
        for item in data:
            raw_values = data[item]
            instance = [cls.from_api(token_data) for token_data in raw_values]
            results[item] = instance
        return results

    @classmethod
    def by_address(cls, network, address, **kwargs):
        path = 'v1/account/%s/%s/token_balances' % (network, address)

        params = dict()
        optional_params = ('offset', 'size', 'contract', 'sort_by', 'hide_empty')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)

        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        balances = data['balances']
        return [cls.from_api(item) for item in balances]

    @classmethod
    def get(cls, network, *address, **kwargs):
        if not address:
            raise ValueError('Must provide 1 or more addresses')
        if len(address) == 1:
            return cls.by_address(network, *address, **kwargs)
        else:
            return cls.batch(network, *address)

    @classmethod
    def group_by_contract(cls, network, address, **kwargs):
        with_metadata = kwargs.get('with_metadata', False)
        if with_metadata:
            path = 'v1/account/%s/%s/count_with_metadata' % (network, address)
        else:
            path = 'v1/account/%s/%s/count' % (network, address)
        return cls._request(path)


class Account(Base):
    __slots__ = ('address', 'alias', 'balance', 'last_action', 'network', 'tx_count')

    def __init__(self, address, alias, balance, last_action, network, tx_count):
        self.address = address
        self.alias = alias
        self.balance = balance
        self.last_action = last_action
        self.network = network
        self.tx_count = tx_count

    def __str__(self):
        return self.address

    @classmethod
    def from_api(cls, data):
        address = data['address']
        alias = data['alias']
        balance = data['balance']
        last_action = data['last_action']
        network = data['network']
        tx_count = data['tx_count']
        return cls(address, alias, balance, last_action, network, tx_count)

    @classmethod
    def get(cls, network, address):
        path = 'v1/account/%s/%s' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def get_metadata(cls, network, address):
        path = 'v1/account/%s/%s/metadata' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch account balances by network and address(es)')
    parser.add_argument('--network', type=str, default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Network to use')
    parser.add_argument('--addresses', metavar='N', type=str, nargs='+', help='Accounts of addresses to fetch')
    parser.add_argument('--limit', type=int, required=False, default=100, help='Number of balances to fetch for each listed account')

    args = parser.parse_args()
    for address in args.addresses:
        print('Address %r' % address)
        balances = []
        balance_page = True

        while balance_page and len(balances) < args.limit:
            kwargs = dict(offset=len(balances))
            balance_page = Balance.get(args.network, address, **kwargs)
            balances += balance_page

        for balance in balances:
            print('\t%r' % balance)
