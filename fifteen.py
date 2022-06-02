# import numpy as np
import random
from heapq import heappop
from dataclasses import dataclass, field
from typing import Any

import helper

DEBUG = False
def Debug(mess, arg1, arg2=None):
    if DEBUG:
        if arg2 is None:
            print(f"****** Debug: {mess}= {arg1}")
        else:
            print(f"****** Debug: {mess}= {arg1},{arg2}")



class Fifteen:
    STAR = 0

    # create a vector (ndarray) of tiles and the layout of tiles positions (a graph)
    # tiles are numbered 1-15, the last tile is 0 (an empty space)
    def __init__(self, size=4):
        self.visited = {}
        # self.tiles = [ list(range(1, size ** 2))] + [0]) ]
        self.size = size
        self.tiles = []
        self.shuffle()
        self.final_solution =  list(range(1, size ** 2) )+ [0]
        #print('self.final_solution=',self.final_solution)
        #print('Intial tiles =', self.tiles)

    # draw the layout with tiles 1-2-3-4
    #                            | | | |
    #                            5-6-7-8 etc.
    def __str__(self):
        return self.__repr__()

    # print the vector of tiles as a 2d array 1 2 3 4
    #                                         5 6 7 8 etc.
    def __repr__(self):
        ret_str = ''
        for index in range(self.size ** 2):
            if index % self.size == 0:
                ret_str += '\n'
            ret_str += f'{self.tiles[index]:^5}'
        return ret_str

    # exchange i-tile with j-tile, tiles are numbered 1-15, the last tile is 0 (empty space)
    # the exchange can be done using a dot product of the vector of tiles and the matrix of
    # the corresponding transformation (vector by matrix multiplication)
    # return the dot product
    def transpose(self, i, j):
        pass

    # checks if the move is valid: one of the tiles is 0 and another tile is its neighbor
    # index of clicked tile must
    # either
    # Case 1: In same Row
    # Then clicked square is in col_star -1 or col_star+1 spot
    # Case 2: in same col
    # Then clicked square is in row_star -1 or row_star+1 spot
    def get_row_col(self, index_tile):
        row = index_tile // self.size
        col = index_tile % self.size
        return row, col

    def get_square(self, i):
        return self.tiles[i]

    def set_square(self, id, new_value):
        self.tiles[id] = new_value

    # update the vector of tiles
    # assign the vector to the return of transpose()
    def update(self, i, j):
        pass

    # shuffle tiles
    def shuffle(self):
        can_solve = False

        while not can_solve:
            ordered_list = list(range(0, self.size ** 2))
            Debug('Ordered list', ordered_list)
            self.tiles = random.sample(ordered_list, self.size ** 2)
            can_solve = self.is_solvable()
            #print('Can Solve=', can_solve)

    # verify if the puzzle is solved
    def is_solved(self):
        is_solved = self.tiles == self.final_solution

        Debug('is_solved=', is_solved)
        return is_solved

    # verify if the puzzle is solvable (optional)
    def is_solvable(self):
        copy_tiles = self.tiles[:]
        index_zero = copy_tiles.index(0)
        copy_tiles[index_zero] = len(copy_tiles)
        parity = helper.get_parity(copy_tiles) + self.get_Manhattan_distance()
        return parity % 2 == 0

    def get_Manhattan_distance(self):
        index_0 = self.get_star_location()
        row, col = self.get_row_col(index_0)
        row_distance = (self.size - 1) - row
        col_distance = (self.size - 1) - col
        m_distance = row_distance + col_distance
        Debug("get_Manhattan_distance", m_distance)
        return m_distance

    def get_star_location(self):
        return self.tiles.index(Fifteen.STAR)

    def swap(node, p1, p2):
        node[p1], node[p2] = node[p2], node[p1]
    @dataclass(frozen = True)
    class DirTuple():
        def __init___(self, x, y):
            x:str
            y:str
    from collections import namedtuple
    DirTuple= namedtuple('DirTuple', 'type,x,y')
    LEFT_DIR = DirTuple('left',-1,0)
    RIGHT_DIR = DirTuple('right',1,0)
    UP_DIR = DirTuple('up',0,-1)
    DOWN_DIR = DirTuple('down',0,1)
    DIR_VECTORS = (LEFT_DIR,RIGHT_DIR,UP_DIR,DOWN_DIR)
    def get_index(self,row,col):
        return row*self.size + col
    @dataclass(frozen = True)
    class heap_item:
        parent: tuple
        move: str
    def expand_nodes(self ,node):
        expanded_nodes = []
        for dir_vect in Fifteen.DIR_VECTORS:
            new_node = self.expand_node_dir( node, dir_vect)
            if expand_dir is not None:
                expanded_nodes.append(new_node)
        return expanded_nodes



    def expand_node_dir(self, trial_node, dir_vector):

        Debug(' Before: ', trial_node)
        index_star = trial_node.index(Fifteen.STAR)
        row_star, col_star = self.get_row_col(index_star)
        col_left_move = col_star + dir_vector.x
        row_left_move = row_star + dir_vector.y
        Debug('col_left_move', col_left_move)
        Debug('row_left_move', row_left_move)
        Debug('get_left_move, row_star=', row_star)
        if (0 <= col_left_move < self.size) and (0 <= row_left_move < self.size):
            new_node = trial_node[:]
            index_left = self.get_index(row_left_move, col_left_move)
            Fifteen.swap(new_node, index_star, index_left)
        else:
            new_node = None
        Debug('Left Move After: ', new_node)
        return new_node

    def get_left_move(self, trial_node):
        return self.get_move(trial_node, Fifteen.LEFT_DIR)

    def is_valid_move(self, square_id):

        row_click, col_click = self.get_row_col(square_id)
        # assume this is row, col of clicked square
        row_star, col_star = self.get_row_col(self.tiles.index(Fifteen.STAR))
        is_valid_left = col_star == (col_click - 1) and (row_star == row_click)
        is_valid_right = (col_star == (col_click + 1)) and (row_star == row_click)
        is_valid_up = (row_star == (row_click - 1)) and (col_star == col_click)
        is_valid_down = (row_star == (row_click + 1)) and (col_star == col_click)
        is_valid = is_valid_left or is_valid_right or is_valid_down or is_valid_up
        # Debug('Col_star =',col_star)
        # Debug('Row_star =',row_star)
        # Debug('col_click =',col_click)
        # Debug('row_click =',row_click)
        Debug('is_valid_right =', is_valid_right)
        Debug('is_valid_left =', is_valid_left)
        Debug('is_valid_down =', is_valid_down)
        Debug('is_valid_up =', is_valid_up)
        return is_valid



    def make_move(self, button_id):
        #print('print move', self.tiles)
        temp = self.tiles[button_id]
        star_id = self.get_star_location()
        self.tiles[star_id] = self.tiles[button_id]
        self.tiles[button_id] = Fifteen.STAR
        #print('after move', self.tiles)





    def out_place(self):
        count_out_place = 0
        for index in range(len(self.tiles) - 1):
            if self.tiles[index] != 0 and self.tiles[index] != (index + 1):
                count_out_place += 1
        Debug('out_place=', count_out_place)
        return count_out_place

    def is_solved(self):
        is_solved = True
        for index in range(len(self.tiles) - 1):
            if self.tiles[index] != (index + 1):
                is_solved = False
                break
        return is_solved

    def get_heuristic(self, node):
        self.tiles = node
        return self.get_Manhattan_distance() + self.out_place()

    def next_node_heap():
        pass



