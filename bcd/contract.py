from .base import Base


class Contract(Base):
    __slots__ = ('address', 'alias', 'annotations', 'delegate', 'delegate_alias', 'entrypoints', 'fail_strings', 'found_by', 'hardcoded', 'hash', 'id', 'language', 'last_action', 'level', 'manager', 'migrations_count', 'network', 'project_id', 'same_count', 'similar_count', 'slug', 'subscription', 'tags', 'timestamp', 'total_subscribed', 'tx_count')

    def __init__(self, address, alias, annotations, delegate, delegate_alias, entrypoints, fail_strings, found_by, hardcoded, hash, id, language, last_action, level, manager, migrations_count, network, project_id, same_count, similar_count, slug, subscription, tags, timestamp, total_subscribed, tx_count):
        self.address = address
        self.alias = alias
        self.annotations = annotations
        self.delegate = delegate
        self.delegate_alias = delegate_alias
        self.entrypoints = entrypoints
        self.fail_strings = fail_strings
        self.found_by = found_by
        self.hardcoded = hardcoded
        self.hash = hash
        self.id = id
        self.language = language
        self.last_action = last_action
        self.level = level
        self.manager = manager
        self.migrations_count = migrations_count
        self.network = network
        self.project_id = project_id
        self.same_count = same_count
        self.similar_count = similar_count
        self.slug = slug
        self.subscription = subscription
        self.tags = tags
        self.timestamp = timestamp
        self.total_subscribed = total_subscribed
        self.tx_count = tx_count

    @classmethod
    def from_api(cls, data):
        address = data['address']
        alias = data['alias']
        annotations = data['annotations']
        delegate = data['delegate']
        delegate_alias = data['delegate_alias']
        entrypoints = data['entrypoints']
        fail_strings = data['fail_strings']
        found_by = data['found_by']
        hardcoded = data['hardcoded']
        hash = data['hash']
        id = data['id']
        language = data['language']
        last_action = data['last_action']
        level = data['level']
        manager = data['manager']
        migrations_count = data['migrations_count']
        network = data['network']
        project_id = data['project_id']
        same_count = data['same_count']
        similar_count = data['similar_count']
        slug = data['slug']
        subscription = [Subscription.from_api(subscription) for item in data['subscription']]
        tags = data['tags']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        total_subscribed = data['total_subscribed']
        tx_count = data['tx_count']
        return cls(address, alias, annotations, delegate, delegate_alias, entrypoints, fail_strings, found_by, hardcoded, hash, id, language, last_action, level, manager, migrations_count, network, project_id, same_count, similar_count, slug, subscription, tags, timestamp, total_subscribed, tx_count)

    @classmethod
    def get(cls, network, address):
        path = 'v1/contract/%s/%s/code' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def by_slug(cls, slug):
        path = 'v1/slug/%r' % slug
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return data

    @classmethod
    def stats(cls, network, period, contracts):
        path = 'v1/stats/%s/contracts' % network
        if isinstance(contracts, (list, tuple, set)):
            contracts = ','.join(contracts)
        params = dict(period=period, contracts=contracts)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return data

    @classmethod
    def get_code(cls, network, address):
        path = 'v1/contract/%s/%s/code' % (network, address)
        response = cls._request(path)
        data = response.content
        return data

    @classmethod
    def from_schema(cls, network, address, data, name, format):
        path = 'v1/contract/%s/%s/entrypoints/data' % (network, address)
        params = dict(data=data, name=name, format=format)
        response = cls_request(path, body=params, method='POST')
        cls.check_errors(data)
        return response.json()

    @classmethod
    def same(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/same' % (network, address)
        optional_params = ('offset', 'size', 'manager')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data['contracts']]

    @classmethod
    def similar(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/similar' % (network, address)
        optional_params = ('offset', 'size')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data['contracts']]

    @classmethod
    def random(cls, network):
        path = 'v1/pick_random' % network
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def diff(cls, left, right):
        path = 'v1/diff'
        body = dict(left=left, right=right)
        response = cls._request(path, json=body, method='POST')
        data = response.json()
        cls.check_errors(data)
        return data


class Entrypoint(Base):
    __slots__ = ('default_model', 'name', 'schema', 'typedef')

    def __init__(self, default_model, name, schema, typedef):
        self.default_model = default_model
        self.name = name
        self.schema = schema
        self.typedef = typedef

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    @classmethod
    def from_api(cls, data):
        default_model = data.get('default_model')
        name = data['name']
        schema = data['schema']
        typedef = data['typedef']
        return cls(default_model, name, schema, typedef)

    @classmethod
    def get(cls, network, address):
        path = 'v1/contract/%s/%s/entrypoints' % (network, address)
        response = cls._request(path)
        data = response.json()
        return [cls.from_api(item) for item in data]

    @classmethod
    def execute_entrypoint(cls, network, address, data, name, **kwargs):
        path = 'v1/contract/%s/%s/entrypoints/trace' % (network, address)
        optional_params = ('amount', 'gas_limit', 'sender', 'source')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        required_params = dict(data=data, name=name)
        params.update(required_params)
        response = cls._request(path, body=params, method='POST')
        data = response.json()
        cls.check_errors(data)
        return data


class EntrypointSchema(Base):
    __slots__ = ('default_model', 'name', 'schema', 'typedef')

    def __init__(self, default_model, name, schema, typedef):
        self.default_model = default_model
        self.name = name
        self.schema = schema
        self.typedef = typedef

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<%s %s name=%r>' % (self.__class__.__name__, id(self), self.name)

    @classmethod
    def from_api(cls, data):
        default_model = data.get('default_model')
        name = data['name']
        schema = data['schema']
        typedef = data['typedef']
        return cls(default_model, name, schema, typedef)

    @classmethod
    def get(cls, network, address, entrypoint, **kwargs):
        path = 'v1/contract/%s/%s/entrypoints/schema' % (network, address)
        optional_params = ('fill_type', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        params['entrypoint'] = entrypoint
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)


