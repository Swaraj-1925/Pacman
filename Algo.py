INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8  

def bresenham_circle(surface, xc, yc, radius, color):
    x = 0
    y = radius
    d = 3 - 2 * radius

    def plot_points(xc, yc, x, y):
        surface.set_at((xc + x, yc + y), color)
        surface.set_at((xc - x, yc + y), color)
        surface.set_at((xc + x, yc - y), color)
        surface.set_at((xc - x, yc - y), color)
        surface.set_at((xc + y, yc + x), color)
        surface.set_at((xc - y, yc + x), color)
        surface.set_at((xc + y, yc - x), color)
        surface.set_at((xc - y, yc - x), color)

    while y >= x:
        plot_points(xc, yc, x, y)
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        plot_points(xc, yc, x, y)

def flood_fill(surface, x, y, fill_color, target_color):
    width, height = surface.get_size()
    stack = [(x, y)]
    if target_color == fill_color:
        return

    while stack:
        x, y = stack.pop()
        if x < 0 or x >= width or y < 0 or y >= height:
            continue
        if surface.get_at((x, y)) != target_color:
            continue
        surface.set_at((x, y), fill_color)
        stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
