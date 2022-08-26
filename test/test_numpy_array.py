from cgi import test
import numpy as np

test_arr = [i for i in range(240)]
arr2 = [j for j in range(240)]
arr_combi = list(zip(test_arr, arr2))
numpy_arr = np.array(arr_combi)
# print(arr_combi[0])
# print(numpy_arr.size)
# print(numpy_arr.shape)
# print(numpy_arr.ndim)
# print(numpy_arr.nbytes)

multid_arr = [ 
    [
        [1, 2], [3, 4], [5, 6]
    ], [
        [5, 6], [7, 8], [9, 10]
    ]
]

numpy_arr_1 = np.array(multid_arr)
# print(numpy_arr_1.shape)
# print(numpy_arr_1.ndim)
# print(numpy_arr_1.size)
# print(numpy_arr_1.dtype)
# print(numpy_arr_1.nbytes)
# print(numpy_arr_1)


# test_array = np.ndarray(shape=(1,), dtype=str)
# print(test_array)
# print(test_array.ndim)
# arr3d = np.ndarray(shape=(2,), dtype=str)
# print(arr3d)
# print(arr3d.ndim)

# arr2d = np.array([[1,2,1], [7,5,3], [9,4,8]])
# B = arr2d[[0], [0, 1,]]
# print(B)
# print(B.shape)
# print(arr2d.shape)

# site = np.ones((20, 200), dtype=int)
# sumkma = np.ones((100, 20), dtype=int)
# B = [sumkma[site[x], x] for x in range(20)]
# print(B)

x = np.arange(10)
print(x[1:9])