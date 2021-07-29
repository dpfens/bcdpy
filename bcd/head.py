from .base import Base


class Head(Base):
    __slots__ = ('contract_calls', 'fa_count', 'level', 'network', 'protocol', 'time', 'total', 'unique_contracts')

    def __init__(self, contract_calls, fa_count, level, network, protocol, time, total, unique_contracts):
        self.contract_calls = contract_calls
        self.fa_count = fa_count
        self.level = level
        self.network = network
        self.protocol = protocol
        self.time = time
        self.total = total
        self.unique_contracts = unique_contracts

    def __str__(self):
        return str(self.level)

    def __repr__(self):
        return '<%s %s contract_calls=%r, fa_count=%r, levels=%r, network=%r, time=%r, total=%r, unique_contracts=%r>' % (self.__class__.__name__, id(self), self.contract_calls, self.fa_count, self.level, self.network, self.time, self.total, self.unique_contracts)

    @classmethod
    def from_api(cls, data):
        contract_calls = data['contract_calls']
        fa_count = data['fa_count']
        level = data['level']
        network = data['network']
        protocol = data['protocol']
        time = data['time']
        if time:
            time = cls.to_datetime(time)
        total = data['total']
        unique_contracts = data['unique_contracts']
        return cls(contract_calls, fa_count, level, network, protocol, time, total, unique_contracts)

    @classmethod
    def get(cls):
        path = 'v1/head'
        response = cls._request(path)
        data = response.json()
        return [cls.from_api(item) for item in data]


if __name__ == '__main__':
    heads = Head.get()
    print('%r' % heads)
