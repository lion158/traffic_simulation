import numpy as np
import pandas as pd


class Matrix:
    operaction_counter = 0

    def matrix_inverse_recursive(self, A):
        n = A.shape[0]
        if n == 1:
            return np.array([[1 / A[0, 0]]])
        else:
            A11 = A[:n // 2, :n // 2]
            A12 = A[:n // 2, n // 2:]
            A21 = A[n // 2:, :n // 2]
            A22 = A[n // 2:, n // 2:]

            A11_inv = self.matrix_inverse_recursive(A11)
            S22 = A22 - self.recurMatrixMultiplication(self.recurMatrixMultiplication(A21, A11_inv), A12)
            S22_inv = self.matrix_inverse_recursive(S22)
            B11 = A11_inv + self.recurMatrixMultiplication(self.recurMatrixMultiplication(
                self.recurMatrixMultiplication(self.recurMatrixMultiplication(A11_inv, A12), S22_inv), A21),
                A11_inv)  ##
            B12 = -np.dot(self.recurMatrixMultiplication(A11_inv, A12), S22_inv)
            B21 = -np.dot(self.recurMatrixMultiplication(S22_inv, A21), A11_inv)
            B22 = S22_inv

            B_top = np.concatenate((B11, B12), axis=1)
            B_bottom = np.concatenate((B21, B22), axis=1)
            B = np.concatenate((B_top, B_bottom), axis=0)
            return B

    def recurMatrixMultiplication(self, first, second):
        size = len(first)
        m = [[0 for j in range(size)] for i in range(size)]
        for i in range(size):  # rows in multiply
            for j in range(size):  # columns in multiply
                sum = 0
                for k in range(size):  # columns in first and rows in second
                    sum += first[i][k] * second[k][j]
                    self.operaction_counter += 1
                m[i][j] = sum
        return np.array(m)

    def recursive_lu(self, A):
        n = len(A)
        L = np.zeros((n, n))
        U = np.zeros((n, n))

        if n == 1:
            L[0, 0] = 1
            U[0, 0] = A[0, 0]
        else:
            m = n // 2
            L11, U11 = self.recursive_lu(A[:m, :m])
            L21 = self.recurMatrixMultiplication(A[m:, :m], self.matrix_inverse_recursive(U11))
            U12 = self.recurMatrixMultiplication(A[:m, m:], self.matrix_inverse_recursive(L11))
            L22, U22 = self.recursive_lu(A[m:, m:] - self.recurMatrixMultiplication(L21, U12))

            L[:m, :m] = L11
            L[m:, :m] = L21
            L[m:, m:] = L22

            U[:m, :m] = U11
            U[:m, m:] = U12
            U[m:, m:] = U22

        return L, U





# Definicja macierzy A o wymiarach 4x4
A = np.array([[1, 2, 3, 4],
              [5, 6, 7, 8],
              [9, 10, 11, 12],
              [13, 14, 15, 16]])

# A = np.array([[1,2],[4,5]])
# Wywołanie algorytmu rekurencyjnej faktoryzacji LU
matrix = Matrix()
L, U = matrix.recursive_lu(A)

# Wyświetlenie wyników
print("Macierz A:\n", A)
print("Macierz L:\n", L)
print("Macierz U:\n", U)