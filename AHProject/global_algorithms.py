import random
from user import User

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


def test_bubble_sort(sort_by, order="desc"):

    names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    random.shuffle(names)
    scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(scores)

    array = [User(username=names[i], score=scores[i]) for i in range(10)]
    print(f"Initial Array: {array}")

    bubble_sort(array, sort_by=sort_by, order=order)
    print(f"Using .bubble_sort(): {array}")


def binary_search(array, target):
    high = len(array)
    low = 0

    while high != low:
        middle = int((high + low) / 2)

        if array[middle].username < target:
            low = middle + 1

        elif array[middle].username > target:
            high = middle - 1

        else:
            return middle

    return None

def test_binary_search(value_in_array=True):
    names = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    random.shuffle(names)
    scores = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    random.shuffle(scores)

    array = [User(username=names[i], score=scores[i]) for i in range(10)]
    bubble_sort(array, "username")

    if value_in_array:
        target = names[random.randint(0, 10)]
        print(array[binary_search(array, target)])

    else:
        target = random.sample(names, 2)
        target = target[0] + target[1]
        print(binary_search(array, target))

