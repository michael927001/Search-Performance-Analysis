"""
Search Assignment Starter Code
Implement three search algorithms and benchmark their performance.
"""

import json
import time
import random


# ============================================================================
# PART 1: Linear Search
# ============================================================================

def linear_search(data, target):
    for i in range(len(data)):
        if data[i] == target:
            return i
    return -1


# ============================================================================
# PART 2: Binary Search (Iterative)
# ============================================================================

def binary_search_iterative(data, target):
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2

        if data[mid] == target:
            return mid
        elif data[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1


# ============================================================================
# PART 3: Binary Search (Recursive)
# ============================================================================

def binary_search_recursive(data, target, left=None, right=None):
    if left is None:
        left = 0
    if right is None:
        right = len(data) - 1

    if left > right:
        return -1

    mid = (left + right) // 2

    if data[mid] == target:
        return mid
    elif data[mid] < target:
        return binary_search_recursive(data, target, mid + 1, right)
    else:
        return binary_search_recursive(data, target, left, mid - 1)


# ============================================================================
# BENCHMARKING & TESTING
# ============================================================================

def load_dataset(filename):
    with open(f"datasets/{filename}", "r") as f:
        return json.load(f)


def load_test_cases():
    with open("datasets/test_cases.json", "r") as f:
        return json.load(f)


def test_search_correctness():
    print("="*70)
    print("TESTING SEARCH CORRECTNESS")
    print("="*70 + "\n")
    
    sorted_data = [1, 3, 5, 7, 9, 11, 13, 15]
    unsorted_data = [7, 2, 9, 1, 5, 13, 3, 11]
    
    print("Test 1: Linear search on unsorted data")
    result = linear_search(unsorted_data, 9)
    print(f"  Expected: 2, Got: {result}, {'✓ PASS' if result == 2 else '✗ FAIL'}")
    
    print("\nTest 2: Linear search - item not found")
    result = linear_search(unsorted_data, 99)
    print(f"  Expected: -1, Got: {result}, {'✓ PASS' if result == -1 else '✗ FAIL'}")
    
    print("\nTest 3: Binary search iterative on sorted data")
    result = binary_search_iterative(sorted_data, 9)
    print(f"  Expected: 4, Got: {result}, {'✓ PASS' if result == 4 else '✗ FAIL'}")
    
    print("\nTest 4: Binary search iterative - item not found")
    result = binary_search_iterative(sorted_data, 10)
    print(f"  Expected: -1, Got: {result}, {'✓ PASS' if result == -1 else '✗ FAIL'}")
    
    print("\nTest 5: Binary search recursive on sorted data")
    result = binary_search_recursive(sorted_data, 13)
    print(f"  Expected: 6, Got: {result}, {'✓ PASS' if result == 6 else '✗ FAIL'}")
    
    print("\nTest 6: Binary search recursive - item not found")
    result = binary_search_recursive(sorted_data, 8)
    print(f"  Expected: -1, Got: {result}, {'✓ PASS' if result == -1 else '✗ FAIL'}")


def benchmark_algorithm(search_func, data, targets):
    start = time.time()
    
    for target in targets:
        search_func(data, target)
    
    end = time.time()
    return (end - start) / len(targets)


def benchmark_all_datasets():
    print("\n" + "="*70)
    print("BENCHMARKING SEARCH ALGORITHMS")
    print("="*70 + "\n")
    
    datasets = {
        "customer_ids.json": "Unsorted Customer IDs (100K)",
        "product_catalog.json": "Pre-sorted Product Catalog (50K)",
        "config_settings.json": "Small Config Settings (500)",
        "dictionary_words.json": "Dictionary Words (10K)"
    }
    
    test_cases = load_test_cases()
    
    for filename, description in datasets.items():
        print(f"Dataset: {description}")
        print("-" * 70)
        
        data = load_dataset(filename)
        dataset_key = filename.replace(".json", "")
        
        targets = test_cases[dataset_key]["present"][:50] + test_cases[dataset_key]["absent"][:50]
        random.shuffle(targets)
        
        linear_time = benchmark_algorithm(linear_search, data, targets)
        print(f"  Linear Search:              {linear_time*1000:.4f} ms per search")
        
        if "unsorted" in description.lower() or "small config" in description.lower():
            sorted_data = sorted(data)
            sort_start = time.time()
            sorted(data)
            sort_time = time.time() - sort_start
            print(f"  Time to sort data:          {sort_time*1000:.2f} ms")
        else:
            sorted_data = data
        
        binary_iter_time = benchmark_algorithm(binary_search_iterative, sorted_data, targets)
        print(f"  Binary Search (Iterative):  {binary_iter_time*1000:.4f} ms per search")
        
        binary_rec_time = benchmark_algorithm(binary_search_recursive, sorted_data, targets)
        print(f"  Binary Search (Recursive):  {binary_rec_time*1000:.4f} ms per search")
        
        print()


def analyze_preprocessing_costs():
    print("="*70)
    print("PREPROCESSING COST ANALYSIS")
    print("="*70 + "\n")
    
    data = load_dataset("customer_ids.json")
    test_cases = load_test_cases()
    targets = test_cases["customer_ids"]["present"][:100]
    
    sort_start = time.time()
    sorted_data = sorted(data)
    sort_time = time.time() - sort_start
    
    linear_time = benchmark_algorithm(linear_search, data, targets[:10])
    binary_time = benchmark_algorithm(binary_search_iterative, sorted_data, targets[:10])
    
    print(f"One-time sort cost: {sort_time*1000:.2f} ms")
    print(f"Linear search time: {linear_time*1000:.4f} ms per search")
    print(f"Binary search time: {binary_time*1000:.4f} ms per search")


if __name__ == "__main__":
    print("SEARCH ASSIGNMENT - STARTER CODE")
    print("Implement the search functions above, then run tests.\n")

    test_search_correctness()
    benchmark_all_datasets()
    analyze_preprocessing_costs()