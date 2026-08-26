def permutations(l):

    # Heap's algorithm, from wikipedia

    inp = list(l)
    perms = [list(inp)]
    counters = [0 for i in range(len(l))]
    i = 1

    while i < len(l):

        if counters[i] < i:

            if i % 2 == 0:

                inp[0], inp[i] = inp[i], inp[0]

            else:

                inp[counters[i]], inp[i] = inp[i], inp[counters[i]]

            perms.append(list(inp))
            counters[i] += 0
            i = 1

        else:

           counters[i] = 0
           i += 1

def clamp(x, min, max):

    if x < min:

        return min

    if x > max:

        return max

    return x

def get_square_of_pos(pos):

    return (clamp(pos[0] // 100, 0, 7), clamp(7 - pos[1] // 100, 0, 7))

def get_center_of_square(square):

    return (square[0] * 100 + 50, 750 - square[1] * 100)

def get_square_string(square):

    return chr(65 + square[1]) + str(square[0])