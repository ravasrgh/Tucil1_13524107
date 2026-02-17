import tkinter as tk
from tkinter import filedialog, messagebox
import time
import threading
from queens_game_solver import Board, Solver

# Palet warna
COLOR_PALETTE = [
    "#FF6B6B",  # merah muda
    "#4ECDC4",  # teal
    "#45B7D1",  # biru muda
    "#96CEB4",  # hijau sage
    "#FFEAA7",  # kuning muda
    "#DDA0DD",  # plum
    "#98D8C8",  # mint
    "#F7DC6F",  # kuning
    "#BB8FCE",  # ungu muda
    "#F0B27A",  # oranye muda
    "#85C1E9",  # biru langit
    "#82E0AA",  # hijau muda
    "#F1948A",  # salmon
    "#D7BDE2",  # lavender
    "#A3E4D7",  # aqua
    "#FAD7A0",  # peach
]

class QueensGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Queens Game Solver")
        self.root.configure(bg="#2C3E50")
        self.root.resizable(False, False)

        self.board = None
        self.solver = None
        self.cell_size = 60
        self.color_map = {}  

        self._build_ui()

    def _build_ui(self):
        """
        Membangun semua komponen GUI
        """
        top_frame = tk.Frame(self.root, bg="#2C3E50", pady=10)
        top_frame.pack(fill=tk.X, padx=10)

        self.btn_load = tk.Button(
            top_frame, text="📂 Load File", command=self.load_file,
            font=("Arial", 11, "bold"), bg="#3498DB", fg="white",
            relief=tk.FLAT, padx=15, pady=5, cursor="hand2"
        )
        self.btn_load.pack(side=tk.LEFT, padx=5)

        self.btn_load_img = tk.Button(
            top_frame, text="🖼 Load Image", command=self.load_image,
            font=("Arial", 11, "bold"), bg="#E67E22", fg="white",
            relief=tk.FLAT, padx=15, pady=5, cursor="hand2"
        )
        self.btn_load_img.pack(side=tk.LEFT, padx=5)

        self.btn_solve = tk.Button(
            top_frame, text="▶ Solve", command=self.start_solve,
            font=("Arial", 11, "bold"), bg="#27AE60", fg="white",
            relief=tk.FLAT, padx=15, pady=5, cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_solve.pack(side=tk.LEFT, padx=5)

        self.btn_save = tk.Button(
            top_frame, text="💾 Save", command=self.save_solution,
            font=("Arial", 11, "bold"), bg="#8E44AD", fg="white",
            relief=tk.FLAT, padx=15, pady=5, cursor="hand2",
            state=tk.DISABLED
        )
        self.btn_save.pack(side=tk.LEFT, padx=5)

        self.canvas_frame = tk.Frame(self.root, bg="#2C3E50")
        self.canvas_frame.pack(padx=10, pady=5)

        self.canvas = tk.Canvas(
            self.canvas_frame, width=400, height=400,
            bg="#34495E", highlightthickness=0
        )
        self.canvas.pack()

        bottom_frame = tk.Frame(self.root, bg="#2C3E50", pady=10)
        bottom_frame.pack(fill=tk.X, padx=10)

        self.label_status = tk.Label(
            bottom_frame, text="Silahkan load file terlebih dahulu.",
            font=("Arial", 11), bg="#2C3E50", fg="#ECF0F1"
        )
        self.label_status.pack()

        self.label_time = tk.Label(
            bottom_frame, text="",
            font=("Arial", 10), bg="#2C3E50", fg="#BDC3C7"
        )
        self.label_time.pack()

        self.label_iter = tk.Label(
            bottom_frame, text="",
            font=("Arial", 10), bg="#2C3E50", fg="#BDC3C7"
        )
        self.label_iter.pack()

    def _assign_colors(self):
        """Assign warna unik ke setiap region. Pakai warna asli dari image jika ada."""
        self.color_map = {}
        if self.board.region_colors:
            # Pake warna asli dari image
            self.color_map = dict(self.board.region_colors)
        else:
            # Pake default palette untuk input .txt
            regions = sorted(self.board.regions.keys())
            for i, region in enumerate(regions):
                self.color_map[region] = COLOR_PALETTE[i % len(COLOR_PALETTE)]

    def draw_board(self):
        """Gambar papan di canvas"""
        self.canvas.delete("all")
        if self.board is None or self.board.n == 0:
            return

        n = self.board.n
        self.cell_size = min(400 // n, 80)
        canvas_size = self.cell_size * n

        self.canvas.config(width=canvas_size, height=canvas_size)

        for row in range(n):
            for col in range(n):
                x1 = col * self.cell_size
                y1 = row * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                region = self.board.grid[row][col]
                color = self.color_map.get(region, "#CCCCCC")

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color, outline="#2C3E50", width=2
                )

                if (row, col) in self.board.queens:
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    size = self.cell_size // 3
                    self.canvas.create_text(
                        cx, cy, text="♛", font=("Arial", size, "bold"),
                        fill="#2C3E50"
                    )

    def load_file(self):
        """
        Buka dialog untuk pilih file .txt
        """
        filepath = filedialog.askopenfilename(
            title="Pilih file test case",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if not filepath:
            return

        self.board = Board()
        result = self.board.load_from_file(filepath)
        if result == False:
            messagebox.showerror("Error", "File tidak valid!")
            self.board = None
            return

        self._assign_colors()
        self.draw_board()
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.DISABLED)
        self.label_status.config(text=f"Board {self.board.n}x{self.board.n} loaded. Tekan Solve!")
        self.label_time.config(text="")
        self.label_iter.config(text="")

    def load_image(self):
        """
        Buka dialog untuk pilih gambar papan Queens
        """
        filepath = filedialog.askopenfilename(
            title="Pilih gambar papan Queens",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]
        )
        if not filepath:
            return

        self.board = Board()
        result = self.board.load_from_image(filepath)
        if result == False:
            messagebox.showerror("Error", "Gagal membaca gambar atau format tidak valid!")
            self.board = None
            return

        self._assign_colors()
        self.draw_board()
        self.btn_solve.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.DISABLED)
        self.label_status.config(
            text=f"Board {self.board.n}x{self.board.n} dari gambar. Tekan Solve!"
        )
        self.label_time.config(text="")
        self.label_iter.config(text="")

    def start_solve(self):
        self.btn_solve.config(state=tk.DISABLED)
        self.btn_load.config(state=tk.DISABLED)
        self.label_status.config(text="Sedang mencari solusi...")

        self.board.queens = []
        self.solver = Solver(self.board)

        thread = threading.Thread(target=self._run_solver)
        thread.start()

    def _run_solver(self):
        # Solve tanpa animasi terlebih dahulu
        start = time.time()
        found = self.solver.solve(0)
        end = time.time()
        elapsed = (end - start) * 1000

        iteration_count = self.solver.iteration_count
        self.root.after(0, self._show_results, found, elapsed, iteration_count)

        if found:
            solution = list(self.board.queens)
            iteration_count = self.solver.iteration_count

            # solve lagi dengan live update
            self.board.queens = []
            self.solver = Solver(self.board)
            self.anim_step = 0  
            self._solve_with_animation(0)

            self.board.queens = solution
            self.root.after(0, self.draw_board)

        self.root.after(0, self._enable_buttons, found)

    def _solve_with_animation(self, row):
        """
        Solve lagi dengan animasi brute force
        """
        if row == self.board.n:
            return True

        for col in range(self.board.n):
            if self.solver.is_valid(row, col):
                self.board.queens.append((row, col))
                self.solver.cols_used.add(col)
                self.solver.regions_used.add(self.board.grid[row][col])

                self.anim_step += 1
                delay = max(0.005, 0.08 / (1 + self.anim_step * 0.02))
                self.root.after(0, self.draw_board)
                time.sleep(delay)

                if self._solve_with_animation(row + 1):
                    return True

                self.board.queens.pop()
                self.solver.cols_used.remove(col)
                self.solver.regions_used.remove(self.board.grid[row][col])

                self.anim_step += 1
                self.root.after(0, self.draw_board)
                time.sleep(delay * 0.3)

        return False

    def _show_results(self, found, elapsed, iteration_count):
        if found:
            self.label_status.config(text="✅ Solusi ditemukan! Menampilkan animasi...", fg="#2ECC71")
        else:
            self.label_status.config(text="❌ Tidak ada solusi.", fg="#E74C3C")
        self.label_time.config(text=f"Waktu pencarian: {elapsed:.2f} ms")
        self.label_iter.config(
            text=f"Banyak kasus yang ditinjau: {iteration_count}"
        )

    def _enable_buttons(self, found):
        self.btn_load.config(state=tk.NORMAL)
        if found:
            self.btn_save.config(state=tk.NORMAL)
            self.label_status.config(text="✅ Solusi ditemukan!", fg="#2ECC71")

    def _on_solve_done(self, found, elapsed):
        self.draw_board()
        self.btn_load.config(state=tk.NORMAL)

        if found:
            self.label_status.config(text="✅ Solusi ditemukan!", fg="#2ECC71")
            self.btn_save.config(state=tk.NORMAL)
        else:
            self.label_status.config(text="❌ Tidak ada solusi.", fg="#E74C3C")

        self.label_time.config(text=f"Waktu pencarian: {elapsed:.2f} ms")
        self.label_iter.config(
            text=f"Banyak kasus yang ditinjau: {self.solver.iteration_count}"
        )

    def save_solution(self):
        """Simpan solusi ke file"""
        filepath = filedialog.asksaveasfilename(
            title="Simpan solusi",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
            ]
        )
        if not filepath:
            return

        if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            self._save_as_image(filepath)
        else:
            self.board.save_solution(filepath)

        messagebox.showinfo("Berhasil", f"Solusi disimpan ke {filepath}")

    def _save_as_image(self, filepath):
        """
        Render papan solusi sebagai gambar dan simpan
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 60
        border = 3
        n = self.board.n
        img_size = cell_size * n + border * (n + 1)

        img = Image.new("RGB", (img_size, img_size), "#2C3E50")
        draw = ImageDraw.Draw(img)

        for row in range(n):
            for col in range(n):
                x1 = border + col * (cell_size + border)
                y1 = border + row * (cell_size + border)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                region = self.board.grid[row][col]
                color = self.color_map.get(region, "#CCCCCC")

                draw.rectangle([x1, y1, x2, y2], fill=color)

                # Gambar queen
                if (row, col) in self.board.queens:
                    cx = (x1 + x2) // 2
                    cy = (y1 + y2) // 2
                    r = cell_size // 4
                    # Gambar lingkaran queen
                    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill="#2C3E50")
                    # Gambar teks Q di tengah
                    try:
                        font = ImageFont.truetype("arial.ttf", cell_size // 3)
                    except:
                        font = ImageFont.load_default()
                    draw.text((cx, cy), "♛", fill="white", font=font, anchor="mm")

        img.save(filepath)


if __name__ == "__main__":
    root = tk.Tk()
    app = QueensGUI(root)
    root.mainloop()
