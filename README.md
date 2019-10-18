# Bloom filter

#### Definition:

__Bloom filters__ are space efficient probabilistic data structures used to test whether 
an element is a member of a set with a null false negative rate.


A bloom filter is constituted of a bit-array of size __m__ and __k__ hash functions.
> using __k__ hash functions is equivalent to using one hash funktion with __k__  
different salts.

Adding an element to the bloom filter: compute __p__ = hash of the element % __m__
then set the __p'th__ bit of the bit-array to 1 and finally 
repeat the operations with the __k__ different hashes.

Testing an element's membership to the set: compute __p__ and check that all the bits
corresponding to all hashes are __all__ et to 1. 


#### Error rate:
False negative rate is __null__.

False positive rate is __(1 - [1 - 1/m]<sup>kn</sup>)<sup>k</sup>__ where __n__ is the
number of distinct elements inserted in the bloom filter.


#### Usage:
The class __BloomFilter__ can be used to create bloom filters with custom bit-array size
__m__ and number of hash functions __k__.

```python
from bloom_filter.bloom_filter import BloomFilter

bloom_filter = BloomFilter(bit_array_size=m, nb_salt=k)
```

If you already know the set's cardinal (number of distinct elements) __n__ to insert 
and the desired memory footprint __m__ (bit-array size), the class method
``BloomFilter.minimal_false_positive_rate_bloom_filter``` can build an instance of
```BloomFilter``` with the minimal false positive rate.
```python
from bloom_filter.bloom_filter import BloomFilter

bloom_filter = BloomFilter.minimal_false_positive_rate_bloom_filter(
        bit_array_size=m, 
        input_cardinal=n
        )
```

If you already know the set's cardinal (number of distinct elements) __n__ to insert 
and the desired false positive rate __err__, the class method 
```BloomFilter.minimal_memory_bloom_filter`` can build an instance of ```BloomFilter``` 
with the minimal memory footprint that satisfies the required error rate.
```python
from bloom_filter.bloom_filter import BloomFilter

bloom_filter = BloomFilter.minimal_memory_bloom_filter(
        input_cardinal=n, 
        error_rate=err
        )
```
