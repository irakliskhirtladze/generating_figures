from random import randint, choice
import time
import concurrent.futures


class Trapezoid:
    """A trapezoid class"""

    def __init__(self, fig_params=[0, 0, 0]):
        self.big_base = max(fig_params)
        self.small_base = min(fig_params)
        self.height = sum(fig_params) - self.big_base - self.small_base

    def __str__(self):
        return f'Trapezoid larger base -> {self.big_base}, Smaller base -> {self.small_base}, Height -> {self.height}'

    def area(self):
        avg_base = (self.big_base + self.small_base) / 2
        return avg_base * self.height

    def __lt__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() < other.area()
        return False

    def __eq__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() == other.area()
        return False

    def __ge__(self, other):
        if isinstance(other, Trapezoid):
            return not self.__lt__(other)
        return False

    def __add__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() + other.area()
        return None

    def __sub__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() - other.area()
        return None

    def __mod__(self, other):
        if isinstance(other, Trapezoid):
            return self.area() % other.area()
        return None


class Rectangle(Trapezoid):
    """A rectangle class inherited from trapezoid"""

    def __init__(self, rect=None):
        if not rect:
            rect = [0, 0]
        super().__init__([rect[0], rect[0], rect[1]])

    def area(self):
        return self.big_base * self.height

    def __str__(self):
        return f"Rectangle width -> {self.big_base}, height -> {self.height}"


class Square(Rectangle):
    """A square class inherited from trapezoid"""

    def __init__(self, side):
        super().__init__([side, side, side])

    def __str__(self):
        return f"Square side -> {self.small_base}"


def calc_trap(sides):
    return Trapezoid(sides).area()


def calc_rect(sides):
    return Rectangle(sides).area()


def calc_sq(side):
    return Square(side).area()


def regular(fig_count=0):
    """Generating N figures for each figure class using regular for-loops"""
    start_time = time.perf_counter()

    traps = [Trapezoid([randint(1, 200), randint(1, 200), randint(1, 200)]).area() for _ in range(fig_count)]
    rects = [Rectangle([randint(1, 200), randint(1, 200)]).area() for _ in range(fig_count)]
    squares = [Square(randint(1, 200)).area() for _ in range(fig_count)]

    end_time = time.perf_counter()
    print(f'Using regular loops finished in {round(end_time - start_time, 3)} seconds')

    return {'traps': traps, 'rects': rects, 'squares': squares}


def threads(fig_count=0):
    start_time = time.perf_counter()

    with concurrent.futures.ThreadPoolExecutor() as exe:
        trap_areas = list(
            exe.map(calc_trap, [[randint(1, 200), randint(1, 200), randint(1, 200)] for _ in range(fig_count)]))
        rect_areas = list(exe.map(calc_rect, [[randint(1, 200), randint(1, 200)] for _ in range(fig_count)]))
        sq_areas = list(exe.map(calc_sq, [randint(1, 200) for _ in range(fig_count)]))

    end_time = time.perf_counter()
    print(f'Using multithreading finished in {round(end_time - start_time, 3)} seconds')

    return {'trap_areas': trap_areas, 'rect_areas': rect_areas, 'square_areas': sq_areas}


def processes(fig_count=0):
    start_time = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as exe:
        trap_areas = list(
            exe.map(calc_trap, [[randint(1, 200), randint(1, 200), randint(1, 200)] for _ in range(fig_count)]))
        rect_areas = list(exe.map(calc_rect, [[randint(1, 200), randint(1, 200)] for _ in range(fig_count)]))
        sq_areas = list(exe.map(calc_sq, [randint(1, 200) for _ in range(fig_count)]))

    end_time = time.perf_counter()
    print(f'Using multiprocessing finished in {round(end_time - start_time, 3)} seconds')

    return {'trap_areas': trap_areas, 'rect_areas': rect_areas, 'square_areas': sq_areas}


def threader_for_mixed(fig_count):
    """The function to perform multithreading within each process.
    It is being called within mixed() function """
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as inner_executor:
        traps = list(inner_executor.map(calc_trap, [[randint(1, 200), randint(1, 200), randint(1, 200)] for _ in
                                                    range(fig_count)]))
        rects = list(inner_executor.map(calc_rect, [[randint(1, 200), randint(1, 200)] for _ in range(fig_count)]))
        squares = list(inner_executor.map(calc_sq, [randint(1, 200) for _ in range(fig_count)]))
    return traps, rects, squares


def mixed():
    """Generating N figures for each figure class"""
    start_time = time.perf_counter()

    with concurrent.futures.ProcessPoolExecutor(max_workers=5) as executor:
        results = executor.map(threader_for_mixed, range(5))

        # Collecting the results from each process
        trap_areas, rect_areas, sq_areas = [], [], []
        for result in results:
            traps, rects, squares = result
            trap_areas.extend(traps)
            rect_areas.extend(rects)
            sq_areas.extend(squares)

    end_time = time.perf_counter()
    print(f'Using mixed approach finished in {round(end_time - start_time, 3)} seconds')

    return {'traps': trap_areas, 'rects': rect_areas, 'squares': sq_areas}


if __name__ == "__main__":
    n_figures = 10_000
    print(f'*** Calculation of {n_figures} figures of each type ***')
    regular(n_figures)
    threads(n_figures)
    processes(n_figures)
    mixed()
