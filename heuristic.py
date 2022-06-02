import heapq
import math
from collections import namedtuple
from dataclasses import dataclass, field
from heapq import heappop
import helper
DEBUG = False


def Debug(mess, arg1, arg2=None):
    if DEBUG:
        if arg2 is None:
            print(f"****** Debug: {mess}= {arg1}")
        else:
            print(f"****** Debug: {mess}= {arg1},{arg2}")


@dataclass
class Tree:
    node: tuple
    parent: 'Tree'
    left_child: 'Tree' = None
    right_child: 'Tree' = None
    up_child: 'Tree' = None
    down_child: 'Tree' = None


@dataclass(order=True, frozen=True)
class Priority_Item:
    priority: int
    tree: Tree = field(compare=False)


class consts:
    DirVector = namedtuple('DirVector', 'dir,x,y')
    LEFT_DIR = DirVector('L', -1, 0)
    RIGHT_DIR = DirVector('R', 1, 0)
    UP_DIR = DirVector('U', 0, -1)
    DOWN_DIR = DirVector('D', 0, 1)
    DIR_VECTORS = (LEFT_DIR, RIGHT_DIR, UP_DIR, DOWN_DIR)


class Heuristic:
    STAR = 0
    # import numpy as np

    def __init__(self, root_tuple: tuple[int], size: int):
        self.num_expanded = 0

        self.size = size
        self.visited = {}
        self.root_tuple = root_tuple
        #print('root_tuple=,',root_tuple)
        self.final_solution = Heuristic.reset(self.size)
        print('root tuple=',root_tuple)
        #print('self.final_solution =',self.final_solution )
        self.heap: list[Priority_Item] = []
        # create a vector (ndarray) of tiles and the layout of tiles positions (a graph)
        # tiles are numbered 1-15, the last tile is 0 (an empty space)
        if not self.is_solvable():
            print("**************Not solvable*****************")
            raise  ValueError
    @staticmethod
    def swap(node_list: tuple[int], p1: int, p2: int) -> None:
        node_list[p1], node_list[p2] = node_list[p2], node_list[p1]

    def get_index(self, row: int, col: int) -> int:
        return row * self.size + col

    def get_row_col(self, index_tile: int) -> (int, int):
        row = index_tile // self.size
        col = index_tile % self.size
        return row, col

    # verify if the puzzle is solved
    def is_solved(self, node: tuple[int]) -> bool:
        is_solved = (node == self.final_solution)

        Debug('is_solved=', is_solved)

        return is_solved

    def move_chain(self, leaf_tree: Tree) -> list[str]:
        list_moves = []
        tree = leaf_tree
        while tree is not None:
            move_str = self.visited[tree.node]
            list_moves.append(move_str)
            tree = tree.parent
        list_moves.reverse()
        list_moves.pop(0)
        print(f'Solution length ={len(list_moves)}')
        return list_moves

    def expand_node(self, node: tuple[int]) -> list[tuple]:
        new_node_list = []
        for dir_vect in consts.DIR_VECTORS:
            new_node = self.expand_node_dir(node, dir_vect)
            new_node_list.append(new_node)
        return new_node_list

    def solve_using_heuristics(self) -> list[str]:
        solved = False
        #print('is solved =',self.is_solved(self.root_tuple))
        if self.is_solved(self.root_tuple):
            return []
        root_tree = Tree(self.root_tuple,None)
        priority = self.get_priority(root_tree.node)
        priority_root_heap_item = Priority_Item(priority, root_tree)
        heapq.heappush(self.heap, priority_root_heap_item)
        self.visited[root_tree.node] = ''

        while not solved and self.heap:

            priority_heap_item = heappop(self.heap)
            #print('popped priority_heap_item=',priority_heap_item)
            parent_tree = priority_heap_item.tree
            child_nodes = self.expand_node(parent_tree.node)
            for dir_tuple, child_node in zip(consts.DIR_VECTORS, child_nodes):
                if child_node is None:
                    continue
                child_node = tuple(child_node)
                if child_node in self.visited:
                    continue
                self.num_expanded += 1
                if self.num_expanded % 100_000 == 0:
                    print("Nodes Expanded =", self.num_expanded)
                priority = self.get_priority(child_node)
                child_tree = Tree(child_node, parent_tree)
                child_priority_item = Priority_Item(priority, child_tree)
                heapq.heappush(self.heap, child_priority_item)
                self.visited[child_node] = dir_tuple.dir
                if self.is_solved(child_node):
                    print("Total Nodes Expanded =", self.num_expanded)

                    return self.move_chain(child_tree)
                else:  # get insert child that results from expansion into the tree
                    Heuristic.insert_tree(child_tree, dir_tuple.dir)

    @staticmethod
    def insert_tree(new_child_tree: Tree, direction: str) -> None:
        parent_tree = new_child_tree.parent
        if direction == 'U':
            parent_tree.up_child = new_child_tree
        elif direction == 'D':
            parent_tree.down_child = new_child_tree
        elif direction == 'L':
            parent_tree.left_child = new_child_tree
        elif direction == 'R':
            parent_tree.right_child = new_child_tree
        else:
            # should never get here
            print('insert_tree: should never get here')
            raise ValueError

    def expand_node_dir(self, trial_node: tuple[int], dir_vector) -> tuple[int]:
        STAR = 0
        index_star = trial_node.index(STAR)
        row_star, col_star = self.get_row_col(index_star)
        col_left_move = col_star + dir_vector.x
        row_left_move = row_star + dir_vector.y
        #Debug('col_left_move', col_left_move)
        #Debug('row_left_move', row_left_move)
        list_node = list(trial_node)
        if (0 <= col_left_move < self.size) and (0 <= row_left_move < self.size):
            new_node = list(trial_node)
            index_left = self.get_index(row_left_move, col_left_move)
            Heuristic.swap(new_node, index_star, index_left)
        else:
            new_node = None
        #Debug('Left Move After: ', new_node)
        return new_node

    def expand_nodes(self, parent):
        expanded_nodes = []

        for dir_vect in consts.DIR_VECTORS:
            new_node = self.expand_node_dir(parent, dir_vect)
            expanded_nodes.append(new_node)
        return expanded_nodes

    def get_priority(self, node_tuple):
        return Heuristic.out_place(node_tuple) + self.get_Manhattan_distance(node_tuple)

    def get_Manhattan_distance(self, node):
        #print('node=',node)
        index_0 = node.index(0)
        row, col = self.get_row_col(index_0)
        row_distance = (self.size - 1) - row
        col_distance = (self.size - 1) - col
        m_distance = row_distance + col_distance
        Debug("get_Manhattan_distance", m_distance)
        return m_distance
    @staticmethod
    def out_place_original(node_tuple):
        count_out_place = 0
        for index in range(len(node_tuple) - 1):
            if node_tuple[index] != 0 and node_tuple[index] != (index + 1):
                count_out_place += 1
        Debug('out_place=', count_out_place)
        return count_out_place
    @staticmethod
    def out_place(node_tuple):
        count_out_place = 0
        extra = len(node_tuple)
        for index in range(len(node_tuple) - 1):
            if node_tuple[index] != 0 and node_tuple[index] != (index + 1):
                count_out_place += math.ceil(math.log(extra))*2
                extra += -1
        Debug('out_place=', count_out_place)
        return count_out_place


    def get_parity_puzzle(self,puzzle):
        copy_tiles = list(puzzle)
        # change 0 to length of list
        index_zero = copy_tiles.index(0)
        copy_tiles[index_zero] = len(copy_tiles)
        return helper.get_parity(copy_tiles)
    def is_solvable(self):
        #print('rootuple',self.root_tuple )
        cycle_parity = self.get_parity_puzzle(self.root_tuple)
        parity = cycle_parity + self.get_Manhattan_distance(self.root_tuple)
        return parity % 2 == 0
    @staticmethod
    def reset(size):
        tiles = list(range(1, size ** 2 + 1))
        tiles[size ** 2 - 1] = 0
        Debug('reset=', tiles)
        return tuple(tiles)

