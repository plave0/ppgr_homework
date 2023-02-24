import numpy as np


def Euler2A(fi, teta, psi):
    Rx = np.array([[1, 0, 0],[0, np.cos(fi), -np.sin(fi)],[0, np.sin(fi), np.cos(fi)]])
    Ry = np.array([[np.cos(teta), 0, np.sin(teta)],[0, 1, 0],[-np.sin(teta), 0, np.cos(teta)]])
    Rz = np.array([[np.cos(psi), -np.sin(psi), 0], [np.sin(psi), np.cos(psi), 0], [0, 0, 1]])

    return Rz @ Ry @ Rx 


def AxisAngle(A):
    
    if abs(np.linalg.det(A) - 1) > 1e-6:
        print("Matrica nije u ispravnom obliku")
        return

    A2 = A - np.eye(A.shape[0])

    p = np.cross(A2[0], A2[1])
    
    pn = p / np.linalg.norm(p)

    u = A2[0]
    up = A @ u

    fi = np.arccos(np.dot(u, up) / (np.linalg.norm(u) * np.linalg.norm(up)))

    orijentacija = np.linalg.det(np.array([u, up, pn]))
    
    if orijentacija > 0:
        return pn, fi
    else:
        return pn, (2 * np.pi) - fi


def Rodrigez(p, fi):
    px = np.array([[0, -p[0][2], p[0][1]], [p[0][2], 0, -p[0][0]], [-p[0][1], p[0][0], 0]])
    A = (p.T @ p) + np.cos(fi) * (np.eye(3) - (p.T @ p)) + np.sin(fi) * px
    return A


def A2Euler(A):
    if A[2][0] > -1 and A[2][0] < 1:
        fi = np.arctan2(A[2][1], A[2][2])
        teta = np.arcsin(-A[2][0])
        psi = np.arctan2(A[1][0], A[0][0])
    elif A[2][0] == -1:
        fi = 0
        teta = np.pi / 2
        psi = np.arctan2(-A[0][1], A[1][1])
    elif A[2][0] == 1:
        fi = 0
        teta = -np.pi / 2
        psi = np.arctan2(-A[0][1], A[1][1])

    return fi, teta, psi