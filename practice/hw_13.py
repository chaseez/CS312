random_list = [5,15,-30,10,-5,40,10]

prev_indexes = {}
total_indexes = {}
prev = None
prev_index = None
total = 0
max = None
max_index = None
first = True

for i in range(len(random_list)):
    if total == 0 and prev is None:
        prev = random_list[i]
        prev_index = i
        first = True
        continue

    curr = random_list[i]

    if prev + curr > prev or first:
        first = False

        total = prev + curr
        prev_indexes[i] = prev_index
        total_indexes[i] = total

        prev = total
        prev_index = i
        if max is None or total > max:
            max = total
            max_index = i
    else:
        total = 0
        prev = None
        prev_index = None


subsequent_list = []
curr_index = max_index
while True:
    subsequent_list.append(random_list[curr_index])
    if curr_index in prev_indexes:
        curr_index = prev_indexes[curr_index]
    else:
        break


subsequent_list.reverse()
print(subsequent_list, max)