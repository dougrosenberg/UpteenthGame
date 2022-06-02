def get_cycles(permutation):
    #print('get cycles',permutation)
    numbers_left = permutation[:]
    disjoint_cycles = []
    while numbers_left:
        start_cycle = permutation.index(numbers_left[0]) + 1
        # print('*******',start_cycle)
        numbers_left.remove(start_cycle)
        new_cycle = [start_cycle]
        last_member = start_cycle
        while True:
            # print('*******',new_cycle)
            next_member = permutation[last_member - 1]
            if next_member == start_cycle:
                break
            else:
                new_cycle.append(next_member)
                numbers_left.remove(next_member)
                last_member = next_member
        disjoint_cycles.append(tuple(new_cycle))

    return disjoint_cycles


def get_parity(permutation):
    num_disjoint = 0
    cycles = get_cycles(permutation)
    #print(permutation)
    #print(cycles)
    for cycle in cycles:
        if len(cycle) == 1:
            pass
        else:
            num_disjoint += len(cycle) + 1
    parity =  num_disjoint % 2
    #print('parity=',parity)
    return parity


def main():
    permute_1 = [4,1,3,2]
    print(get_parity(permute_1))


if  __name__ == '__main__':
    main()

