import numpy as np

from .utils import sign, is_in_bounds, weighted_random_choice


def horizontal(size):
    width, height = size
    for y in range(height):
        yield ((x, y) for x in range(width))


def vertical(size):
    width, height = size
    for x in range(width):
        yield ((x, y) for y in range(height))


def diagonal(size):
    width, height = size
    for offset in range(height - 1, -width, -1):
        yield ((x, x + offset) for x in range(max(0, -offset), min(width, height - offset)))


def single_diagonal(size):
    width, height = size

    def path_iter():
        for offset in range(height - 1, -width, -1):
            for x in range(max(0, -offset), min(width, height - offset)):
                yield (x, x + offset)

    yield path_iter()


def line(size, start, slope):
    err = -1.0
    if np.abs(slope) > 1:
        slope = 1 / slope
        switch = True
    else:
        switch = False
    sgn = sign(slope)
    dx = dy = 0
    current = start
    x0, y0 = start
    while is_in_bounds(current, (0, 0), size):
        yield current
        dx += 1
        err += np.abs(slope)
        if err > 0:
            dy += sgn
            err -= 1
        current = (x0+dx, y0+dy) if not switch else (x0+np.abs(dy), y0+sgn*dx)


def angle(size, angle):
    angle = -angle
    if angle % 180 == 0:
        yield from horizontal(size)
        return
    if angle % 180 == 90:
        yield from vertical(size)
        return
    width, height = size
    slope = np.tan(np.radians(angle))
    start_y = 0 if slope > 0 else height - 1
    for x in range(width-1, 0, -1):
        yield line(size, (x, start_y), slope)
    for y in range(height):
        yield line(size, (0, y), slope)


def rectangles(size):
    def path_iter():
        for x in range(min_x, max_x):
            yield (x, min_y)

        if min_y + 1 == max_y: # In case there's only 1 row
            return
        for y in range(min_y + 1, max_y):
            yield (max_x - 1, y)
        for x in range(max_x - 2, min_x - 1, -1):
            yield (x, max_y - 1)
        for y in range(max_y - 2, min_y, -1):
            yield (min_x, y)

    width, height = size
    min_x, max_x = 0, width
    min_y, max_y = 0, height

    while min_x < max_x and min_y < max_y:
        yield path_iter()

        min_x += 1
        max_x -= 1
        min_y += 1
        max_y -= 1


def random(size, distribution=None, start=None):
    def path_iter(start_point):
        x, y = start_point
        while True:
            dx, dy = weighted_random_choice(iter(distribution.items()))
            x += dx
            y += dy
            if x < 0 or x >= width or y < 0 or y >= height:
                return
            yield (x, y)

    width, height = size
    neighbors = [(dx, dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if dy != 0 or dx != 0]
    if distribution is None:
        distribution = {n: 0.125 for n in neighbors}
    else:
        for n in neighbors:
            if n not in distribution:
                distribution[n] = 0
        neighbor_sum = sum(distribution[n] for n in neighbors)
        distribution = {n: p / float(neighbor_sum) for n, p in distribution.items()}

    if start is None:
        start = [(np.random.randint(width), np.random.randint(height)) for _ in range(10)]

    for x0, y0 in start:
        yield path_iter((x0, y0))


def horizontal_random(size):
    _, height = size
    distribution = {(1, dy): 1 / 3.0 for dy in [-1, 0, 1]}
    start = [(0, y) for y in range(height)]
    return random(size, distribution, start)


def vertical_random(size):
    width, _= size
    distribution = {(dx, 1): 1 / 3.0 for dx in [-1, 0, 1]}
    start = [(x, 0) for x in range(width)]
    return random(size, distribution, start)


def bresenham(radius):
    x, y = radius, 0
    r2 = radius ** 2
    coords = []
    while x >= y:
        coords.append((x, y))
        y += 1
        if abs((x-1)**2 + y**2 - r2) < abs(x**2 + y**2 - r2):
            x -= 1

    if coords[-1][0] != coords[-1][1]:
        coords.append((coords[-1][0], coords[-1][0]))

    return coords


def concentric_circles(center, radius, size=None):
    c_out = bresenham(radius + 1)
    c_in = bresenham(radius)

    coords = []

    for x, y in c_in:
        for x1 in range(x, c_out[y][0]):
            coords.append((x1, y))

    next_octant = [(y, x) for x, y in reversed(coords)]
    coords.extend(next_octant)
    next_quadrant = [(-y, x) for x, y in coords]
    coords.extend(next_quadrant)
    next_half = [(-x, -y) for x, y in coords]
    coords.extend(next_half)

    for x, y in coords:
        c = x + center[0], y + center[1]
        if size is not None:
            if not is_in_bounds(c, (0, 0), size):
                continue
        yield c


def fill_concentric_circles(center, radius, size=None):
    for r in range(radius):
        yield concentric_circles(center, r, size=size)


def circles(size):
    width, height = size
    x0, y0 = width // 2, height // 2
    max_radius = int(np.sqrt(2) * max(height, width))
    yield from fill_concentric_circles((x0, y0), max_radius, size=size)


def filled_circles(size, radius=100):
    width, height = size
    radius = int(radius)
    dx = dy = int(2 * radius / np.sqrt(2))
    for x in range(dx // 2, width + dx, dx):
        for y in range(dy // 2, height + dy, dy):
            yield from fill_concentric_circles((x, y), radius, size=size)
