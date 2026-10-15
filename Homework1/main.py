import pathlib
import math

def load_system(path: pathlib.Path):
    A = []
    B = []
    with path.open("r") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            left, right = line.split("=")
            B.append(float(right.strip()))


            # print(left)
            left = left.replace(" ", "")
            # print(left)
            left = left.replace("+", " +").replace("-", " -")
            # print(left)
            left = left.split(' ')


            row = [0.0, 0.0, 0.0]
            for val in left:
                if not val:
                    continue
                if 'x' in val:
                    val = val.replace('x', '')
                    row[0] = 1.0 if val in ('', '+') else (-1.0 if val == '-' else float(val))
                elif 'y' in val:
                    val = val.replace('y', '')
                    row[1] = 1.0 if val in ('', '+') else (-1.0 if val == '-' else float(val))
                elif 'z' in val:
                    val = val.replace('z', '')
                    row[2] = 1.0 if val in ('', '+') else (-1.0 if val == '-' else float(val))

            A.append(row)
    return A, B

def determinant(matrix: list[list[float]]) -> float:
    return matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])

def trace(matrix: list[list[float]]) -> float:
    return matrix[0][0] + matrix[1][1] + matrix[2][2]

def norm(vector: list[float]) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

def transpose(matrix: list[list[float]]) -> list[list[float]]:
    T = []
    for j in range(len(matrix)):
        row = []

        for i in range(len(matrix)):
            row.append(matrix[i][j])
        T.append(row)
    return T

def multiply(matrix: list[list[float]], vector: list[float]) -> list[float]:
    list = []
    for row in matrix:
        sum = row[0] * vector[0] + row[1] * vector[1] + row[2] * vector[2]
        list.append(sum)
    return list

def solve_cramer(matrix: list[list[float]], vector: list[float]) -> list[float]:
    lista = []
    det = determinant(matrix)
    if det == 0:
        raise ValueError("Det e 0 nu se poate")

    Ax = [row[:] for row in matrix]
    for i in range(len(matrix)):
        Ax[i][0] = vector[i]
    lista.append(determinant(Ax)/det)

    Bx = [row[:] for row in matrix]

    for i in range(len(matrix)):
        Bx[i][1] = vector[i]
    lista.append(determinant(Bx)/det)
    Cx = [row[:] for row in matrix]

    for i in range(len(matrix)):
        Cx[i][2] = vector[i]
    lista.append(determinant(Cx)/det)

    return lista

def minor(matrix: list[list[float]], i: int, j: int) -> list[list[float]]:
    rows = [r for r in range(len(matrix)) if r!= i]
    cols = [c for c in range(len(matrix)) if c!= j]
    return [
        [matrix[rows[0]][cols[0]], matrix[rows[0]][cols[1]]],
        [matrix[rows[1]][cols[0]], matrix[rows[1]][cols[1]]]
    ]

def cofactor(matrix: list[list[float]]) -> list[list[float]]:
    copie =     [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            a = minor(matrix, i, j)
            det_a = a[0][0] * a[1][1] - a[0][1] * a[1][0]
            copie[i][j] = (-1) ** (i + j) * det_a
    return copie

def adjoint(matrix: list[list[float]]) -> list[list[float]]:
    return transpose(cofactor(matrix))

def solve(matrix: list[list[float]], vector: list[float]) -> list[float]:
    det = determinant(matrix)
    inversa = [[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]]
    if det == 0:
        raise ValueError("Det e 0 nu se poate")

    adj = adjoint(matrix)

    for i in range(len(adj)):
        for j in range(len(adj)):
            inversa[i][j] = adj[i][j] / det




    return multiply(inversa, vector)












A, B = load_system(pathlib.Path("system.txt"))
print(f"{A=} {B=}")
print(f"{determinant(A)=}")
print(f"{trace(A)=}")
print(f"{norm(B)=}")
print(f"{transpose(A)=}")
print(f"{multiply(A, B)=}")
print(f"{solve_cramer(A, B)=}")
print(f"{solve(A, B)=}")