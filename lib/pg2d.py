
import numpy as np
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

def nevidljiva_tacka(
    p1:ProjectivePoint2D,
    p2:ProjectivePoint2D,
    p3:ProjectivePoint2D,
    p5:ProjectivePoint2D,
    p6:ProjectivePoint2D,
    p7:ProjectivePoint2D,
    p8:ProjectivePoint2D,
):

    xb_1 = meet_projective_lines(
        join_projective_points(p2, p6),
        join_projective_points(p1, p5)
    )
    xb_2 = meet_projective_lines(
        join_projective_points(p2, p6),
        join_projective_points(p3, p7)
    )
    xb_3 = meet_projective_lines(
        join_projective_points(p3, p7),
        join_projective_points(p1, p5)
    )

    xb = ProjectivePoint2D(*(
        map(lambda i, j, k: i + j + k, xb_1, xb_2, xb_3)
    ))
    xb = ProjectivePoint2D(*(
        map(lambda x: x/3, xb)
    ))

    yb_1 = meet_projective_lines(
        join_projective_points(p7, p8), 
        join_projective_points(p6, p5)
    )
    yb_2 = meet_projective_lines(
        join_projective_points(p7, p8),
        join_projective_points(p1, p2)
    )
    yb_3 = meet_projective_lines(
        join_projective_points(p5, p6),
        join_projective_points(p1, p2)
    )

    yb = ProjectivePoint2D(*(
        map(lambda i, j, k: i + j + k, yb_1, yb_2, yb_3)
    ))
    yb = ProjectivePoint2D(*(
        map(lambda x : x/3, yb)
    ))

    p4 = meet_projective_lines(
        join_projective_points(yb, p3),
        join_projective_points(xb, p8)
    )

    return p4

def nevidljiva_tacka_2(
    p1:ProjectivePoint2D,
    p2:ProjectivePoint2D,
    p3:ProjectivePoint2D,
    p5:ProjectivePoint2D,
    p6:ProjectivePoint2D,
    p7:ProjectivePoint2D,
    p8:ProjectivePoint2D,
):

    p4 = nevidljiva_tacka(p1, p2, p3, p5, p6, p7, p8)
    return np.array(p4)