def reset(size):
    tiles = list(range(1, size ** 2 + 1))
    tiles[15] = 0
    Debug('reset=', tiles)
    return tiles


def transpose(tiles, i, j):
    temp = tiles[i]
    tiles[i] = tiles[j]
    tiles[j] = temp


def main():
    print('Start of Tests')
    x = Fifteen(4)
    fiveteen = x
    x.tiles = reset(x.size)

    assert x.get_Manhattan_distance() == 0
    x.tiles[0] = 0
    x.tiles[15] = 1
    assert x.get_Manhattan_distance() == 6
    x.tiles = reset(4)
    x.tiles[3] = 0
    x.tiles[15] = 4
    assert x.get_Manhattan_distance() == 3
    assert x.out_place() == 0
    transpose(x.tiles, 4, 5)
    transpose(x.tiles, 6, 9)
    transpose(x.tiles, 1, 2)
    assert x.out_place() == 6
    trial_before_left_node = reset(x.size)
    after_left_move = trial_before_left_node[:]
    after_left_move[14] = 0
    after_left_move[15] = 15
    direct_msg = ['left','right','up','down']
    test_node= reset(4)
    test_node[14]= 0
    test_node[15]= 15
    print('Before Expand',test_node)
    for dir_vect in Fifteen.DIR_VECTORS:
        print( dir_vect.type,x.expand_node_dir( test_node, dir_vect) )
if __name__ == '__main__':
    main()
