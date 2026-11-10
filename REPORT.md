# Assignment 5: Quicksort Implementation, Analysis, and Randomization

## Introduction

This assignment compares deterministic Quicksort with randomized Quicksort. Both versions partition a list around a pivot and then sort the remaining sections. The main difference is how each version selects that pivot. The deterministic version uses the final element, while the randomized version selects a position uniformly from the current subarray. I used the same partition procedure for both versions to keep the comparison focused on pivot selection.

Cormen et al. (2022, Chapter 7) explain that Quicksort has strong average performance but can become inefficient when its partitions are consistently unbalanced. This project examines that relationship through complexity analysis and measured execution times.

## Implementation and Design Choices

The implementation uses Lomuto partitioning. A boundary tracks the section containing values less than or equal to the pivot. As the algorithm scans the subarray, qualifying values move into that section. The final swap places the pivot in its sorted position. The left section then contains values no greater than the pivot, and the right section contains larger values.

The randomized version first selects a pivot index and swaps that value with the final element. Both versions then call the same partition function. Random selection includes both endpoints of the current subarray.

Both functions modify the original list and return None. They avoid slicing and temporary partition lists. They are not stable because swaps can change the original relative order of records with equal keys.

Instead of recursively processing both partitions, the implementation recursively sorts the smaller partition and processes the larger partition through a loop. Both partitions are still sorted. This design prevents deeply nested calls on ordered inputs without changing the partitioning behavior or its worst case running time. The implementation does not increase Python's recursion limit.

Correctness follows from the partition invariant. Before each scan step, values before the boundary are no greater than the pivot, and the examined values between the boundary and the scan position are greater than the pivot. The final swap fixes the pivot position. Applying the same reasoning to the remaining sections produces a sorted list. Sections with fewer than two values require no work.

## Time Complexity

### Best Case

The best case occurs when partitions remain approximately balanced. Partitioning a section of size n takes Theta(n) time. Balanced sections produce the recurrence T(n) = 2T(n / 2) + Theta(n). There are approximately log n partition levels with Theta(n) total work at each level. The resulting running time is Theta(n log n) for both versions (Cormen et al., 2022).

### Average and Expected Cases

For deterministic Quicksort on uniformly random permutations of distinct values, the average running time is Theta(n log n). Every split does not need to be perfectly balanced. Enough useful splits occur to limit the expected total work.

For randomized Quicksort, the expectation is over random pivot choices for any fixed input of distinct values. Consider two values with sorted ranks i and j. They are compared only when one becomes the first pivot selected from the values with ranks i through j. This has probability 2 / (j minus i plus 1). Summing these probabilities gives an expected comparison count of 2(n + 1)H_n minus 4n, where H_n is the nth harmonic number. Since H_n grows as Theta(log n), expected running time is Theta(n log n) (Cormen et al., 2022).

### Worst Case

The worst case occurs when each partition removes only one pivot and leaves the remaining values on one side. The recurrence becomes T(n) = T(n minus 1) + Theta(n). The total work follows the sum n + (n minus 1) + ... + 1, producing Theta(n squared) time.

Using the final element as the pivot produces this pattern on sorted and reverse sorted distinct inputs. Randomization makes repeated extreme pivot selections unlikely, but does not eliminate the quadratic worst case. For distinct values, the probability of selecting an extreme value at every nontrivial partition is 2 to the power of (n minus 1) divided by n factorial.

Equal values expose a separate limitation. With this partition procedure, every value equal to the pivot moves into the same section. An input containing only equal values therefore takes Theta(n squared) time in both versions. Random selection cannot change the pivot value in that situation.

## Space Complexity and Overhead

A conventional implementation that recursively processes both partitions uses O(log n) expected stack space and O(n) worst case stack space. This implementation instead guarantees O(log n) auxiliary stack space because every recursive call receives at most half of the current section. On extremely unbalanced partitions, the larger section stays in the loop rather than creating another nested call.

Partitioning itself requires O(1) additional space. The random generator also has fixed size state independent of the list length. Function calls, comparisons, swaps, loop operations, and random number generation contribute execution overhead. Randomization adds a generator call and a pivot swap for each partition. The benchmark copies lists for fairness, but these copies are outside the timed region and are not part of the sorting function's space requirement.

## Empirical Method

The experiment used input sizes of 500, 1,000, and 2,000 values. It tested random permutations, sorted values, reverse sorted values, and equal values. Each condition had three trials. Both algorithms received copies of the same original input for each trial. Algorithm order alternated between trials to reduce systematic ordering effects.

Input generation, copying, random generator initialization, and correctness checking were excluded from the timed region. Pivot generation during sorting remained included. Timing used perf_counter_ns, with results converted to milliseconds. Every output was checked against Python's sorted result after timing. Reported values are medians rather than individual trial results.

The environment file records Python and platform information. Seeds make the generated inputs and pivot choices reproducible, but execution times will vary between systems and runs.

## Measured Results

| Distribution | Size | Deterministic milliseconds | Randomized milliseconds |
| :--- | :--- | :--- | :--- |
| Random | 500 | 0.305 | 0.428 |
| Random | 1,000 | 0.667 | 0.968 |
| Random | 2,000 | 1.549 | 2.008 |
| Sorted | 500 | 6.702 | 0.360 |
| Sorted | 1,000 | 29.539 | 0.852 |
| Sorted | 2,000 | 127.669 | 1.811 |
| Reverse | 500 | 4.976 | 0.376 |
| Reverse | 1,000 | 22.348 | 0.886 |
| Reverse | 2,000 | 91.514 | 1.949 |
| Equal | 500 | 6.354 | 6.478 |
| Equal | 1,000 | 27.572 | 27.850 |
| Equal | 2,000 | 114.447 | 115.533 |

## Discussion of Results

On random input, the deterministic version was faster at every tested size. At 2,000 values, it required approximately 1.549 milliseconds compared with 2.008 milliseconds for randomized Quicksort. A final element pivot already has a random rank when the input is a random permutation. Additional random selection therefore introduced overhead without producing a measured advantage in these trials.

Ordered inputs showed a different result. At 2,000 sorted values, deterministic Quicksort required approximately 127.669 milliseconds, while randomized Quicksort required 1.811 milliseconds. On reverse sorted input, the corresponding results were 91.514 and 1.949 milliseconds. Randomization prevented input order from consistently forcing extreme pivots.

Doubling the sorted input from 1,000 to 2,000 values increased deterministic execution time by approximately 4.32 times. The randomized version increased by approximately 2.13 times. These measurements are consistent with quadratic growth for deterministic Quicksort and expected n log n growth for randomized Quicksort. They illustrate the theoretical patterns but do not prove asymptotic complexity.

Equal input produced poor results for both versions. At 2,000 values, deterministic Quicksort required 114.447 milliseconds and randomized Quicksort required 115.533 milliseconds. This confirms that random pivot selection does not resolve the duplicate value limitation of this partition procedure. A partition method that separates values into smaller, equal, and larger groups would address that problem more directly.

The experiment used modest input sizes and three trials per condition. Shared execution resources, interpreter overhead, garbage collection, and timer variability may affect the measurements. Larger experiments with more repetitions would support stronger performance conclusions. The correctness suite passed four test methods covering empty lists, single values, negative values, duplicates, ordered inputs, and random inputs.

## Conclusion

The results show why pivot selection matters. Deterministic Quicksort performed well on random input but slowed substantially on ordered data. Randomized Quicksort reduced sensitivity to input order while adding some overhead. It retained a quadratic worst case and did not solve the equal value problem. Recursing only on the smaller partition controlled stack usage without changing these time complexity limits.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). MIT Press. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
