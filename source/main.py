import tkinter as tk
from tkinter import messagebox

# Import class bàn cờ
from board import Caro

# Import AI
from ai import Agent


# =========================================================
# MÀN HÌNH MENU
# =========================================================

class MenuScreen:

    def __init__(self, root):

        # Cửa sổ chính
        self.root = root

        # Tiêu đề cửa sổ
        self.root.title("Gomoku AI")

        # Kích thước cửa sổ
        self.root.geometry("420x420")

        # Màu nền
        self.root.configure(bg="#2c3e50")

        # ============================================
        # BIẾN LƯU CHẾ ĐỘ
        # ============================================

        # Thuật toán
        self.algorithm = tk.StringVar(value="alphabeta")

        # Độ sâu tìm kiếm
        self.depth = tk.IntVar(value=3)

        # Người đi trước
        self.first = tk.StringVar(value="human")

        # Tạo giao diện
        self.build_ui()

    # =====================================================
    # TẠO GIAO DIỆN MENU
    # =====================================================

    def build_ui(self):

        # ============================================
        # TITLE
        # ============================================

        title = tk.Label(

            self.root,

            text="🎮 GOMOKU AI",

            font=("Arial", 22, "bold"),

            bg="#2c3e50",

            fg="white"
        )

        title.pack(pady=20)

        # ============================================
        # FRAME CHỌN THUẬT TOÁN
        # ============================================

        algo_frame = tk.LabelFrame(

            self.root,

            text="Thuật toán",

            font=("Arial", 11, "bold"),

            bg="#34495e",

            fg="white"
        )

        algo_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # --------------------------------------------
        # Alpha Beta
        # --------------------------------------------

        tk.Radiobutton(

            algo_frame,

            text="Alpha-Beta",

            variable=self.algorithm,

            value="alphabeta",

            bg="#34495e",

            fg="white",

            selectcolor="#2c3e50"

        ).pack(anchor="w", padx=10, pady=5)

        # --------------------------------------------
        # Minimax
        # --------------------------------------------

        tk.Radiobutton(

            algo_frame,

            text="Minimax",

            variable=self.algorithm,

            value="minimax",

            bg="#34495e",

            fg="white",

            selectcolor="#2c3e50"

        ).pack(anchor="w", padx=10, pady=5)

        # --------------------------------------------
        # Compare mode
        # --------------------------------------------

        tk.Radiobutton(

            algo_frame,

            text="Compare",

            variable=self.algorithm,

            value="compare",

            bg="#34495e",

            fg="white",

            selectcolor="#2c3e50"

        ).pack(anchor="w", padx=10, pady=5)

        # ============================================
        # FRAME ĐỘ SÂU
        # ============================================

        depth_frame = tk.LabelFrame(

            self.root,

            text="Độ sâu tìm kiếm",

            font=("Arial", 11, "bold"),

            bg="#34495e",

            fg="white"
        )

        depth_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # Thanh kéo chọn depth
        tk.Scale(

            depth_frame,

            from_=1,

            to=5,

            orient="horizontal",

            variable=self.depth,

            bg="#34495e",

            fg="white",

            highlightthickness=0

        ).pack(fill="x", padx=10)

        # ============================================
        # FRAME CHỌN NGƯỜI ĐI TRƯỚC
        # ============================================

        first_frame = tk.LabelFrame(

            self.root,

            text="Lượt đi đầu",

            font=("Arial", 11, "bold"),

            bg="#34495e",

            fg="white"
        )

        first_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        # --------------------------------------------
        # Người chơi đi trước
        # --------------------------------------------

        tk.Radiobutton(

            first_frame,

            text="Người chơi đi trước",

            variable=self.first,

            value="human",

            bg="#34495e",

            fg="white",

            selectcolor="#2c3e50"

        ).pack(anchor="w", padx=10, pady=5)

        # --------------------------------------------
        # Máy đi trước
        # --------------------------------------------

        tk.Radiobutton(

            first_frame,

            text="Máy đi trước",

            variable=self.first,

            value="ai",

            bg="#34495e",

            fg="white",

            selectcolor="#2c3e50"

        ).pack(anchor="w", padx=10, pady=5)

        # ============================================
        # BUTTON START
        # ============================================

        tk.Button(

            self.root,

            text="▶ BẮT ĐẦU",

            font=("Arial", 14, "bold"),

            bg="#27ae60",

            fg="white",

            width=20,

            command=self.start_game

        ).pack(pady=20)

    # =====================================================
    # BẮT ĐẦU GAME
    # =====================================================

    def start_game(self):

        # Xóa toàn bộ widget menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Mở game
        GameGUI(

            self.root,

            self.algorithm.get(),

            self.depth.get(),

            self.first.get()
        )


