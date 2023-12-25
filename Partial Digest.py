L = [2, 2, 3, 3, 4, 5, 6, 7, 8, 10]
width = max(L)
X = [0]

def delta(y, X):
    diffs = []
    for x in X:
        diffs.append(abs(y-x))
    return diffs

def backtrack(L, X):
    if len(L)==0:
        X.sort()
        print(X)
        return
    y = max(L)
    delta_y = delta(y, X)
    is_subset = all(item in L for item in delta_y)
    if is_subset:
        for x in delta_y:
            L.remove(x)
        X.append(y)
        backtrack(L,X)
        for x in delta_y:
            L.append(x)
        X.remove(y)
    else:
        y = width - y
        delta_y = delta(y, X)
        for x in delta_y:
            L.remove(x)
        X.append(y)
        backtrack(L,X)
        for x in delta_y:
            L.append(x)
        X.remove(y)
    return

backtrack(L,X)
