from .base import Base


def error(id):
    path = 'v1/operation/%s/error_location' % id
    response = Base._request(path)
    data = response.json()
    return data


class OperationGroup(Base):
    __slots__ = ('allocated_destination_contract', 'allocated_destination_contract_burned', 'amount', 'balance', 'burned', 'consumed_gas', 'content_index', 'counter', 'delegate', 'destination', 'destination_alias', 'entrypoint', 'errors', 'fee', 'gas_limit', 'hash', 'id', 'internal', 'kind', 'level', 'manager_pubkey', 'mempool', 'network', 'paid_storage_size_diff', 'parameters', 'protocol', 'public_key', 'raw_mempool', 'source', 'source_alias', 'status', 'storage_diff', 'storage_limit', 'storage_size', 'timestamp')

    def __init__(self, allocated_destination_contract, allocated_destination_contract_burned, amount, balance, burned, consumed_gas, content_index, counter, delegate, destination, destination_alias, entrypoint, errors, fee, gas_limit, hash, id, internal, kind, level, manager_pubkey, mempool, network, paid_storage_size_diff, parameters, protocol, public_key, raw_mempool, source, source_alias, status, storage_diff, storage_limit, storage_size, timestamp):
        self.allocated_destination_contract = allocated_destination_contract
        self.allocated_destination_contract_burned = allocated_destination_contract_burned
        self.amount = amount
        self.balance = balance
        self.burned = burned
        self.consumed_gas = consumed_gas
        self.content_index = content_index
        self.counter = counter
        self.delegate = delegate
        self.destination = destination
        self.destination_alias = destination_alias
        self.entrypoint = entrypoint
        self.errors = errors
        self.fee = fee
        self.gas_limit = gas_limit
        self.hash = hash
        self.id = id
        self.internal = internal
        self.kind = kind
        self.level = level
        self.manager_pubkey = manager_pubkey
        self.mempool = mempool
        self.network = network
        self.paid_storage_size_diff = paid_storage_size_diff
        self.parameters = parameters
        self.protocol = protocol
        self.public_key = public_key
        self.raw_mempool = raw_mempool
        self.source = source
        self.source_alias = source_alias
        self.status = status
        self.storage_diff = storage_diff
        self.storage_limit = storage_limit
        self.storage_size = storage_size
        self.timestamp = timestamp

    def __str__(self):
        return self.hash

    def __repr__(self):
        return '<%s %s kind=%r, amount=%r, balance=%r, network=%r, level=%r>' % (self.__class__.__name__, id(self), self.kind, self.amount, self.balance, self.network, self.level)

    @classmethod
    def from_api(cls, data):
        allocated_destination_contract = data['allocated_destination_contract']
        allocated_destination_contract_burned = data['allocated_destination_contract_burned']
        amount = data['amount']
        balance = data['balance']
        burned = data['burned']
        consumed_gas = data['consumed_gas']
        content_index = data['content_index']
        counter = data['counter']
        delegate = data['delegate']
        destination = data['destination']
        destination_alias = data['destination_alias']
        entrypoint = data['entrypoint']
        errors = data['errors']
        fee = data['fee']
        gas_limit = data['gas_limit']
        hash = data['hash']
        id = data['id']
        internal = data['internal']
        kind = data['kind']
        level = data['level']
        manager_pubkey = data['manager_pubkey']
        mempool = data['mempool']
        network = data['network']
        paid_storage_size_diff = data['paid_storage_size_diff']
        parameters = data['parameters']
        protocol = data['protocol']
        public_key = data['public_key']
        rawMempool = data.get('rawMempool')
        source = data['source']
        source_alias = data['source_alias']
        status = data['status']
        storage_diff = data['storage_diff']
        storage_limit = data['storage_limit']
        storage_size = data['storage_size']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(allocated_destination_contract, allocated_destination_contract_burned, amount, balance, burned, consumed_gas, content_index, counter, delegate, destination, destination_alias, entrypoint, errors, fee, gas_limit, hash, id, internal, kind, level, manager_pubkey, mempool, network, paid_storage_size_diff, parameters, protocol, public_key, rawMempool, source, source_alias, status, storage_diff, storage_limit, storage_size, timestamp)

    @classmethod
    def get(cls, hash, **kwargs):
        path = 'v1/opg/%s' % hash
        optional_params = ('with_mempool', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]
