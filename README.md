# Assignment 5: Quicksort

## Overview

This project implements deterministic and randomized Quicksort in Python. Both versions use Lomuto partitioning and recursively process the smaller partition to control stack usage.

## Requirements

Python 3.10 or newer. All executable code uses the Python standard library. No package installation is required.

## Project Files

* quicksort.py contains both sorting functions and a demonstration.
* test_quicksort.py contains correctness tests.
* benchmark.py runs the timing experiment.
* REPORT.md contains implementation details and analysis.
* benchmark_raw.csv contains individual trial results.
* benchmark_summary.csv contains median execution times.
* environment.txt records the benchmark environment.
* test_results.txt records the supplied correctness test run.

## Run the Demonstration

Open a terminal in the project folder and run:

```bash
python quicksort.py
```

## Run the Tests

```bash
python test_quicksort.py
```

## Run the Benchmark

```bash
python benchmark.py
```

The benchmark tests 500, 1,000, and 2,000 values across four distributions with three repetitions. It validates every sorted result. Running it again replaces the CSV files and environment record. Existing report measurements describe the supplied run. Update the report if you replace those measurements.

## Summary of Findings

The deterministic version was faster on random input in the supplied run. The randomized version was substantially faster on sorted and reverse sorted input. Both versions showed quadratic behavior when every value was equal. Neither algorithm is stable. The sorting functions modify the supplied list and return None.

Best case time is Theta(n log n). Average deterministic time on random permutations and expected randomized time on fixed distinct input are Theta(n log n). Worst case time is Theta(n squared). This implementation uses O(log n) auxiliary stack space in the worst case.



## Reference

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/