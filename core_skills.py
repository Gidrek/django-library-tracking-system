import random
rand_list = [random.randint(1, 20) for _ in range(0, 10)]

list_comprehension_below_10 = [x for x in rand_list if x < 10]

print(list_comprehension_below_10)

list_comprehension_below_10 = filter(lambda x: x < 10, rand_list)

print(list(list_comprehension_below_10))
