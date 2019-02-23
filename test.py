a1 = {"a":14.2, "c":11.3, "d":9.1, "e":13.9, "f":19.9, "g":13.2, "b":14.2}
print(min(a1, key=a1.get))
# li = []
#
# for each in a1:
#
#     if len(li) == 3:
#         if a1[each] > min(li):
#             li.remove(min(li))
#             li.append(a1[each])
#             print(min(li))
#             print(max(li))
#     else:
#         li.append(a1[each])
#         print(a1[each])
#         print(len(li))
#
# print(li)


di = {}

for each in a1:

    if len(di) == 3:
        if a1[each] > di[min(di, key=di.get)]:
            del di[min(di, key=di.get)]
            di[each] = a1[each]
    else:
        di[each] = a1[each]

print(di)