# lists are mutable

list_a = [1, "one", 44, "yes", 33.3]

# command: list_a
# output: [1, "one", 44, "yes", 33.3]

# command: list_a[3]
# output: "yes"

# command: list_a[3] = "no"
# command: list_a
# output: [1, "one", 44, "no", 33.3]

# command: list_a.remove("one")
# command: list_a
# output: [1, 44, "no", 33.3]

# command: list_a.insert(3, "3isThePosition")
# command: list_a
# output: [1, 44, "no", '3isThePosition', 33.3]

# command: list_a.append("today")
# command: list_a
# output: [1, 44, "no", '3isThePosition', 33.3, "today"]

# command: list_a.insert(2, [1.2, 3, 1, "koala"])
# command: list_a
# output: [1, 44, [1.2, 3, 1, 'koala'], "no", '3isThePosition', 33.3, "today"]
