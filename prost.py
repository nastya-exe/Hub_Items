lst = [4, 2, 7, 5, 11, 9, 8, 12,3, 4, 1]
for i  in range(len(lst)):
    n = i % 3 + 1
    lst[i] = lst[i] ** n
print(lst[7])