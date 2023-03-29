import numpy as np


def matrix_inverse_recursive(A):
    n = A.shape[0]
    if n == 1:
        return np.array([[1 / A[0, 0]]])
    else:
        A11 = A[:n // 2, :n // 2]
        A12 = A[:n // 2, n // 2:]
        A21 = A[n // 2:, :n // 2]
        A22 = A[n // 2:, n // 2:]

        A11_inv = matrix_inverse_recursive(A11)
        S22 = A22 - np.dot(np.dot(A21, A11_inv), A12)
        S22_inv = matrix_inverse_recursive(S22)
        B11 = A11_inv + np.dot(np.dot(np.dot(np.dot(A11_inv, A12), S22_inv), A21), A11_inv)##
        B12 = -np.dot(np.dot(A11_inv, A12), S22_inv)
        B21 = -np.dot(np.dot(S22_inv, A21), A11_inv)
        B22 = S22_inv

        B_top = np.concatenate((B11, B12), axis=1)
        B_bottom = np.concatenate((B21, B22), axis=1)
        B = np.concatenate((B_top, B_bottom), axis=0)
        return B

arr = np.array([[1, 2], [3, 4]])
x = matrix_inverse_recursive(np.array([[1, 2], [3, 4]]))
y = matrix_inverse_recursive(np.array([[2, 1, 0, 1],
              [3, 2, 1, 0],
              [1, 0, 2, 1],
              [0, 3, 1, 2]]))
print(x)
print(y)


import numpy as np

A = np.array([[2, 1, 0, 1],
              [3, 2, 1, 0],
              [1, 0, 2, 1],
              [0, 3, 1, 2]])

A_inv = matrix_inverse_recursive(A)
print(A_inv)

# Sprawdzenie czy A * A_inv = I
I = np.dot(A, A_inv)
print(I)