from .base import Base


class Token(Base):
    __slots__ = ('address', 'alias', 'balance', 'delegate', 'delegate_alias', 'last_action', 'level', 'manager', 'methods', 'network', 'timestamp', 'tx_count', 'type')

    def __init__(self, address, alias, balance, delegate, delegate_alias, last_action, level, manager, methods, network, timestamp, tx_count, type):
        self.address = address
        self.alias = alias
        self.balance = balance
        self.delegate = delegate
        self.delegate_alias = delegate_alias
        self.last_action = last_action
        self.level = level
        self.manager = manager
        self.methods = methods
        self.network = network
        self.timestamp = timestamp
        self.tx_count = tx_count
        self.type = type

    def __str__(self):
        return self.address

    def __repr__(self):
        return '<%s %s address=%r, alias=%r, balance=%r, level=%r, network=%r, timestamp=%r, tx_count=%r, type=%r>' % (self.__class__.__name__, id(self), self.address, self.alias, self.balance, self.level, self.network, self.timestamp, self.tx_count, self.type)

    def metadata(self, **kwargs):
        kwargs.setdefault('contract', self.address)
        kwargs.setdefault('token_id', self.token_id)
        return TokenMetadata.get(self.network, **kwargs)

    def volume_series(self, **kwargs):
        return self.get_volume_series(self.network, self.address, **kwargs)

    @classmethod
    def from_api(cls, data):
        address = data['address']
        alias = data.get('alias')
        balance = data['balance']
        delegate = data.get('delegate')
        delegate_alias = data.get('delegate_alias')
        last_action = data['last_action']
        level = data['level']
        manager = data.get('manager')
        methods = data.get('methods')
        network = data['network']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        tx_count = data['tx_count']
        type = data['type']
        return cls(address, alias, balance, delegate, delegate_alias, last_action, level, manager, methods, network, timestamp, tx_count, type)

    @classmethod
    def get(cls, network, **kwargs):
        faversion = kwargs.get('faversion')
        if faversion:
            path = 'v1/tokens/%s/version/%s' % (network, faversion)
        else:
            path = 'v1/tokens/%s' % network

        optional_params = ('offset', 'sizVersion of FA tokene')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data['tokens']]

    @classmethod
    def get_volume_series(cls, network, contract, token_id, period):
        path = 'v1/tokens/%s/series' % network
        params = dict(contract=contract, token_id=token_id, period=period)
        response = cls._request(path, params=params)
        print(response.url)
        data = response.json()
        cls.check_errors(data)
        return data

    @classmethod
    def get_transfers(cls, network, address):
        path = 'v1/tokens/%s/transfers/%s' % (network, address)
        optional_params = ('last_id', 'size', 'sort', 'start', 'end', 'contracts', 'token_id')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return data

    @classmethod
    def by_contract(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/tokens' %(network, address)
        optional_params = ('offset', 'size', 'max_level', 'min_level', 'token_id')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]

    @classmethod
    def contract_count(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/tokens/count' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return data['count']

    @classmethod
    def get_token_holders(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/tokens/holders' %(network, address)
        token_id = kwargs.get('token_id', 0)
        params = dict(token_id=token_id)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return data


class TokenMetadata(Base):
    __slots__ = ('artifact_uri', 'contract', 'creators', 'decimals', 'description', 'display_uri', 'external_uri', 'formats', 'is_boolean_amount', 'is_transferable', 'level', 'name', 'network', 'should_prefer_symbol', 'supply', 'symbol', 'tags', 'thumbnail_uri', 'timestamp', 'token_id', 'token_info', 'transfered', 'volume_24_hours', 'number')

    def __init__(self, artifact_uri, contract, creators, decimals, description, display_uri, external_uri, formats, is_boolean_amount, is_transferable, level, name, network, should_prefer_symbol, supply, symbol, tags, thumbnail_uri, timestamp, token_id, token_info, transfered, volume_24_hours):
        self.artifact_uri = artifact_uri
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
        self.supply = supply
        self.symbol = symbol
        self.tags = tags
        self.thumbnail_uri = thumbnail_uri
        self.timestamp = timestamp
        self.token_id = token_id
        self.token_info = token_info
        self.transfered = transfered
        self.volume_24_hours = volume_24_hours

    def __repr__(self):
        return '<%s %s name=%r, symbol=%r, token_id=%r, supply=%r, is_boolean_amount=%r, contract=%r, level=%r>' % (self.__class__.__name__, id(self), self.name, self.symbol, self.token_id, self.supply, self.is_boolean_amount, self.contract, self.level)

    @classmethod
    def from_api(cls, data):
        artifact_uri = data.get('artifact_uri')
        contract = data['contract']
        creators = data.get('creators')
        decimals = data.get('decimals')
        description = data.get('description')
        display_uri = data.get('display_uri')
        external_uri = data.get('external_uri')
        formats = data.get('formats')
        is_boolean_amount = data.get('is_boolean_amount')
        is_transferable = data.get('is_transferable')
        level = data.get('level')
        name = data.get('name')
        network = data['network']
        should_prefer_symbol = data.get('should_prefer_symbol')
        supply = data['supply']
        symbol = data.get('symbol')
        tags = data.get('tags')
        thumbnail_uri = data.get('thumbnail_uri')
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        token_id = data['token_id']
        token_info = data.get('token_info')
        transfered = data.get('transfered')
        volume_24_hours = data.get('volume_24_hours')
        return cls(artifact_uri, contract, creators, decimals, description, display_uri, external_uri, formats, is_boolean_amount, is_transferable, level, name, network, should_prefer_symbol, supply, symbol, tags, thumbnail_uri, timestamp, token_id, token_info, transfered, volume_24_hours)

    @classmethod
    def get(cls, network, **kwargs):
        path = 'v1/tokens/%s/metadata' % network
        optional_params = ('offset', 'size', 'max_level', 'min_level', 'creator', 'contract', 'token_id')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch FA tokens by network')
    parser.add_argument('--network', type=str, default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Network to use')
    parser.add_argument('--faversion', type=str, choices=('fa1', 'fa12', 'fa2'), help='Version of FA token')
    parser.add_argument('--limit', type=int, required=False, default=100, help='Number of tokens to fetch')

    args = parser.parse_args()
    size = 10
    kwargs = dict(size=size)
    if args.faversion:
        kwargs['faversion'] = args.faversion

    tokens = []
    token_page = True
    current_page = 0
    while token_page and len(tokens) < args.limit:
        kwargs['offset'] = current_page * size
        token_page = Token.get(args.network, **kwargs)
        tokens += token_page
        current_page += 1

    for token in tokens:
        print('%r' % token)
