import pytest
from bloom_filter.bloom_filter import BloomFilter
from bloom_filter.tools import false_positive_rate


class TestBloomFilter:
    @pytest.mark.parametrize("bit_array_size, nb_salt", [
        (100, 1),
        (1000, 2),
        (10 ** 4, 32)
    ])
    def test_bit_array_size(self, bit_array_size, nb_salt):
        bloom_filter = BloomFilter(
            bit_array_size=bit_array_size,
            nb_salt=nb_salt
        )
        assert len(bloom_filter.bit_array) == bit_array_size
        assert bloom_filter.bit_array_size == bit_array_size

    @pytest.mark.parametrize("bit_array_size, nb_salt", [
        (100, 1),
        (1000, 2),
        (10 ** 4, 32)
    ])
    def test_all_bits_should_be_set_to_false(self, bit_array_size, nb_salt):
        bloom_filter = BloomFilter(
            bit_array_size=bit_array_size,
            nb_salt=nb_salt
        )
        for bit in bloom_filter.bit_array:
            assert bit is False

    @pytest.mark.parametrize("item, bit_array_size, nb_salt", [
        ("bloom", 10, 1),
        ("filter", 1000, 2),
        ("data", 10 ** 4, 32)
    ])
    def test_add_item(self, item, bit_array_size, nb_salt):
        bloom_filter = BloomFilter(
            bit_array_size=bit_array_size,
            nb_salt=nb_salt
        )
        for salt in range(nb_salt):
            custom_address = hash(''.join([str(salt), str(item)])) % bit_array_size
            assert bloom_filter.bit_array[custom_address] is False
        bloom_filter.add_item(item=item)
        for salt in range(nb_salt):
            custom_address = hash(''.join([str(salt), str(item)])) % bit_array_size
            assert bloom_filter.bit_array[custom_address]

    @pytest.mark.parametrize("item, bit_array_size, nb_salt", [
        ("bloom", 10, 1),
        ("filter", 1000, 2),
        ("data", 10 ** 4, 32)
    ])
    def test_retrieve_item(self, item, bit_array_size, nb_salt):
        bloom_filter = BloomFilter(
            bit_array_size=bit_array_size,
            nb_salt=nb_salt
        )
        assert bloom_filter.retrieve_item(item=item) is False
        bloom_filter.add_item(item=item)
        assert bloom_filter.retrieve_item(item=item)

    @pytest.mark.parametrize("bit_array_size, input_cardinal", [
        (10 ** 3, 100),
        (10 ** 4, 100),
        (10 ** 5, 100)
    ])
    def test_minimal_false_positive_rate(self, bit_array_size, input_cardinal):
        bloom_filter = BloomFilter.minimal_false_positive_rate_bloom_filter(
            bit_array_size=bit_array_size,
            input_cardinal=input_cardinal
        )
        assert false_positive_rate(
            bit_array_size=bit_array_size,
            nb_salt=bloom_filter.nb_salt,
            input_cardinal=input_cardinal
        ) < false_positive_rate(
            bit_array_size=bit_array_size,
            nb_salt=bloom_filter.nb_salt - 1,
            input_cardinal=input_cardinal
        )
        assert false_positive_rate(
            bit_array_size=bit_array_size,
            nb_salt=bloom_filter.nb_salt,
            input_cardinal=input_cardinal
        ) < false_positive_rate(
            bit_array_size=bit_array_size,
            nb_salt=bloom_filter.nb_salt + 1,
            input_cardinal=input_cardinal
        )

    @pytest.mark.parametrize("input_cardinal, error_rate", [
        (1000, 0.01),
        (1000, 0.05),
        (10 ** 4, 0.02)
    ])
    def test_minimal_memory_error_rate(self, input_cardinal, error_rate):
        bloom_filter = BloomFilter.minimal_memory_bloom_filter(
            input_cardinal=input_cardinal, error_rate=error_rate)
        observed_error_rate = false_positive_rate(
            bit_array_size=bloom_filter.bit_array_size,
            nb_salt=bloom_filter.nb_salt,
            input_cardinal=input_cardinal
        )
        assert observed_error_rate == pytest.approx(
            expected=error_rate,
            abs=error_rate / 20  # 5% interval
        ), "Observed error rate {observed} is higher than expected {expected}".format(
            observed=observed_error_rate,
            expected=error_rate
        )
