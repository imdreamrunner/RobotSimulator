def get_coverage(grids, width, height):
    explored_count = 0.0
    for w in range(width):
        for h in range(height):
            if grids[w][h] > 0:
                explored_count += 1
    return explored_count / (width * height)


def get_hex_map(grids, width, height):
    expl = 0b11
    obst = 0xF
    # for w in range(WIDTH-1, -1, -1):
    for w in range(width):
        for h in range(height):
            print grids[width - w - 1][h],
            # print knownWorld[w][h],
            expl <<= 1
            if grids[w][h] > 0:
                expl |= 0b1
                obst <<= 1
                if grids[w][h] == 2:
                    obst |= 0b1
        print
    print
    expl <<= 2
    expl |= 0b11

    if obst.bit_length() % 4 != 0:
        obst <<= 4 - obst.bit_length() % 4
    obst_string = format(obst, "X")[1:]

    return format(expl, "X"), obst_string