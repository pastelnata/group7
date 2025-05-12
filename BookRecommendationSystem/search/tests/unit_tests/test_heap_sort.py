import unittest
from search.sorting.heap_sort import HeapSort

class TestHeapSort(unittest.TestCase):
    def test_maxHeapify(self):
        A = [3, 9, 2, 1, 4, 5]
        result = HeapSort.maxHeapify(A, 0, len(A))
        self.assertEqual(result, [9, 4, 2, 1, 3, 5])

    def test_buildMaxHeap(self):
        A = [3, 9, 2, 1, 4, 5]
        result = HeapSort.buildMaxHeap(A)
        self.assertEqual(result, [9, 4, 5, 1, 3, 2])

    def test_topK_within_range(self):
        A = [3, 9, 2, 1, 4, 5]
        k = 3
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [9, 5, 4])

    def test_topK_exceeding_length(self):
        A = [3, 9, 2, 1, 4, 5]
        k = 10
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [9, 5, 4, 3, 2, 1])

    def test_topK_empty_list(self):
        A = []
        k = 3
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [])

    def test_topK_single_element(self):
        A = [7]
        k = 1
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [7])

    def test_maxHeapify_with_duplicates(self):
        A = [3, 3, 3, 3, 3, 3]
        result = HeapSort.maxHeapify(A, 0, len(A))
        self.assertEqual(result, [3, 3, 3, 3, 3, 3])

    def test_buildMaxHeap_with_duplicates(self):
        A = [3, 3, 3, 3, 3, 3]
        result = HeapSort.buildMaxHeap(A)
        self.assertEqual(result, [3, 3, 3, 3, 3, 3])

    def test_topK_with_duplicates(self):
        A = [3, 3, 3, 3, 3, 3]
        k = 3
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [3, 3, 3])

    def test_topK_large_k(self):
        A = [10, 20, 30, 40, 50]
        k = 5
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [50, 40, 30, 20, 10])

    def test_topK_k_is_zero(self):
        A = [10, 20, 30, 40, 50]
        k = 0
        result = HeapSort.topK(A, k)
        self.assertEqual(result, [])