# =========================================================
# MÀN HÌNH GAME
# =========================================================

class GameGUI:

    def __init__(self, root, algorithm, depth, first):

        # Cửa sổ chính
        self.root = root

        # Thuật toán
        self.algorithm = algorithm

        # Độ sâu
        self.depth = depth

        # Người đi trước
        self.first = first

        # Tạo bàn cờ
        self.board = Caro(9)

        # Tạo AI
        self.agent = Agent(depth)

        # Trạng thái game
        self.game_over = False

        # AI đang suy nghĩ
        self.ai_thinking = False

        # Kích thước mỗi ô
        self.cell = 50

        # Tạo giao diện
        self.build_ui()

        # Nếu AI đi trước
        if self.first == "ai":

            self.root.after(500, self.ai_turn)

    # =====================================================
    # TẠO GIAO DIỆN GAME
    # =====================================================

    def build_ui(self):

        # Kích thước cửa sổ
        self.root.geometry("850x620")

        # Màu nền
        self.root.configure(bg="#2c3e50")

        # ============================================
        # STATUS
        # ============================================

        top = tk.Frame(
            self.root,
            bg="#2c3e50"
        )

        top.pack()

        # Dòng trạng thái
        self.status = tk.Label(

            top,

            text="Lượt của bạn",

            font=("Arial", 14, "bold"),

            bg="#2c3e50",

            fg="white"
        )

        self.status.pack(pady=10)

        # ============================================
        # FRAME CHÍNH
        # ============================================

        main = tk.Frame(
            self.root,
            bg="#2c3e50"
        )

        main.pack()

        # ============================================
        # CANVAS BÀN CỜ
        # ============================================

        self.canvas = tk.Canvas(

            main,

            width=450,

            height=450,

            bg="#d7ccc8"
        )

        self.canvas.pack(
            side="left",
            padx=10
        )

        # Bắt sự kiện click chuột
        self.canvas.bind(
            "<Button-1>",
            self.click
        )

        # ============================================
        # PANEL THÔNG TIN AI
        # ============================================

        right = tk.Frame(

            main,

            bg="#34495e",

            width=320
        )

        right.pack(
            side="right",
            fill="y",
            padx=10
        )

        # Tiêu đề panel
        tk.Label(

            right,

            text="📊 THÔNG TIN AI",

            font=("Arial", 14, "bold"),

            bg="#34495e",

            fg="white"

        ).pack(pady=10)

        # Label hiển thị thông số
        self.info = tk.Label(

            right,

            text="",

            justify="left",

            anchor="nw",

            font=("Consolas", 10),

            bg="#34495e",

            fg="white"
        )

        self.info.pack(
            padx=10,
            pady=10
        )

        # ============================================
        # BUTTONS
        # ============================================

        btn_frame = tk.Frame(
            self.root,
            bg="#2c3e50"
        )

        btn_frame.pack(pady=10)

        # --------------------------------------------
        # Button chơi lại
        # --------------------------------------------

        tk.Button(

            btn_frame,

            text="🔄 Chơi lại",

            width=15,

            bg="#3498db",

            fg="white",

            command=self.restart

        ).pack(side="left", padx=5)

        # --------------------------------------------
        # Button quay lại menu
        # --------------------------------------------

        tk.Button(

            btn_frame,

            text="🏠 Menu",

            width=15,

            bg="#e67e22",

            fg="white",

            command=self.back_menu

        ).pack(side="left", padx=5)

        # --------------------------------------------
        # Button thoát
        # --------------------------------------------

        tk.Button(

            btn_frame,

            text="❌ Thoát",

            width=15,

            bg="#e74c3c",

            fg="white",

            command=self.root.quit

        ).pack(side="left", padx=5)

        # Vẽ bàn cờ
        self.draw_board()

    # =====================================================
    # VẼ BÀN CỜ
    # =====================================================

    def draw_board(self):

        # Xóa toàn bộ canvas
        self.canvas.delete("all")

        # Vẽ lưới
        for i in range(10):

            # Đường ngang
            self.canvas.create_line(

                0,
                i * self.cell,

                450,
                i * self.cell
            )

            # Đường dọc
            self.canvas.create_line(

                i * self.cell,
                0,

                i * self.cell,
                450
            )

        # ============================================
        # VẼ QUÂN CỜ
        # ============================================

        for x in range(9):

            for y in range(9):

                p = self.board.grid[x][y]

                # Bỏ qua ô trống
                if p == '.':
                    continue

                # Tính tọa độ tâm
                cx = y * self.cell + 25
                cy = x * self.cell + 25

                # Nếu là X
                if p == 'X':

                    self.canvas.create_oval(

                        cx - 18,
                        cy - 18,

                        cx + 18,
                        cy + 18,

                        fill="#3498db"
                    )

                    self.canvas.create_text(

                        cx,
                        cy,

                        text="X",

                        fill="white",

                        font=("Arial", 18, "bold")
                    )

                # Nếu là O
                else:

                    self.canvas.create_oval(

                        cx - 18,
                        cy - 18,

                        cx + 18,
                        cy + 18,

                        fill="#e74c3c"
                    )

                    self.canvas.create_text(

                        cx,
                        cy,

                        text="O",

                        fill="white",

                        font=("Arial", 18, "bold")
                    )
    # =====================================================
    # XỬ LÝ CLICK CHUỘT
    # =====================================================

    def click(self, event):

        # Nếu game kết thúc -> không cho đánh
        if self.game_over:
            return

        # Nếu AI đang suy nghĩ -> không cho đánh
        if self.ai_thinking:
            return

        # ============================================
        # TÍNH TỌA ĐỘ Ô ĐƯỢC CLICK
        # ============================================

        col = event.x // self.cell
        row = event.y // self.cell

        # ============================================
        # KIỂM TRA HỢP LỆ
        # ============================================

        if not self.board.is_valid_move(row, col):
            return

        # ============================================
        # NGƯỜI CHƠI ĐÁNH
        # ============================================

        self.board.make_move(row, col, 'X')

        # Vẽ lại bàn cờ
        self.draw_board()

        # ============================================
        # KIỂM TRA THẮNG
        # ============================================

        if self.board.check_winner() == 'X':

            self.game_over = True

            messagebox.showinfo(
                "Kết quả",
                "🎉 BẠN THẮNG!"
            )

            return

        # ============================================
        # KIỂM TRA HÒA
        # ============================================

        if self.board.is_full():

            self.game_over = True

            messagebox.showinfo(
                "Kết quả",
                "🤝 HÒA!"
            )

            return

        # ============================================
        # TỚI LƯỢT AI
        # ============================================

        self.ai_turn()

    # =====================================================
    # LƯỢT ĐÁNH CỦA AI
    # =====================================================

    def ai_turn(self):

        # AI đang suy nghĩ
        self.ai_thinking = True

        # Hiển thị trạng thái
        self.status.config(
            text="⏳ AI đang suy nghĩ..."
        )

        # Cập nhật giao diện
        self.root.update()

        # ============================================
        # CHẾ ĐỘ COMPARE
        # ============================================

        if self.algorithm == "compare":

            # ----------------------------------------
            # MINIMAX
            # ----------------------------------------

            mini_ai = Agent(self.depth)

            move1 = mini_ai.get_best_move(
                self.board,
                "minimax"
            )

            mini_stats = mini_ai.last_stats

            # ----------------------------------------
            # ALPHA BETA
            # ----------------------------------------

            alpha_ai = Agent(self.depth)

            move2 = alpha_ai.get_best_move(
                self.board,
                "alphabeta"
            )

            alpha_stats = alpha_ai.last_stats

            # ========================================
            # HIỂN THỊ THÔNG TIN SO SÁNH
            # ========================================

            text = ""

            text += "====== MINIMAX ======\n\n"

            text += f"Nước đi: {move1}\n"

            text += f"Depth: {mini_stats['depth']}\n"

            text += f"Time: {mini_stats['duration']}s\n"

            text += f"Nodes: {mini_stats['nodes']}\n"

            text += f"Speed: {mini_stats['speed']} n/s\n\n"

            text += "====== ALPHABETA ======\n\n"

            text += f"Nước đi: {move2}\n"

            text += f"Depth: {alpha_stats['depth']}\n"

            text += f"Time: {alpha_stats['duration']}s\n"

            text += f"Nodes: {alpha_stats['nodes']}\n"

            text += f"Speed: {alpha_stats['speed']} n/s"

            # Hiển thị panel
            self.info.config(text=text)

            # AI dùng AlphaBeta để đánh thật
            move = move2

        # ============================================
        # CHẾ ĐỘ THƯỜNG
        # ============================================

        else:

            move = self.agent.get_best_move(

                self.board,

                self.algorithm
            )

            # Lấy thống kê
            s = self.agent.last_stats

            # Hiển thị thông tin
            text = ""

            text += f"Thuật toán: {s['algorithm']}\n\n"

            text += f"Nước đi: {s['move']}\n"

            text += f"Điểm: {s['score']}\n"

            text += f"Depth: {s['depth']}\n\n"

            text += f"Time: {s['duration']}s\n"

            text += f"Nodes: {s['nodes']}\n"

            text += f"Speed: {s['speed']} n/s"

            self.info.config(text=text)

        # ============================================
        # AI ĐÁNH
        # ============================================

        if move:

            self.board.make_move(

                move[0],
                move[1],
                'O'
            )

        # Vẽ lại bàn cờ
        self.draw_board()

        # ============================================
        # KIỂM TRA AI THẮNG
        # ============================================

        if self.board.check_winner() == 'O':

            self.game_over = True

            messagebox.showinfo(
                "Kết quả",
                "😢 AI THẮNG!"
            )

            return

        # ============================================
        # KIỂM TRA HÒA
        # ============================================

        if self.board.is_full():

            self.game_over = True

            messagebox.showinfo(
                "Kết quả",
                "🤝 HÒA!"
            )

            return

        # ============================================
        # TRẢ LƯỢT CHO NGƯỜI CHƠI
        # ============================================

        self.status.config(
            text="Lượt của bạn"
        )

        self.ai_thinking = False

    # =====================================================
    # CHƠI LẠI
    # =====================================================

    def restart(self):

        # Xóa toàn bộ widget
        for widget in self.root.winfo_children():
            widget.destroy()

        # Mở lại game
        GameGUI(

            self.root,

            self.algorithm,

            self.depth,

            self.first
        )

    # =====================================================
    # QUAY LẠI MENU
    # =====================================================

    def back_menu(self):

        # Xóa widget
        for widget in self.root.winfo_children():
            widget.destroy()

        # Quay lại menu
        MenuScreen(self.root)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    # Tạo cửa sổ
    root = tk.Tk()

    # Mở menu
    MenuScreen(root)

    # Chạy chương trình
    root.mainloop()                    
