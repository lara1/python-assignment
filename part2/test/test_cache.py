"""
Test module for caching
"""
# pylint: disable=no-self-use, unused-argument
import pytest

from part2.cache import *

@pytest.fixture(scope='function')
def factory(request):
    """
    Fixture for cache_factory
    Fixture Scope - function, class, module, session
    """
    cache_factory = SimpleCacheFactory()
    return cache_factory

class TestSimpleCacheFactory(object):
    """
    Test class for Simple Cache Factory
    """
    def correct_initialization(self, factory):
        """
        Testing reverse string.
        """
        cache = factory.create_cache(10, 10)
        assert cache != None

    def incorrect_intialization(self, factory):
        """
        Testing cache capacities with negative numbers
        """
        try:
            factory.create_cache(0, -1)
        except InitializationError:
            assert True
        else:
            assert False

class TestSimpleCache(object):
    """
    Test class for Simple Cache
    """
    def cache_get(self, factory):
        """
        Testing cache get feature
        """
        cache = factory.create_cache(2, 3)
        cache.put("aaa", "AAA")
        cache.put("bbb", "BBB")
        cache.put("ccc", "CCC")

        assert cache.get("aaa") == "AAA"

class TestMemoryCacheProvider(object):
    """
    Test memory cache provider
    """
    @pytest.fixture(scope='function')
    def mem_cache(self, request, size):
        mem_provider = MemoryCacheProvider(size)
        if size == 1:
            mem_provider.add_cache_record("aaa", "AAA")
        return mem_provider

    @pytest.mark.parametrize('size', [5])
    def test_max_cache_units(self, mem_cache, size):
        """
        Testing maximum memory limit allocated
        """
        assert mem_cache.capacity == 5

    @pytest.mark.parametrize('size', [1])
    def test_current_cache_size(self, mem_cache):
        """
        Testing alloacted memroy size for a given time
        """
        assert len(mem_cache.key_list) == 1

    @pytest.mark.parametrize('size', [1])
    def test_add_cache_record(self, mem_cache, size):
        """
        Testing add feature of cache
        """
        assert len(mem_cache.key_list) == 1
        assert len(mem_cache.cache) == 1
        mem_cache.add_cache_record("bbb", "BBB")
        assert len(mem_cache.key_list) == 2
        assert len(mem_cache.cache) == 2

    @pytest.mark.parametrize('size', [1])
    def test_get_cache_value(self, mem_cache, size):
        """
        Testing retrieving cache value stored
        """
        assert mem_cache.get_cache_value("aaa") == "AAA"

        try:
            mem_cache.get_cache_value("bbb")
        except KeyError:
            assert True
        else:
            assert False

    @pytest.mark.parametrize('size', [1]) 
    def test_remove_cache(self, mem_cache, size):
        """
        Testing removing cache key
        """
        mem_cache.remove_cache("aaa")
        assert len(mem_cache.key_list) == 0
        assert len(mem_cache.cache) == 0

    @pytest.mark.parametrize('size', [1])
    def test_clean_cache(self, mem_cache, size):
        """
        Testing cache clean up
        """
        mem_cache.add_cache_record("bbb", "BBB")
        mem_cache.clean_cache()
        assert len(mem_cache.key_list) == 0
        assert len(mem_cache.cache) == 0
    
    @pytest.mark.parametrize('size', [1])
    def test_get_oldest_key(self, mem_cache, size):
        """
        Testing oldest key find situation
        """
        mem_cache.add_cache_record("bbb", "BBB")
        assert mem_cache.get_oldest_key() == "aaa"

    @pytest.mark.parametrize('size', [1])
    def test_get_contains_key(self, mem_cache, size):
        """
        Testing cache contails key
        """
        assert mem_cache.contains_key("aaa") == True


class TestDiskCacheProvider(object):
    """
    Test disk cache provider
    """
    @pytest.fixture(scope='function')
    def disk_cache(self, request, size):
        disk_provider = DiskCacheProvider(size)
        if size == 1:
            disk_provider.add_cache_record("aaa", "AAA")
        return disk_provider

    @pytest.mark.parametrize('size', [5])
    def test_max_cache_units(self, disk_cache, size):
        """
        Testing maximum memory limit allocated
        """
        assert disk_cache.capacity == 5

    @pytest.mark.parametrize('size', [1])
    def test_current_cache_size(self, disk_cache):
        """
        Testing alloacted memroy size for a given time
        """
        assert disk_cache.current_cache_size() == 1
        assert len(disk_cache.key_list) == 1

    @pytest.mark.parametrize('size', [1])
    def test_add_cache_record(self, disk_cache, size):
        """
        Testing add feature of cache
        """
        assert len(disk_cache.key_list) == 1
        assert len(disk_cache.cache) == 1
        disk_cache.add_cache_record("bbb", "BBB")
        assert len(disk_cache.key_list) == 2
        assert len(disk_cache.cache) == 2

    @pytest.mark.parametrize('size', [1])
    def test_get_cache_value(self, disk_cache, size):
        """
        Testing retrieving cache value stored
        """
        assert disk_cache.get_cache_value("aaa") == "AAA"

        try:
            disk_cache.get_cache_value("bbb")
        except KeyError:
            assert True
        else:
            assert False

    @pytest.mark.parametrize('size', [1]) 
    def test_remove_cache(self, disk_cache, size):
        """
        Testing removing cache key
        """
        disk_cache.remove_cache("aaa")
        assert len(disk_cache.key_list) == 0
        assert len(disk_cache.cache) == 0

    @pytest.mark.parametrize('size', [1])
    def test_clean_cache(self, disk_cache, size):
        """
        Testing cache clean up
        """
        disk_cache.add_cache_record("bbb", "BBB")
        disk_cache.clean_cache()
        assert len(disk_cache.key_list) == 0
        assert len(disk_cache.cache) == 0
    
    @pytest.mark.parametrize('size', [1])
    def test_get_oldest_key(self, disk_cache, size):
        """
        Testing oldest key find situation
        """
        disk_cache.add_cache_record("bbb", "BBB")
        assert disk_cache.get_oldest_key() == "aaa"

    @pytest.mark.parametrize('size', [1])
    def test_get_contains_key(self, disk_cache, size):
        """
        Testing cache contails key
        """
        assert disk_cache.contains_key("aaa") == True
