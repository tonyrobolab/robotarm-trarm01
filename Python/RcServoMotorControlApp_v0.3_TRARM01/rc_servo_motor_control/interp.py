# --------------------------------------------------------------------------------
#   File        interp.py
#
#   Version     v0.1  2025.11.14  Tony Kwon
#                   Initial revision
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
#   Import
# --------------------------------------------------------------------------------
import copy

# --------------------------------------------------------------------------------
#   Class - Interp
# --------------------------------------------------------------------------------
class Interp:

    def get_interp_lists(self, arrs, step):
        arr_list = []
        arr_list.append(arrs[0])     
        for i in range(len(arrs) - 1):
            arr_list.extend(self.get_interp_list(arrs[i], arrs[i + 1], step))
        return arr_list

    def get_interp_list(self, arr1, arr2, step):
        arr_list = []
        arr1 = copy.copy(arr1)
        arr2 = copy.copy(arr2)
        cnt = int(self.get_max_value(arr1, arr2) / step)
        for j in range(cnt):
            arr = []
            for i in range(len(arr1)):
                if arr1[i] < arr2[i]:
                    if arr1[i] < (arr2[i] + step):
                        arr.append(arr1[i] + step)
                    else:
                        arr.append(arr2[i])
                else:
                    if (arr1[i] - step) > arr2[i]:
                        arr.append(arr1[i] - step)
                    else:
                        arr.append(arr2[i])
                arr1[i] = arr[i]
            arr_list.append(arr)
        return arr_list

    def get_max_value(self, arr1, arr2):
        diffs = [abs(x - y) for x, y in zip(arr1, arr2)]
        return max(diffs)
