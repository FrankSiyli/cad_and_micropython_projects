# tuples are immutable


test = (1, 2, 5)
# command: test
# output: (1,2,5)

# command: test[1]
# output: 2


def get_data():
    pos_x = 10
    pos_y = 20
    pos_z = 30
    return (pos_x, pos_y, pos_z)


x, y, z = get_data()

# command: x
# output: 10

# command: y
# output: 20

# command: z
# output: 30
