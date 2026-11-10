"""Deterministic and randomized Quicksort with bounded recursion space."""

import random


def partition(values: list[int], low: int, high: int) -> int:
    """Place the final value in its sorted position using Lomuto partitioning."""
    pivot = values[high]
    boundary = low
    for index in range(low, high):
        if values[index] <= pivot:
            values[boundary], values[index] = values[index], values[boundary]
            boundary += 1
    values[boundary], values[high] = values[high], values[boundary]
    return boundary


def _sort(values: list[int], low: int, high: int,
          rng: random.Random | None) -> None:
    """Recurse on the smaller partition and loop over the larger partition."""
    while low < high:
        if rng is not None:
            pivot_index = rng.randrange(low, high + 1)
            values[pivot_index], values[high] = values[high], values[pivot_index]
        pivot_index = partition(values, low, high)
        # Each recursive call receives at most half of the current elements.
        if pivot_index - low < high - pivot_index:
            _sort(values, low, pivot_index - 1, rng)
            low = pivot_index + 1
        else:
            _sort(values, pivot_index + 1, high, rng)
            high = pivot_index - 1


def quicksort(values: list[int]) -> None:
    """Sort the supplied list in place using the final element as the pivot."""
    _sort(values, 0, len(values) - 1, None)


def randomized_quicksort(values: list[int],
                         rng: random.Random | None = None) -> None:
    """Sort in place using a uniformly selected pivot for each partition.

    Supply a seeded Random instance when reproducible pivot choices are needed.
    """
    generator = rng if rng is not None else random.Random()
    _sort(values, 0, len(values) - 1, generator)


if __name__ == "__main__":
    sample = [17, 4, 12, 4, 9, 1]
    first = sample.copy()
    second = sample.copy()
    quicksort(first)
    randomized_quicksort(second, random.Random(42))
    print("Original:", sample)
    print("Deterministic:", first)
    print("Randomized:", second)
