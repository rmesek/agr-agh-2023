edges1 = [True, True, False]  # 1
edges2 = [False, False, False]  # -1
edges3 = [True, True]  # 1
edges4 = [True, False, False, False]  # 0
edges5 = [True, True, False, False]  # 1
edges6 = [True, True, True, False]  # 2
lists = [edges1, edges2, edges3, edges4, edges5, edges6]
for edges in lists:
    for i in range(len(edges)):
        edges[i] = (edges[i], i)


def simple_search(edges):
    result = -1
    for edge, i in edges[::-1]:
        # print(i)
        if edge:
            result = i
            break
    return result


def binary_search(edges):
    result = -1
    low, high = 0, len(edges) - 1
    while low <= high:
        mid = (low + high) // 2
        if edges[mid][0]:
            result = mid
            low = mid + 1
        else:
            high = mid - 1
    return result


for edges in lists:
    binary_search_res = binary_search(edges)
    simple_search_res = simple_search(edges)
    print(f"{binary_search_res=} {simple_search_res=}")
    assert binary_search_res == simple_search_res

# print(simple_search(edges1), simple_search(edges1), simple_search(edges1))
