import time
import os
import math

class Board:
    def __init__(self):
        self.n = 0
        self.grid = []
        self.regions = {}
        self.queens = []
        self.region_colors = {}  # mapping region letter -> hex color (dari image)

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
        """
        Membaca gambar papan Queens dan mengekstrak konfigurasi warna.
        Mendeteksi grid lewat garis border hitam, sampling warna tiap sel.
        """
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

        # Deteksi posisi sel: pertama cari kolom, lalu pakai tengah kolom pertama untuk cari baris
        col_positions = self._find_cell_positions(pixels, width, height, axis="x")
        if len(col_positions) < 2:
            print("Tidak bisa mendeteksi kolom dari gambar.")
            return False
        # Scan baris di tengah kolom pertama (pasti bukan border)
        first_col_center = (col_positions[0][0] + col_positions[0][1]) // 2
        row_positions = self._find_cell_positions(pixels, width, height, axis="y", scan_at=first_col_center)

        n_cols = len(col_positions)
        n_rows = len(row_positions)

        if n_cols != n_rows or n_cols < 2:
            print(f"Grid tidak valid: {n_rows} baris, {n_cols} kolom terdeteksi.")
            return False

        self.n = n_cols

        # Sampling warna dari tengah setiap sel
        raw_colors = []
        for row_start, row_end in row_positions:
            row_colors = []
            for col_start, col_end in col_positions:
                cx = (col_start + col_end) // 2
                cy = (row_start + row_end) // 2
                color = pixels[cx, cy]
                row_colors.append(color)
            raw_colors.append(row_colors)

        # Grouping warna serupa
        color_groups = []  # list of (representative_color, letter)
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

        # Bangun regions dictionary
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
        """
        Mencari posisi sel di sepanjang sumbu tertentu.
        Mendeteksi border hitam dan mengembalikan list of (start, end) untuk tiap sel.
        scan_at: posisi di sumbu tegak lurus untuk scanning (default: tengah)
        """
        if axis == "x":
            length = width
            scan_pos = scan_at if scan_at else height // 4
            get_pixel = lambda i: pixels[i, scan_pos]
        else:
            length = height
            scan_pos = scan_at if scan_at else width // 4
            get_pixel = lambda i: pixels[scan_pos, i]

        # Tandai pixel yang gelap (border)
        is_dark = []
        for i in range(length):
            c = get_pixel(i)
            # Pixel dianggap border jika gelap
            is_dark.append(c[0] < 100 and c[1] < 100 and c[2] < 100)

        # Cari runs of non-dark pixels (= sel berwarna)
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

        # Filter: buang sel yang terlalu kecil (noise dari anti-aliasing)
        min_size = 10
        cells = [(s, e) for s, e in cells if (e - s + 1) >= min_size]

        return cells

    def _color_distance(self, c1, c2):
        """Hitung jarak Euclidean antara dua warna RGB."""
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
        
        for (queen_row, queen_col) in self.board.queens:
            if abs(queen_row - row) <= 1 and abs(queen_col - col) <= 1:
                return False

        return True

    def solve(self, row, live_update=False):
        if row == self.board.n:
            return True
    
        for col in range(self.board.n):  
            self.iteration_count += 1 
            if self.is_valid(row,col):
                self.board.queens.append((row,col))
                if live_update:
                    print("\033[H\033[J", end="")
                    self.board.display()  
                    time.sleep(0.02) 
                self.cols_used.add(col)
                self.regions_used.add(self.board.grid[row][col])
                if self.solve(row+1, live_update):
                    return True
                self.board.queens.pop()
                self.cols_used.remove(col)
                self.regions_used.remove(self.board.grid[row][col])
        return False


if __name__ == "__main__":
    filepath = input("Masukkan path file test case (.txt): ")
    board = Board()
    result = board.load_from_file(filepath)
    if result != False:
        solver = Solver(board)
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
