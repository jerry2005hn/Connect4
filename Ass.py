"""
Name: Minh Tuan Nguyen
UPI: 142905798
Comment: This program is the Connect 4 game between the player and an AI"""
import math
class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2
    def num_free_positions_in_column(self, column):
        return self.size-self.num_entries[column]
    def game_over(self):
        for i in self.num_entries:
            if i!=self.size:
                return False
        return True
    def display(self):
        for row in range(self.size-1,-1,-1):
            for col in range(0,self.size):
                if self.items[col][row]==1:
                    print("o",end=" ")
                elif self.items[col][row]==2:
                    print("x",end=" ")
                else:
                    print(" ",end=" ")
            print()
        print("-"*(self.size*2-1))
        for i in range(self.size):
            print(i,end=" ")
        print()
        print("Points player 1:",self.points[0])
        print("Points player 2:",self.points[1])
    def num_new_points(self, column, row, player):
        points=0
        count=0
        #horizontal
        for i in range(-3,4):
            col_check=column+i
            if 0<=col_check and col_check<self.size:
                if self.items[col_check][row]==player:
                    count+=1
                else:
                    count=0
                if count>=4:
                    points+=1
        #vertical
        count=0
        for i in range(-3,4):
            row_check=row+i
            if 0<=row_check and row_check<self.size:
                if self.items[column][row_check]==player:
                    count+=1
                else:
                    count=0
                if count>=4:
                    points+=1
        #right diagonal
        count=0
        for i in range(-3,4):
            col_check=column+i
            row_check=row+i
            if 0<=col_check and col_check<self.size and 0<=row_check and row_check<self.size:
                if self.items[col_check][row_check]==player:
                    count+=1
                else:
                    count=0
                if count>=4:
                    points+=1
        #left diagonal
        count=0
        for i in range(-3,4):
            col_check=column-i
            row_check=row+i
            if 0<=col_check and col_check<self.size and 0<=row_check and row_check<self.size:
                if self.items[col_check][row_check]==player:
                    count+=1
                else:
                    count=0
                if count>=4:
                    points+=1
        return points
    def add(self, column, player):
        if self.num_entries[column]>=self.size or column<0 or column>=self.size:
            return False
        else:
            row_ava=self.num_entries[column]
            self.items[column][row_ava]=player
            self.points[player-1]+=self.num_new_points(column, row_ava, player)
            self.num_entries[column]+=1
            return True
        
    def free_slots_as_close_to_middle_as_possible(self):
        cols=[]
        result=[]
        mid=math.floor(self.size/2)
        if self.size%2==0:
            for i in range(1,mid+1):
                cols.append(mid+(-1*i))
                cols.append(mid+i-1)
        else:
            if self.num_free_positions_in_column(mid)>0:
                cols.append(mid)
            for i in range(1,mid+1):
                cols.append(mid+(-1*i))
                cols.append(mid+i)
        for col in cols:
            if self.num_free_positions_in_column(col)>0:
                result.append(col)
        return result
    def column_resulting_in_max_points(self, player):             
        best_spot=self.free_slots_as_close_to_middle_as_possible()[0]
        max_point=0
        ava_spots=self.free_slots_as_close_to_middle_as_possible()
        for spot in ava_spots:
            self.items[spot][self.num_entries[spot]]=player
            points_creates=self.num_new_points(spot,self.num_entries[spot],player)
            self.items[spot][self.num_entries[spot]]=0
            if points_creates>max_point:
                max_point=points_creates
                best_spot=spot
        return (best_spot,max_point)

class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                valid_input = False
                while not valid_input:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                        else:
                            if self.board.add(column, player_number+1):
                                valid_input = True
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
            else:
                # Choose move which maximises new points for computer player
                (best_column, max_points)=self.board.column_resulting_in_max_points(2)
                if max_points>0:
                    column=best_column
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (best_column, max_points)=self.board.column_resulting_in_max_points(1)
                    if max_points>0:
                        column=best_column
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(6)
game.play()        