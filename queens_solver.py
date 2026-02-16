"""
LinkedIn Queens Game Solver
Menemukan semua solusi penempatan Queen pada papan N×N
dengan constraint: satu Queen per region warna, per baris, per kolom,
dan tidak ada dua Queen yang bersebelahan (termasuk diagonal).
"""


class QueensGame:
    """
    Kelas utama untuk merepresentasikan dan menyelesaikan
    LinkedIn Queens Game dari file input .txt.
    """

    def __init__(self, filepath):
        """
        Inisialisasi game dari file input.

        Args:
            filepath (str): Path ke file .txt berisi papan permainan.
        """
        # 1. Matriks 2D — Grid Warna
        self.board = self.parse_board(filepath)
        self.n = len(self.board)

        # 2. Matriks 2D — Grid Solusi (0 = kosong, 1 = Queen)
        self.solution_grid = [[0] * self.n for _ in range(self.n)]

        # 3. Hash Map / Dictionary — Region Mapper
        self.region_map = self.build_region_map()

        # 4. Set — Tracking Constraints
        self.cols_occupied = set()
        self.regions_occupied = set()

        # 5. Counter & Solutions
        self.check_count = 0        # jumlah konfigurasi yang diperiksa
        self.solutions = []         # list semua solusi yang ditemukan
        self.solution_count = 0     # jumlah solusi

    def parse_board(self, filepath):
        """
        Parse file .txt menjadi matriks 2D (list of lists).
        Format input: setiap baris berisi karakter tanpa spasi.
        Contoh baris: "AAABBCCCD"

        Args:
            filepath (str): Path ke file input.

        Returns:
            list[list[str]]: Matriks N×N berisi karakter warna.
        """
        board = []
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:  # skip baris kosong
                    row = list(line)  # setiap karakter jadi elemen
                    board.append(row)
        return board

    def build_region_map(self):
        """
        Bangun dictionary yang mengelompokkan koordinat berdasarkan warna.
        Key: karakter warna (misal 'A', 'B', 'C')
        Value: list of (row, col) tuples

        Returns:
            dict[str, list[tuple[int, int]]]: Mapping warna → koordinat.
        """
        region_map = {}
        for r in range(self.n):
            for c in range(self.n):
                color = self.board[r][c]
                if color not in region_map:
                    region_map[color] = []
                region_map[color].append((r, c))
        return region_map

    def reset_solution(self):
        """
        Reset grid solusi dan semua constraint sets ke keadaan awal.
        Dipanggil sebelum memulai pencarian baru.
        """
        self.solution_grid = [[0] * self.n for _ in range(self.n)]
        self.cols_occupied = set()
        self.regions_occupied = set()
        self.check_count = 0
        self.solutions = []
        self.solution_count = 0

    def is_safe(self, row, col, color):
        """
        Cek apakah aman menempatkan Queen di posisi (row, col) dengan warna color.
        Mengecek 4 aturan utama permainan Queens:

        1. Cek Kolom   — Kolom belum ditempati Queen lain.
        2. Cek Wilayah — Region warna belum memiliki Queen.
        3. Cek Baris   — Baris belum ditempati (otomatis jika rekursi per baris).
        4. Cek Tetangga (Adjacency) — 8 sel di sekitar (termasuk diagonal) bebas Queen.

        Args:
            row (int): Indeks baris.
            col (int): Indeks kolom.
            color (str): Karakter warna dari region di posisi (row, col).

        Returns:
            bool: True jika aman menempatkan Queen, False jika tidak.
        """
        # 1. Cek Kolom: apakah kolom sudah ada di cols_occupied?
        if col in self.cols_occupied:
            return False

        # 2. Cek Wilayah: apakah warna sudah ada di regions_occupied?
        if color in self.regions_occupied:
            return False

        # 3. Cek Baris: otomatis aman jika iterasi dilakukan per baris
        #    (setiap baris hanya dikunjungi sekali dalam rekursi)

        # 4. Cek Tetangga (Adjacency): periksa 8 sel di sekitar (row, col)
        #    termasuk diagonal, pastikan tidak ada Queen di sana.
        #
        #    (r-1,c-1)  (r-1,c)  (r-1,c+1)
        #    (r  ,c-1)  [r , c]  (r  ,c+1)
        #    (r+1,c-1)  (r+1,c)  (r+1,c+1)
        #
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue  # skip posisi sendiri
                nr, nc = row + dr, col + dc
                if 0 <= nr < self.n and 0 <= nc < self.n:
                    if self.solution_grid[nr][nc] == 1:
                        return False

        return True

    def place_queen(self, row, col, color):
        """
        Tempatkan Queen di posisi (row, col) dan tandai constraint.

        Args:
            row (int): Indeks baris.
            col (int): Indeks kolom.
            color (str): Karakter warna region.
        """
        self.solution_grid[row][col] = 1
        self.cols_occupied.add(col)
        self.regions_occupied.add(color)

    def remove_queen(self, row, col, color):
        """
        Hapus Queen dari posisi (row, col) dan lepas constraint (backtrack).

        Args:
            row (int): Indeks baris.
            col (int): Indeks kolom.
            color (str): Karakter warna region.
        """
        self.solution_grid[row][col] = 0
        self.cols_occupied.discard(col)
        self.regions_occupied.discard(color)

    def solve(self, row=0):
        """
        Fungsi utama rekursi brute force dengan backtracking.
        Mencoba menempatkan satu Queen per baris.

        Args:
            row (int): Baris saat ini yang sedang diproses (mulai dari 0).

        Logika:
        1. Base Case  — row == N → semua Queen terpasang, simpan solusi.
        2. Iterasi    — Untuk setiap kolom c di baris ini:
           a. Hitung check_count.
           b. Cek is_safe(row, c, color).
           c. Jika aman: place, rekursi solve(row+1), lalu backtrack.
        """
        # Base Case: semua baris sudah terisi Queen
        if row == self.n:
            # Simpan salinan solusi saat ini
            solution_copy = [r[:] for r in self.solution_grid]
            self.solutions.append(solution_copy)
            self.solution_count += 1
            return

        # Iterasi setiap kolom di baris ini
        for col in range(self.n):
            color = self.board[row][col]
            self.check_count += 1  # hitung setiap konfigurasi yang diperiksa

            if self.is_safe(row, col, color):
                # Tempatkan Queen
                self.place_queen(row, col, color)

                # Rekursi ke baris berikutnya
                self.solve(row + 1)

                # Backtrack — hapus Queen, coba kemungkinan lain
                self.remove_queen(row, col, color)

    def display_board(self):
        """Tampilkan grid warna asli."""
        print(f"\nPapan Permainan ({self.n}×{self.n}):")
        print("─" * (self.n * 2 + 1))
        for row in self.board:
            print("│" + " ".join(row) + "│")
        print("─" * (self.n * 2 + 1))

    def display_solution(self):
        """
        Tampilkan solusi dalam format output.
        Queen ditandai dengan '#', sisanya tetap karakter warna asli.
        """
        print(f"\nSolusi:")
        for r in range(self.n):
            line = ""
            for c in range(self.n):
                if self.solution_grid[r][c] == 1:
                    line += "#"
                else:
                    line += self.board[r][c]
            print(line)

    def get_solution_string(self):
        """
        Kembalikan solusi dalam format string.

        Returns:
            str: String multiline dengan '#' menandai posisi Queen.
        """
        lines = []
        for r in range(self.n):
            line = ""
            for c in range(self.n):
                if self.solution_grid[r][c] == 1:
                    line += "#"
                else:
                    line += self.board[r][c]
            lines.append(line)
        return "\n".join(lines)

    def display_state(self):
        """Tampilkan keadaan saat ini dari semua struktur data."""
        print(f"\n{'='*40}")
        print("STATE SAAT INI")
        print(f"{'='*40}")

        print(f"\nUkuran papan  : {self.n}×{self.n}")
        print(f"Jumlah region : {len(self.region_map)}")

        print(f"\nRegion Map:")
        for color, cells in sorted(self.region_map.items()):
            print(f"  '{color}' → {len(cells)} sel: {cells}")

        print(f"\nCols Occupied   : {self.cols_occupied if self.cols_occupied else '(kosong)'}")
        print(f"Regions Occupied: {self.regions_occupied if self.regions_occupied else '(kosong)'}")

        # Cek queen di solution grid
        queens = []
        for r in range(self.n):
            for c in range(self.n):
                if self.solution_grid[r][c] == 1:
                    queens.append((r, c))
        print(f"Queens placed   : {queens if queens else '(belum ada)'}")
        print(f"{'='*40}")


