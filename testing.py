# import numpy as np
#
# my_list = [-50, -2, -210, 1, -2, -2, -10, -2, -1, -2, -2, -2, -2]
# start_index = 3
#
# # Tworzymy tablicę NumPy z listy
# my_array = np.array(my_list)
# my_array = np.roll(my_array, -start_index) # roll to start_index as first
#
# print(my_array)
#
# # Utworzenie maski wartości dodatnich i ujemnych
# positive_mask = my_array >= 0
# negative_mask = my_array < 0
#
# # Znajdujemy indeks pierwszej wartości dodatniej od start_index
# positive_index = (positive_mask[0 + 1:] == True).argmax()
#
#
# # Obliczamy ilość wartości ujemnych między wartościami dodatnimi
# count = np.count_nonzero(negative_mask[positive_index:0:-1])
# print(count)
#
#

my_list = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
print(my_list[1][:])
