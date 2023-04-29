import numpy as np

# utworzenie macierzy 3x3
matrix = np.array([[1, 0, -2],
                   [-3, 4, 0],
                   [5, 6, -1]])

# wyznaczenie indeksów elementów większych lub równych 0
idx = np.where(matrix >= 0)

x = matrix[matrix >=0]
# wyznaczenie liczby elementów większych lub równych 0
num_nonnegative = np.size(idx)

# wyświetlenie liczby
print(len(x))
