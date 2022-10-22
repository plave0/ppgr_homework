
from collections import namedtuple

AffinePoint2D = namedtuple('AffinePoint2D', 'x y')
ProjectivePoint2D = namedtuple('ProjectivePoint2D', 'x1 x2 x3')
ProjectiveLine2D = namedtuple('ProjectiveLine2D', 'x1 x2 x3') 

def affine_to_projective_point(affine_point : AffinePoint2D) -> ProjectivePoint2D:
    return ProjectivePoint2D(affine_point.x, affine_point.y, 1)

def projective_to_affine_point(projective_point : ProjectivePoint2D) -> AffinePoint2D:
    if projective_point.x3 != 0:
        x = projective_point.x1 / projective_point.x3
        y = projective_point.x2 / projective_point.x3
        return AffinePoint2D(x,y)

def cross_product_3d(a : tuple, b : tuple) -> tuple:

    c1 = a[1] * b[2] - a[2] * b[1]
    c2 = a[2] * b[0] - a[0] * b[2]  
    c3 = a[0] * b[1] - a[1] * b[0]

    return (c1,c2,c3)

def join_projective_points(point1: ProjectivePoint2D, point2: ProjectivePoint2D) -> ProjectiveLine2D:
    line = cross_product_3d(point1, point2)
    return ProjectiveLine2D(*(line))

def meet_projective_lines(line1: ProjectiveLine2D, line2: ProjectiveLine2D) -> ProjectivePoint2D:
    point = cross_product_3d(line1, line2)
    return ProjectivePoint2D(*(point))
