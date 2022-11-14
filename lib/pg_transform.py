import numpy as np

# Naivni algoritam
# Ulaz : Osam tačaka u homohenim koordinatama
# Izlaz : Matrica projektivne transofrmacije.
#   Dobijena matrica slika prve četri tačke u druge četri tačke na ulazu.
def naive(a, b, c, d,
          ap, bp, cp, dp):
    
    A = np.column_stack((a, b, c))
    x = np.linalg.solve(A, d)

    g = np.column_stack((x[0] * a, x[1] * b, x[2] * c))

    A = np.column_stack((ap, bp, cp))
    x = np.linalg.solve(A, dp)

    h = np.column_stack((x[0] * ap, x[1] * bp, x[2] * cp))

    return h @ np.linalg.inv(g)

# DLT algoitam
# Ulaz : Dva niza tačaka u homogenim koordinatama
# Izlaz : Matrica projektivne transformacije
#   Dobijena matrica slika tačke iz prvog niza u tačke iz drugog niza.
def dlt(points1, points2):

    A = None
    for (x, xp) in zip(points1, points2):
        a = np.array([[0, 0, 0, -xp[2] * x[0], -xp[2] * x[1], -xp[2] * x[2], xp[1] * x[0], xp[1] * x[1], xp[1] * x[2]],
                      [xp[2] * x[0], xp[2] * x[1], xp[2] * x[2], 0, 0, 0, -xp[0] * x[0], -xp[0] * x[1], -xp[0] * x[2]]])
        
        if A is None:
            A = a
        else:
            A = np.vstack((A, a))

    
    _, _, vt = np.linalg.svd(A)
    #vt = np.transpose(v)

    P = np.reshape(vt[-1], (3, 3))

    return P

# Normalizacija niza tačaka
# Ulza : Niz tačaka
# Izlaz : Niz tačaka u normalizovanim koordinatama i matrica normalizacije.
def normalize(points):

    points = list(map(
        lambda x : np.array([x[0] / x[2], x[1] / x[2], 1]),
        points
    ))
    
    B = sum(points) / len(points)
    G = np.array([[1, 0, -B[0]],
                  [0, 1, -B[1]],
                  [0, 0, 1]])
    
    points = list(map(
        lambda x : G @ x,
        points
    ))

    ro = sum( map(lambda x : np.linalg.norm(x), points) )  / len(points)

    S = np.array([[np.sqrt(2)/ro, 0, 0],
                  [0, np.sqrt(2)/ro, 0],
                  [0, 0, 1]])

    
    points = list(map(
        lambda x : S @ x,
        points
    ))

    return points, S @ G

# Unapređeni DLT algoitam
# Ulaz : Dva niza tačaka u homogenim koordinatama
# Izlaz : Matrica projektivne transformacije
#   Dobijena matrica slika tačke iz prvog niza u tačke iz drugog niza.
def dlt2(points1, points2):
    
    points1, T1 = normalize(points1)
    points2, T2 = normalize(points2)

    P = dlt(points1, points2)

    return np.linalg.inv(T2) @ P @ T1