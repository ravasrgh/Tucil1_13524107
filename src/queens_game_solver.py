import time
import os
import math

class Board:
    def __init__(self):
        self.n = 0
        self.grid = []
        self.regions = {}
        self.queens = []
        self.region_colors = {}

    def load_from_file(self, filepath):
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
                if (row,col) in self.queens:
                    print("#",end="")
                else:
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

    def load_from_image(self, filepath):
        try:
            from PIL import Image
        except ImportError:
            print("Library Pillow belum terinstall. Jalankan: pip install Pillow")
            return False

        try:
            img = Image.open(filepath).convert("RGB")
        except Exception:
            print("Gagal membuka file gambar.")
            return False

        width, height = img.size
        pixels = img.load()

        col_positions = self._find_cell_positions(pixels, width, height, axis="x")
        if len(col_positions) < 2:
            print("Tidak bisa mendeteksi kolom dari gambar.")
            return False

        first_col_center = (col_positions[0][0] + col_positions[0][1]) // 2
        row_positions = self._find_cell_positions(pixels, width, height, axis="y", scan_at=first_col_center)

        n_cols = len(col_positions)
        n_rows = len(row_positions)

        if n_cols != n_rows or n_cols < 2:
            print(f"Grid tidak valid: {n_rows} baris, {n_cols} kolom terdeteksi.")
            return False

        self.n = n_cols

        raw_colors = []
        for row_start, row_end in row_positions:
            row_colors = []
            for col_start, col_end in col_positions:
                cx = (col_start + col_end) // 2
                cy = (row_start + row_end) // 2
                color = pixels[cx, cy]
                row_colors.append(color)
            raw_colors.append(row_colors)

        color_groups = []  
        letter_index = 0
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        self.grid = []
        for row in range(self.n):
            grid_row = []
            for col in range(self.n):
                color = raw_colors[row][col]
                assigned = False
                for i, (rep_color, letter) in enumerate(color_groups):
                    if self._color_distance(color, rep_color) < 35:
                        grid_row.append(letter)
                        assigned = True
                        break
                if not assigned:
                    letter = letters[letter_index % len(letters)]
                    letter_index += 1
                    color_groups.append((color, letter))
                    grid_row.append(letter)
            self.grid.append(grid_row)

        # Simpan mapping warna asli untuk GUI
        self.region_colors = {}
        for rep_color, letter in color_groups:
            r, g, b = rep_color
            self.region_colors[letter] = f"#{r:02x}{g:02x}{b:02x}"

        self.regions = {}
        for row in range(self.n):
            for col in range(self.n):
                colour = self.grid[row][col]
                if colour not in self.regions:
                    self.regions[colour] = []
                self.regions[colour].append((row, col))

        if not self.validate():
            return False

        return True

    def _find_cell_positions(self, pixels, width, height, axis="x", scan_at=None):
        if axis == "x":
            length = width
            scan_pos = scan_at if scan_at else height // 4
            get_pixel = lambda i: pixels[i, scan_pos]
        else:
            length = height
            scan_pos = scan_at if scan_at else width // 4
            get_pixel = lambda i: pixels[scan_pos, i]

        is_dark = []
        for i in range(length):
            c = get_pixel(i)
            is_dark.append(c[0] < 100 and c[1] < 100 and c[2] < 100)

        cells = []
        in_cell = False
        start = 0
        for i in range(length):
            if not is_dark[i] and not in_cell:
                start = i
                in_cell = True
            elif is_dark[i] and in_cell:
                cells.append((start, i - 1))
                in_cell = False
        if in_cell:
            cells.append((start, length - 1))

        min_size = 10
        cells = [(s, e) for s, e in cells if (e - s + 1) >= min_size]

        return cells

    def _color_distance(self, c1, c2):
        # hitung jarak euclidean buat dua warna rgb
        return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2 + (c1[2]-c2[2])**2)

    def save_solution(self, filepath):
        with open(filepath, "w") as file:
            for row in range(self.n):
                for col in range(self.n):
                    if (row, col) in self.queens:
                        file.write("#")
                    else:
                        file.write(self.grid[row][col])
                file.write("\n")

class BruteForceSolver:
    def __init__(self, board):
        self.iteration_count = 0
        self.board = board

    def is_valid(self, config):
        for i in range(self.board.n):
            for j in range(i+1,self.board.n):
                if config[i] == config[j]:
                    return False
                if self.board.grid[i][config[i]] == self.board.grid[j][config[j]]:
                    return False
                if abs(i - j) <= 1 and abs(config[i] - config[j]) <= 1:
                    return False
        return True

    def solve(self, on_update=None, get_interval=None):
        n = self.board.n
        config = [0 for i in range(n)]
        while True:
            self.iteration_count += 1

            if on_update and get_interval:
                interval = get_interval()
                if self.iteration_count % interval == 0:
                    self.board.queens = [(row, config[row]) for row in range(n)]
                    on_update()

            if self.is_valid(config):
                self.board.queens = [(row, config[row]) for row in range(n)]
                return True
            else:
                i = n - 1
                config[i] += 1

                while config[i] >= n:
                    config[i] = 0
                    i -= 1
                    if i < 0:
                        return False
                    config[i] += 1

class OptimizedSolver:
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
        
        for (queen_row, queen_col) in self.board.queens:
            if abs(queen_row - row) <= 1 and abs(queen_col - col) <= 1:
                return False

        return True

    def solve(self, row, on_update=None, get_interval=None):
        if row == self.board.n:
            return True
    
        for col in range(self.board.n):  
            self.iteration_count += 1

            if on_update and get_interval:
                interval = get_interval()
                if self.iteration_count % interval == 0:
                    on_update()

            if self.is_valid(row,col):
                self.board.queens.append((row,col))
                self.cols_used.add(col)
                self.regions_used.add(self.board.grid[row][col])
                if self.solve(row+1, on_update, get_interval):
                    return True
                self.board.queens.pop()
                self.cols_used.remove(col)
                self.regions_used.remove(self.board.grid[row][col])
        return False

#main
if __name__ == "__main__":
    filepath = input("Masukkan path file test case (.txt): ")
    board = Board()
    result = board.load_from_file(filepath)
    if result != False:
        solver = OptimizedSolver(board)
        start = time.time()
        found = solver.solve(0)
        end = time.time()
        elapsed_time = (end - start) * 1000
        if found:
            print("Solusi ditemukan!")
            board.display()
            print(f"Waktu pencarian: {elapsed_time:.2f} ms")
            print(f"Banyak kasus yang ditinjau: {solver.iteration_count}")
            simpan = input("Apakah Anda ingin menyimpan solusi? (Ya/Tidak): ")
            if simpan == "Ya":
                nama_file = input("Masukkan nama file output: ")
                board.save_solution(nama_file)
                print(f"Solusi disimpan ke {nama_file}")
        else:
            print("Tidak ada solusi.")
