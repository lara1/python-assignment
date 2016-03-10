"""
Assignment Part2 - Cache Implementation
"""
class SimpleCacheFactory(object):
    """
    Implementation for Cache Factory.
    """
    def __init__(self):
        self.mem_capacity = 0
        self.disk_capacity = 0
        print "Initializing Cache Factory"

    def create_cache(self, mem_capacity=0, disk_capacity=0):
        """
        Creating cache based on parameters.
        """
        self.mem_capacity = mem_capacity
        self.disk_capacity = disk_capacity

        if self.mem_capacity < 0 or self.disk_capacity < 0:
            raise InitializationError
        else: return SimpleCache(self.mem_capacity, self.disk_capacity)

class SimpleCache(object):
    """
    Implementation for Cache
    """
    def __init__(self, mem_capacity=0, disk_capacity=0):
        self.memory = MemoryCacheProvider(mem_capacity)
        self.disk = DiskCacheProvider(disk_capacity)

    def put(self, key, value):
        """
        Put implementation
        """
        if self.memory.capacity <= len(self.memory.key_list) and self.disk.capacity <= len(self.disk.key_list):
            old_key = self.disk.get_oldest_key()
            self.disk.remove_cache(old_key)
            old_key = self.memory.get_oldest_key()
            old_value = self.memory.cache[old_key]
            self.memory.remove_cache(old_key)
            self.disk.add_cache_record(old_key, old_value)
            self.memory.add_cache_record(key, value)
        elif self.memory.capacity <= len(self.memory.key_list) and self.disk.capacity > len(self.disk.key_list):
            old_key = self.memory.get_oldest_key()
            old_value = self.memory.cache[old_key]
            self.memory.remove_cache(old_key)
            self.disk.add_cache_record(old_key, old_value)
            self.memory.add_cache_record(key, value)
        else:
            self.memory.add_cache_record(key, value)

    def get(self, key):
        """
        Get Implementation
        """
        print "Getting value from cache ", key
        return key

class MemoryCacheProvider(object):
    """
    In memory cache provider
    """
    def __init__(self, capacity):
        self.capacity = capacity
        self.key_list = []
        self.cache = {}

    def get_max_cache_units(self):
        """
        Return maximum capcity allowed in cache
        """
        return self.capacity

    def current_cache_size(self):
        """
        Return current size of objects stored in cache
        """
        return len(self.key_list)

    def add_cache_record(self, key, obj):
        """
        Adding cache record in to the memory
        """
        self.key_list.append(key)
        self.cache[key] = obj

    def get_cache_value(self, key):
        """
        Get stored cache value from memory
        """
        return self.cache[key]

    def remove_cache(self, key):
        """
        Removing a cache record
        """
        self.key_list.remove(key)
        del self.cache[key]

    def clean_cache(self):
        """
        Clean entire cache
        """
        self.cache.clear()
        del self.key_list[:]

    def get_oldest_key(self):
        """
        Getting oldest key in the cache
        """
        return self.key_list[0]

    def contains_key(self, key):
        """
        Check whether given key contains in cache
        """
        return key in self.key_list

class DiskCacheProvider(object):
    """
    File level cache implementation
    """
    def __init__(self, disk_capacity):
        self.capacity = disk_capacity
        self.key_list = []
        self.cache = {}

    def get_max_cache_units(self):
        """
        Return maximum capcity allowed in cache
        """
        return self.capacity

    def current_cache_size(self):
        """
        Return current size of objects stored in cache
        """
        return len(self.key_list)

    def add_cache_record(self, key, obj):
        """
        Adding cache record in to the memory
        """
        self.key_list.append(key)
        self.cache[key] = obj

    def get_cache_value(self, key):
        """
        Get stored cache value from memory
        """
        return self.cache[key]

    def remove_cache(self, key):
        """
        Removing a cache record
        """
        self.key_list.remove(key)
        del self.cache[key]

    def clean_cache(self):
        """
        Clean entire cache
        """
        self.cache.clear()
        del self.key_list[:]

    def get_oldest_key(self):
        """
        Getting oldest key in the cache
        """
        return self.key_list[0]

    def contains_key(self, key):
        """
        Check whether given key contains in cache
        """
        return key in self.key_list

class InitializationError(RuntimeError):
    """
    Cache intiailization problem.
    """