# verify if the puzzle is solvable (optional)

def main():
    # print('Start of Tests')
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    # x.reverse()
    # h = Heuristic(x, 3)
    # assert Heuristic.reset(3) == (1, 2, 3, 4, 5, 6, 7, 8, 0)
    # print('Passed Reset test')
    #
    # assert Heuristic.out_place([1, 2, 3, 4, 5, 6, 7, 8, 0]) == 0
    # assert Heuristic.out_place([2, 1, 3, 4, 5, 6, 7, 8, 0]) == 2
    # assert h.get_Manhattan_distance([0, 2, 3, 4, 5, 6, 7, 8, 8]) == 4
    # h = Heuristic((1, 2, 3, 0), 2)
    # print('before solvabe=',h.root_tuple)
    # assert h.is_solvable()
    # #assert h.is_solved([1, 2, 3, 0])
    # print('passed solved test')
    # print(h.solve_using_heuristics())
    # print('End of Tests')
    # x =(1,2,0,3)
    # x=(2,3,1,0)
    # x= (2, 6, 8, 4, 3, 7, 5, 1, 0)
    root_test1= (7, 1, 8, 12, 15, 6, 5, 4, 11, 9, 0, 2, 10, 13, 14, 3)
    root_test2= (9, 2, 5, 10, 15, 1, 6, 7, 14, 11, 4, 3, 13, 8, 12, 0)
    root_test3= (13, 11, 21, 3, 1, 9, 20, 16, 22, 15, 18,
                            14, 10, 23, 12, 17, 2, 7, 5, 19, 0, 8, 4, 6, 24)

    h = Heuristic(root_test2, 4)
    h.solve_using_heuristics()



if __name__ == '__main__':
    main()
