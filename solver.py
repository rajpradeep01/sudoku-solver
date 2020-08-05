
sudoku=[[0]*9]*9

def printsudoku():
	global sudoku
	for i in range(9):
		for j in range(9):
			print(sudoku[i][j],end="")
		print()
	print()

def check(a,b,c):
	for i in range(9):
		if sudoku[a][i]==c:
			return False
		if sudoku[i][b]==c:
			return False
	a=(a//3)*3
	b=(b//3)*3
	for i in range(0,3):
		for j in range(0,3):
			if sudoku[a+i][b+j]==c:
				return False
	return True


def solve():

	global sudoku

	for i in range(9):
		for j in range(9):
			if sudoku[i][j]==0:
				for z in range(1,10):
					if check(i,j,z):
						sudoku[i][j]=z;
						if solve():
							return True
						sudoku[i][j]=0
				return False
	printsudoku()
	return False

def main(): 
	global sudoku
	sudoku=[[0,0,0,0,0,0,2,0,0],
			[0,8,0,0,0,7,0,9,0],
			[6,0,2,0,0,0,5,0,0],
			[0,7,0,0,6,0,0,0,0],
			[0,0,0,9,0,1,0,0,0],
			[0,0,0,0,2,0,0,4,0],
			[0,0,5,0,0,0,6,0,3],
			[0,9,0,4,0,0,0,7,0],
			[0,0,6,0,0,0,0,0,0]]
	if solve():
		printsudoku()
	else:
		print("NO VALID MATRIX")


if __name__=="__main__": 
    main() 