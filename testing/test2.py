import numpy as np


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
                    sum += self.multiply(first[i][k], second[k][j])
                m[i][j] = sum
        return np.array(m)

    # def multiply(self, a, b):
    #     if a == 1:
    #         return b
    #     if b < 0:
    #         return -self.multiply(a, -b)
    #     elif b == 1:
    #         return a
    #     else:
    #         b -= 1
    #         # global operation_counter
    #         # operation_counter += 2
    #         return a + self.multiply(a, b)




matrix = Matrix()

arr = np.array([[1, 2], [3, 4]])
arr2 = np.array([[2, 1, 0, 1],
                 [3, 2, 1, 0],
                 [1, 0, 2, 1],
                 [0, 3, 1, 2]])
#matrix.matrix_inverse_recursive(arr)
#print(matrix.matrix_inverse_recursive(arr2))
# res = matrix.matrix_inverse_recursive(arr)
# print(res)


def multiply(a, b):
    if b == 0:
        return 0
    elif b > 0:
        return a + multiply(a, b-1)
    else:
        return -multiply(a, -b)





# print(multiply(np.array([2]),np.array([-0.5])))
print(multiply(2,-2))