def rectifyZeroVector(vector):
    for i in range(len(vector)):
        if not vector[i] == 0:
            break
        if i == len(vector) - 1:
            vector[i] = -1
    return vector

