# count 0 - 10
for i in range(0, 11):
    print(i)

# add a step
for i in range(0, 20, 2):
    print(i)

# backwards
for i in range(20, 0, -1):
    print(i)

# without "range" it prints all entries no matter which type of data
for i in ("hello", 0, -1, 50, 100, 45, "bye"):
    print(i)
