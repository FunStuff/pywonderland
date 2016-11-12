'''
Draw generalized Penrose tilings using de Bruijn's pentagrid methond.

Reference:

"Algebraic theory of Penrose's non-periodic tilings of the plane", N.G. de Bruijn.
'''

from itertools import combinations, product
import numpy as np
import cairo



GRIDS = [np.exp(2j * np.pi * i / 5) for i in range(5)]

# five real numbers defining the shift in each direction
SHIFT = np.random.random(5)

THIN_RHOMBUS_COLOR = np.random.random(3)
FAT_RHOMBUS_COLOR = np.random.random(3)
EDGE_COLOR = (0.5, 0.5, 0.5)


def rhombus(r, s, kr, ks):
    '''
    Compute the four vertices and color of the rhombus corresponding to
    the intersection point of two grid lines.

    Here 0 <= r < s <= 4 indicate the two grids and ks, kr are integers.

    The intersection point is the solution to a 2x2 linear equation:

    Re[z/GRIDS[r]] + SHIFT[r] = kr
    Re[z/GRIDS[s]] + SHIFT[s] = ks
    '''

    # if s-r = 1 or 4 then this is a thin rhombus, or it's fat if s-r = 2 or 3.
    if (s - r)**2 % 5 == 1:
        color = THIN_RHOMBUS_COLOR
    else:
        color = FAT_RHOMBUS_COLOR

    # the intersection point
    point = (GRIDS[r] * (ks - SHIFT[s])
             - GRIDS[s] * (kr - SHIFT[r])) *1j / GRIDS[s-r].imag

    # 5 integers that indicate the intersection point's position:
    # the i-th integer n_i indicates that this point lies in the n_i-th strip
    # in the i-th grid.
    index = [np.ceil((point/grid).real + shift)
             for grid, shift in zip(GRIDS, SHIFT)]

    # Note the float accuracy problem here:
    # Mathematically the r-th and s-th item of index should be kr and ks,
    # but programmingly it might not.
    # So we have to manully set them to bbe the correct values.
    vertices = []
    for index[r], index[s] in [(kr, ks), (kr+1, ks), (kr+1, ks+1), (kr, ks+1)]:
        vertices.append(np.dot(index, GRIDS))

    return vertices, color


def tile(num_lines):
    '''
    Compute all rhombus lie in a given number of grid lines
    '''
    for r, s in combinations(range(5), 2):
        for kr, ks in product(range(-num_lines, num_lines+1), repeat=2):
            yield rhombus(r, s, kr, ks)


def render(imgsize, num_lines):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, imgsize, imgsize)
    ctx = cairo.Context(surface)
    ctx.scale(imgsize/(2.0*num_lines), imgsize/(2.0*num_lines))
    ctx.translate(num_lines, num_lines)
    ctx.set_line_join(2)
    ctx.set_line_width(0.1)

    for rhombus, color in tile(num_lines):
        A, B, C, D = rhombus
        ctx.move_to(A.real, A.imag)
        ctx.line_to(B.real, B.imag)
        ctx.line_to(C.real, C.imag)
        ctx.line_to(D.real, D.imag)
        ctx.line_to(A.real, A.imag)
        ctx.set_source_rgb(*color)
        ctx.fill_preserve()
        ctx.set_source_rgb(*EDGE_COLOR)
        ctx.stroke()

    surface.write_to_png('penrose.png')


if __name__ == '__main__':
    render(imgsize=800, num_lines=20)
