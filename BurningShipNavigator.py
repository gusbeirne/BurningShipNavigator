import pygame
import math
from collections import namedtuple

pygame.init()


(WINDOW_WIDTH, WINDOW_HEIGHT) = (500, 500)
ZOOM_FACTOR = 2

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()


FractalView = namedtuple('FractalView',
                         'complex_extent_x complex_extent_y complex_center max_iterations window_x window_y')


def set_pixel(x, y, color):
    pygame.draw.circle(screen, (color, color, color), (x, y), 0, 0)


def draw_fractal(pixel_color_function, fractal_view):
    for x in range(fractal_view.window_x):
        for y in range(fractal_view.window_y):
            set_pixel(x, y,
                      pixel_color_function(x, y, fractal_view))
    pygame.display.update()


def pixel_to_complex(pixel_x, pixel_y, fractal_view):
    fv = fractal_view
    real = pixel_x * fv.complex_extent_x / fv.window_x + fv.complex_center.real - (fv.complex_extent_x / 2)
    imag = pixel_y * (-1) * fv.complex_extent_y / fv.window_y + fv.complex_center.imag + (fv.complex_extent_y / 2)
    return complex(real, imag)


def burning_ship_transform(z, c):
    return complex(abs(z.real), abs(z.imag))**2 + c


def recursive_burning_ship_transform(c, num_iterations):
    if num_iterations == 1:
        return burning_ship_transform(0, c)
    elif num_iterations > 1:
        return burning_ship_transform(recursive_burning_ship_transform(c, num_iterations-1), c)
    else:
        print("error: non-positive num_iterations")
        return None


Escape = namedtuple('Escape', 'iterations magnitude')


def burning_ship_escape_value(c, max_iterations):
    z = 0
    for n in range(1, max_iterations + 1):
        z = burning_ship_transform(z, c)
        if abs(z) > 2:
            escape = Escape(n, abs(z))
            return escape
    escape = Escape(max_iterations, abs(c))
    return escape


def escape_value_to_color(escape, max_iterations):
    #if escape.magnitude <= 0:
        #return 0
   # smooth_iterations = escape.iterations - 1 + math.log(escape.magnitude)/math.log(2)
    color = 255 - ((escape.iterations / (max_iterations + 1)) * 255)
    return color


def burning_ship_pixel_color(pixel_x, pixel_y, fractal_view):
    fv = fractal_view
    c = pixel_to_complex(pixel_x, pixel_y, fractal_view)
    escape_value = burning_ship_escape_value(c, fv.max_iterations)
    return escape_value_to_color(escape_value, fv.max_iterations)


def zoom(fractal_view, zoom_factor):
    new_complex_extent_x = fractal_view.complex_extent_x / zoom_factor
    new_complex_extent_y = fractal_view.complex_extent_y / zoom_factor
    return fractal_view._replace(complex_extent_x=new_complex_extent_x, complex_extent_y=new_complex_extent_y)


def recenter(fractal_view, new_complex_center):
    return fractal_view._replace(complex_center=new_complex_center)


view0 = FractalView(
    complex_extent_x=4,
    complex_extent_y=4,
    complex_center=complex(0, 0),
    max_iterations=64,
    window_x=WINDOW_WIDTH,
    window_y=WINDOW_HEIGHT
)
current_view = view0
previous_view = view0

draw_fractal(burning_ship_pixel_color, view0)
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                (click_x, click_y) = event.pos
                previous_view = current_view
                current_view = zoom(current_view, ZOOM_FACTOR)
                new_center = pixel_to_complex(click_x, click_y, previous_view)
                current_view = recenter(current_view, new_center)
                draw_fractal(burning_ship_pixel_color, current_view)
            elif event.button == 3:
                (click_x, click_y) = event.pos
                previous_view = current_view
                current_view = zoom(current_view, 1/ZOOM_FACTOR)
                new_center = pixel_to_complex(click_x, click_y, previous_view)
                current_view = recenter(current_view, new_center)
                draw_fractal(burning_ship_pixel_color, current_view)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                # b key pressed
                pass
        if event.type == pygame.QUIT:
            running = False
