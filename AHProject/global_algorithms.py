def bubble_sort(unsorted_array, sort_by="username"):
    if sort_by == "username":
        def sort_condition(): return unsorted_array[j].username > unsorted_array[j + 1].username

    elif sort_by == "score":
        def sort_condition(): return unsorted_array[j].score > unsorted_array[j + 1].score

    ARRAY_LENGTH = len(unsorted_array)
    SWAPPED = False

    for i in range(ARRAY_LENGTH - 1):
        for j in range(0, ARRAY_LENGTH - i - 1):

            if sort_condition():
                SWAPPED = True
                unsorted_array[j], unsorted_array[j + 1] = unsorted_array[j + 1], unsorted_array[j]
        if not SWAPPED:
            return

def binary_search(array, target):
    high = len(array) - 1
    low = 0

    while high >= low:

        middle = int((high + low) / 2)

        if array[middle].username < target:
            low = middle + 1

        elif array[middle].username > target:
            high = middle - 1

        else:
            return middle

    return None