class MemPool(Base):
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
        raw_mempool = data['rawMempool']
        source = data['source']
        source_alias = data['source_alias']
        status = data['status']
        storage_diff = data['storage_diff']
        storage_limit = data['storage_limit']
        storage_size = data['storage_size']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(allocated_destination_contract, allocated_destination_contract_burned, amount, balance, burned, consumed_gas, content_index, counter, delegate, destination, destination_alias, entrypoint, errors, fee, gas_limit, hash, id, internal, kind, level, manager_pubkey, mempool, network, paid_storage_size_diff, parameters, protocol, public_key, raw_mempool, source, source_alias, status, storage_diff, storage_limit, storage_size, timestamp)

    @classmethod
    def get(cls, network, address):
        path = 'v1/contract/%s/%s/mempool' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]


class Migration(Base):
    __slots__ = ('hash', 'kind', 'level', 'prev_protocol', 'protocol', 'timestamp')

    def __init__(self, hash, kind, level, prev_protocol, protocol, timestamp):
        self.hash = hash
        self.kind = kind
        self.level = level
        self.prev_protocol = prev_protocol
        self.protocol = protocol
        self.timestamp = timestamp

    @classmethod
    def from_api(cls, data):
        hash = data['hash']
        kind = data['kind']
        level = data['level']
        prev_protocol = data['prev_protocol']
        protocol = data['protocol']
        timestamp = data['timestamp']
        if timestamp:
            timestamp = cls.to_datetime(timestamp)
        return cls(hash, kind, level, prev_protocol, protocol, timestamp)

    @classmethod
    def get(cls, network, address):
        path = 'v1/contract/%s/%s/migrations' % (network, address)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]


class ContractStorage(Base):
    __slots__ = ('children', 'diff_type', 'from_obj', 'name', 'prim', 'type', 'value')

    def __init__(self, children, diff_type, from_obj, name, prim, type, value):
        self.children = children
        self.diff_type = diff_type
        self.from_obj = from_obj
        self.name = name
        self.prim = prim
        self.type = type
        self.value = value

    def __str__(self):
        return self.name

    @classmethod
    def from_api(cls, data):
        children = data['children']
        diff_type = data['diff_type']
        from_obj = data['from']
        name = data['name']
        prim = data['prim']
        type = data['type']
        value = data['value']
        return cls(children, diff_type, from_obj, name, prim, type, value)

    @classmethod
    def get(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/storage' % (network, address)
        optional_params = ('level', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return [cls.from_api(item) for item in data]

    @classmethod
    def get_raw(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/storage/raw' % (network, address)
        optional_params = ('level', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.content
        return data

    @classmethod
    def get_rich(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/storage/rich' % (network, address)
        optional_params = ('level', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.content
        return data


class ContractStorageSchema(Base):
    __slots__ = ('default_model', 'name', 'schema', 'typedef')

    def __init__(self, default_model, name, schema, typedef):
        self.default_model = default_model
        self.name = name
        self.schema = schema
        self.typedef = typedef

    @classmethod
    def from_api(cls, data):
        default_model = data['default_model']
        name = data['name']
        schema = data['schema']
        typedef = data['typedef']
        return cls(default_model, name, schema, typedef)

    @classmethod
    def get(cls, network, address, **kwargs):
        path = 'v1/contract/%s/%s/storage/schema' % (network, address)
        optional_params = ('fill_type', )
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)


class Subscription(Base):
    __slots__ = ('address', 'alias', 'network', 'sentry_dsn', 'sentry_enabled', 'subscribed_at', 'watch_calls', 'watch_deployments', 'watch_errors', 'watch_mempool', 'watch_migrations', 'watch_same', 'watch_similar')

    def __init__(self, address, alias, network, sentry_dsn, sentry_enabled, subscribed_at, watch_calls, watch_deployments, watch_errors, watch_mempool, watch_migrations, watch_same, watch_similar):
        self.address = address
        self.alias = alias
        self.network = network
        self.sentry_dsn = sentry_dsn
        self.sentry_enabled = sentry_enabled
        self.subscribed_at = subscribed_at
        self.watch_calls = watch_calls
        self.watch_deployments = watch_deployments
        self.watch_errors = watch_errors
        self.watch_mempool = watch_mempool
        self.watch_migrations = watch_migrations
        self.watch_same = watch_same
        self.watch_similar = watch_similar

    @classmethod
    def from_api(cls, data):
        address = data['address']
        alias = data['alias']
        network = data['network']
        sentry_dsn = data['sentry_dsn']
        sentry_enabled = data['sentry_enabled']
        subscribed_at = data['subscribed_at']
        watch_calls = data['watch_calls']
        watch_deployments = data['watch_deployments']
        watch_errors = data['watch_errors']
        watch_mempool = data['watch_mempool']
        watch_migrations = data['watch_migrations']
        watch_same = data['watch_same']
        watch_similar = data['watch_similar']
        return cls(address, alias, network, sentry_dsn, sentry_enabled, subscribed_at, watch_calls, watch_deployments, watch_errors, watch_mempool, watch_migrations, watch_same, watch_similar)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Fetch FA tokens by network')
    parser.add_argument('--network', type=str, default='mainnet', choices=('edo2net', 'florencenet', 'granadanet', 'mainnet'), help='Network to use')
    parser.add_argument('--address', type=str, help='Address of a given smart contract')

    args = parser.parse_args()
    entrypoints = Entrypoint.get(args.network, args.address)

    for entrypoint in entrypoints:
        print('%r' % entrypoint)
