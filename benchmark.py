"""Measure both versions on identical inputs and save raw and median times."""

import csv
import platform
import random
import statistics
import sys
from pathlib import Path
from time import perf_counter_ns
from quicksort import quicksort, randomized_quicksort

SIZES = (500, 1000, 2000)
REPEATS = 3
SEED = 2026


def make_input(distribution, size, rng):
    if distribution == "random":
        values = list(range(size))
        rng.shuffle(values)
        return values
    if distribution == "sorted":
        return list(range(size))
    if distribution == "reverse":
        return list(range(size, 0, -1))
    return [7] * size


def run():
    output = Path(__file__).resolve().parent
    rows = []
    distributions = ("random", "sorted", "reverse", "equal")
    warmup = list(range(100, 0, -1))
    quicksort(warmup.copy())
    randomized_quicksort(warmup.copy(), random.Random(SEED))
    for distribution in distributions:
        for size in SIZES:
            for trial in range(REPEATS):
                seed = SEED + size * 10 + trial
                original = make_input(distribution, size, random.Random(seed))
                expected = sorted(original)
                algorithms = ["deterministic", "randomized"]
                if trial % 2:
                    algorithms.reverse()
                for algorithm in algorithms:
                    values = original.copy()
                    rng = random.Random(seed + 100000)
                    start = perf_counter_ns()
                    if algorithm == "deterministic":
                        quicksort(values)
                    else:
                        randomized_quicksort(values, rng)
                    elapsed = (perf_counter_ns() - start) / 1000000
                    if values != expected:
                        raise AssertionError("Sorting produced incorrect output")
                    rows.append(dict(distribution=distribution, size=size,
                                     trial=trial + 1, algorithm=algorithm,
                                     milliseconds=elapsed))
    with (output / "benchmark_raw.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = []
    for distribution in distributions:
        for size in SIZES:
            entry = dict(distribution=distribution, size=size)
            for algorithm in ("deterministic", "randomized"):
                samples = [r["milliseconds"] for r in rows
                           if r["distribution"] == distribution
                           and r["size"] == size and r["algorithm"] == algorithm]
                entry[algorithm + "_ms"] = statistics.median(samples)
            summary.append(entry)
    with (output / "benchmark_summary.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    environment = (f"Python: {sys.version}\nPlatform: {platform.platform()}\n"
                   f"Processor: {platform.processor() or 'Not reported'}\n"
                   f"Repeats: {REPEATS}\nInput and pivot seeds: derived from {SEED}\n")
    (output / "environment.txt").write_text(environment)
    for row in summary:
        print(row)
    return summary


if __name__ == "__main__":
    run()
