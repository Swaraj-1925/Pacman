INSIDE = 0  # 0000
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8  

def bresenham_line(surface, x1, y1, x2, y2, color):
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        surface.set_at((x1, y1), color)
        if x1 == x2 and y1 == y2:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
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

def compute_outcode(x, y, xmin, ymin, xmax, ymax):
    code = INSIDE
    if x < xmin:
        code |= LEFT
    elif x > xmax:
        code |= RIGHT
    if y < ymin:
        code |= BOTTOM
    elif y > ymax:
        code |= TOP
    return code

def cohen_sutherland_clip(x1, y1, x2, y2, xmin, ymin, xmax, ymax):
    outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
    outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)
    accept = False

    while True:
        if not (outcode1 | outcode2):
            accept = True
            break
        elif outcode1 & outcode2:
            break
        else:
            x = y = 0
            outcode_out = outcode1 if outcode1 else outcode2

            if outcode_out & TOP:
                x = x1 + (x2 - x1) * (ymax - y1) / (y2 - y1)
                y = ymax
            elif outcode_out & BOTTOM:
                x = x1 + (x2 - x1) * (ymin - y1) / (y2 - y1)
                y = ymin
            elif outcode_out & RIGHT:
                y = y1 + (y2 - y1) * (xmax - x1) / (x2 - x1)
                x = xmax
            elif outcode_out & LEFT:
                y = y1 + (y2 - y1) * (xmin - x1) / (x2 - x1)
                x = xmin

            if outcode_out == outcode1:
                x1, y1 = x, y
                outcode1 = compute_outcode(x1, y1, xmin, ymin, xmax, ymax)
            else:
                x2, y2 = x, y
                outcode2 = compute_outcode(x2, y2, xmin, ymin, xmax, ymax)

    if accept:
        return (x1, y1, x2, y2)
    else:
        return None

def constrain_ghost_movement(ghost, maze_bounds):
    xmin, ymin, xmax, ymax = maze_bounds
    new_pos = cohen_sutherland_clip(ghost.rect.x, ghost.rect.y, 
                                    ghost.rect.x + ghost.change_x, 
                                    ghost.rect.y + ghost.change_y, 
                                    xmin, ymin, xmax, ymax)
    if new_pos:
        ghost.rect.x, ghost.rect.y = new_pos[2], new_pos[3]
    else:
        # Ghost is outside bounds, reset to a valid position
        ghost.rect.x, ghost.rect.y = (xmin + xmax) // 2, (ymin + ymax) // 2
