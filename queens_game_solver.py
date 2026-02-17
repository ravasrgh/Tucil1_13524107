class Board:
    def __init__(self):
        self.n = 0
        self.grid = []
        self.regions = {}
        self.queens = []

    def load_from_file(self, filepath):
        """
        Membaca file .txt dan mengubah menjadi data yang bisa dipakai
        """
        # tambahkan data ke grid
        try:
            with open(filepath) as file:
                for line in file:
                    line = line.strip()
                    if line:
                        row = list(line)
                        self.grid.append(row)
                        # kaya gini tuh bisa juga:
                        # self.grid.append(list(line.strip()))
        except FileNotFoundError:
            print("File tidak ditemukan.")
            return False

        # hitung jumlah baris (n)
        self.n = len(self.grid)

        # tambahkan data daerah warna
        for row in range(self.n):
            for col in range(len(self.grid[row])):
                colour = self.grid[row][col]
                if colour not in self.regions:
                    self.regions[colour] = []
                self.regions[colour].append((row,col))

        if not self.validate():
            return False

    def display(self):
        for row in range(self.n):
            for col in range(self.n):
                print(self.grid[row][col],end="")
            print()

    def validate(self):
        if self.n == 0:
            print("Papan kosong.")
            return False 

        for row in range(self.n):
            if len(self.grid[row]) != self.n:
                print("Papan tidak persegi")
                return False
                
        if len(self.regions) != self.n:
            print("Jumlah warna tidak sama dengan jumlah sisi papan.")
            return False
        
        return True

class Solver:
    def __init__(self, board):
        self.iteration_count = 0 
        self.board = board
        self.cols_used = set()
        self.regions_used = set()

    def is_valid(self, row, col):
        if col in self.cols_used:
            return False
        
        if self.board.grid[row][col] in self.regions_used:
            return False
        
        if abs(self.board.queens[row] - row) <= 1 and abs(self.board.queens[col] - col) <= 1:
            return False



board = Board()
result = board.load_from_file("test/input1.txt")
if result != False:
    board.display()


        