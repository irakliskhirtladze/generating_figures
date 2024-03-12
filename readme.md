# Number array generation and calculation with different methods

### Description

The program compares performance of regular loops, multithreading, multiprocessing and
mixed (several processes with several threads in each) approaches for object generation and numerical calculations.

Sadly I couldn't work on GUI this time, but can be added in near future.

Run 'figures.py' to create certain number of trapezoids, rectangles and squares with randomly generated dimensions.
The number of each figure can be set at the bottom of the file: n_figures = <some integer here>

There are several functions for each above-mentioned approach:
    generate_figures()
    threads()
    multiprocess()
    mixed()

### Observations

I have run the program for 1000, 10_000, 100_000 and a Million parameters.

Regular loops always outperforms multithreading and multiprocessing.

It also outperforms mixed approach for low number of parameters,
but as number of parameters increases significantly (100_000 and more),
the mixed approach gives the best results.

The worst performance was shown by multiprocessing.

### Requirements

Python 3.x

