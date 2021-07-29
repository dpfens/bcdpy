from .base import Base


class IndexerStatistics(Base):
    __slots__ = ('chain_id', 'hash', 'level', 'network', 'predecessor', 'protocol', 'timestamp')

    def __init__(self, chain_id, hash, level, network, predecessor, protocol, timestamp):
        self.chain_id = chain_id
        self.hash = hash
        self.level = level
        self.network = network
        self.predecessor = predecessor
        self.protocol = protocol
        self.timestamp = timestamp

    def __repr__(self):
        return '<%s %s hash=%r, level=%r, timestamp=%r>' % (self.__class__.__name__, id(self), self.hash, self.level, self.timestamp)

    @classmethod
    def from_api(cls, data):
        chain_id = data['chain_id']
        hash = data['hash']
        level = data['level']
        network = data['network']
        predecessor = data['predecessor']
        protocol = data['protocol']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(chain_id, hash, level, network, predecessor, protocol, timestamp)

    @classmethod
    def get(cls):
        path = 'v1/stats'
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]


class NetworkStatistics(Base):
    __slots__ = ('contract_calls', 'contracts_count', 'fa_count', 'languages', 'operations_count', 'protocols', 'unique_contracts')

    def __init__(self, contract_calls, contracts_count, fa_count, languages, operations_count, protocols, unique_contracts):
        self.contract_calls = contract_calls
        self.contracts_count = contracts_count
        self.fa_count = fa_count
        self.languages = languages
        self.operations_count = operations_count
        self.protocols = protocols
        self.unique_contracts = unique_contracts

    def __repr__(self):
        return '<%s %s contract_calls=%r, contracts_count=%r, fa_count=%r, operations_count=%r, unique_contracts=%r>' % (self.__class__.__name__, id(self), self.contract_calls, self.contracts_count, self.fa_count, self.operations_count, self.unique_contracts)

    @classmethod
    def from_api(cls, data):
        contract_calls = data['contract_calls']
        contracts_count = data['contracts_count']
        fa_count = data['fa_count']
        languages = data['languages']
        operations_count = data['operations_count']
        protocols = data['protocols']
        unique_contracts = data['unique_contracts']
        return cls(contract_calls, contracts_count, fa_count, languages, operations_count, protocols, unique_contracts)

    @classmethod
    def get(cls, network):
        path = 'v1/stats/%s' % network
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def get_series(cls, network, name, period, **kwargs):
        path = 'v1/stats/%s/series' % network
        address = kwargs.get('address')
        params = dict()
        if address:
            params['address'] = ','.join(address)
        response = cls._request(path, params=params)
        data = response.json()
        return data


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch FA tokens by network')
    parser.add_argument('--network', type=str, default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Network to use')

    args = parser.parse_args()

    network_statistics = NetworkStatistics.get(args.network)
    print('%r' % network_statistics)
