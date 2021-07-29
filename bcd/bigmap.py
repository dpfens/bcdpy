from .base import Base


class BigMap(Base):
    __slots__ = ('active_keys', 'address', 'contract_alias', 'network', 'ptr', 'total_keys', 'typedef')

    def __init__(self, active_keys, address, contract_alias, network, ptr, total_keys, typedef):
        self.active_keys = active_keys
        self.address = address
        self.contract_alias = contract_alias
        self.network = network
        self.ptr = ptr
        self.total_keys = total_keys
        self.typedef = typedef

    @classmethod
    def from_api(cls, data):
        active_keys = data['active_keys']
        address = data['address']
        contract_alias = data['contract_alias']
        network = data['network']
        ptr = data['ptr']
        total_keys = data['total_keys']
        typedef = data['typedef']
        return cls(active_keys, address, contract_alias, network, ptr, total_keys, typedef)

    @classmethod
    def get(cls, network, ptr):
        path = 'v1/bigmap/%s/%s' % (network, ptr)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def get_diff_count(cls, network, ptr):
        path = 'v1/bigmap/%s/%s' % (network, ptr)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return data['count']

    @classmethod
    def get_actions(cls, network, ptr):
        path = 'v1/bigmap/%s/%r/history' % (network, ptr)
        response = cls._request(path)
        data = response.json()
        cls.check_errors(data)
        return cls.from_api(data)

    @classmethod
    def get_keys_by_ptr(cls, network, ptr, **kwargs):
        path = 'v1/bigmap/%s/%s/keys' % (network, ptr)
        optional_params = ('q', 'offset', 'size', 'max_level', 'min_level')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return data

    @classmethod
    def get_diff(cls, network, ptr, key_hash, **kwargs):
        path = 'v1/bigmap/%s/%s/keys/%s' % (network, ptr, key_hash)
        optional_params = ('offset', 'size')
        params = dict((param, kwargs[param]) for param in optional_params if param in kwargs)
        response = cls._request(path, params=params)
        data = response.json()
        cls.check_errors(data)
        return data
