class HeapSort:
    def maxHeapify(A, i, n):
        left = 2 * i + 1
        right = 2 * i + 2
        largest = i
        if left < n and A[left] > A[largest]:
            largest = left
        if right < n and A[right] > A[largest]:
            largest = right
        if largest != i:
            A[i], A[largest] = A[largest], A[i]
            HeapSort.maxHeapify(A, largest, n)
        return A

    def buildMaxHeap(A):
        n = len(A)
        for i in range(n // 2, -1, -1):
            A =  HeapSort.maxHeapify(A, i, n)
        return A

    def topK(A, k):
        n = len(A)
        if k >= n:
            return sorted(A, reverse=True)
        HeapSort.buildMaxHeap(A)
        top_k = []
        for _ in range(k):
            # Extract max element
            A[0], A[n - 1] = A[n - 1], A[0]
            top_k.append(A.pop()) 
            n -= 1
            HeapSort.maxHeapify(A, 0, n)
        return top_k