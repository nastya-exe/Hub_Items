import random

lst = random.sample(range(0, 1000000), 10)

evens = []
odds = []

for num in lst:
    if num % 2 == 0:
        evens.append(num)
    else:
        odds.append(num)

evens.sort()
odds.sort()

sorted_lst = evens[::-1] + odds

print(sorted_lst)
