#Given a chessboard, if it is black, print YES. Otherwise, print NO
#8x8 chessboard

x_coord = int(input())
y_coord = int(input())

if(x_coord + y_coord % 2 == 0):
    print("YES")
else:
    print("NO")