# ─── Test / Demo ────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    import os
    import time

    # Default test file
    test_file = "test/input1.txt"
    if len(sys.argv) > 1:
        test_file = sys.argv[1]

    if not os.path.exists(test_file):
        print(f"Error: File '{test_file}' tidak ditemukan.")
        sys.exit(1)

    print("=" * 50)
    print("  LinkedIn Queens Game Solver")
    print("  Step 3: Brute Force Backtracking")
    print("=" * 50)

    # Inisialisasi game
    game = QueensGame(test_file)
    game.display_board()

    # ─── Jalankan Solver ────────────────────────────────────────────
    print(f"\n{'─'*50}")
    print("MENJALANKAN SOLVER...")
    print(f"{'─'*50}")

    start_time = time.time()
    game.solve()
    elapsed = time.time() - start_time

    print(f"\n✓ Selesai dalam {elapsed:.4f} detik")
    print(f"  Konfigurasi diperiksa : {game.check_count}")
    print(f"  Solusi ditemukan      : {game.solution_count}")

    # ─── Tampilkan Solusi ───────────────────────────────────────────
    if game.solutions:
        for idx, sol in enumerate(game.solutions):
            print(f"\n{'─'*50}")
            print(f"SOLUSI #{idx + 1}:")
            print(f"{'─'*50}")

            # Tampilkan dalam format output (# = Queen)
            for r in range(game.n):
                line = ""
                for c in range(game.n):
                    if sol[r][c] == 1:
                        line += "#"
                    else:
                        line += game.board[r][c]
                print(line)

            # Tampilkan posisi Queen
            queens = [(r, c) for r in range(game.n) for c in range(game.n) if sol[r][c] == 1]
            print(f"  Posisi Queen: {queens}")
    else:
        print("\n  Tidak ada solusi ditemukan.")

    # ─── Verifikasi dengan expected output ──────────────────────────
    expected_output = [
        "AAABBCC#D",
        "ABBB#CECD",
        "ABBBDC#CD",
        "A#ABDCCCD",
        "BBBBD#DDD",
        "FGG#DDHDD",
        "#GIGDDHDD",
        "FG#GDDHDD",
        "FGGGDDHH#",
    ]

    print(f"\n{'─'*50}")
    print("VERIFIKASI:")
    print(f"{'─'*50}")

    found_match = False
    for idx, sol in enumerate(game.solutions):
        # Bangun output string dari solusi
        output_lines = []
        for r in range(game.n):
            line = ""
            for c in range(game.n):
                if sol[r][c] == 1:
                    line += "#"
                else:
                    line += game.board[r][c]
            output_lines.append(line)

        if output_lines == expected_output:
            found_match = True
            print(f"  ✅ Solusi #{idx + 1} cocok dengan expected output!")
            break

    if not found_match:
        print("  ❌ Tidak ada solusi yang cocok dengan expected output.")


