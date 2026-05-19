class Caro:
    """
    Class quản lý bàn cờ Caro
    """

    def __init__(self, size=9):

        # Kích thước bàn cờ
        self.size = size

        # Tạo ma trận bàn cờ
        self.grid = [
            ['.' for _ in range(size)]
            for _ in range(size)
        ]

    # =====================================================
    # KIỂM TRA NƯỚC ĐI HỢP LỆ
    # =====================================================

    def is_valid_move(self, x, y):

        return (

            0 <= x < self.size and

            0 <= y < self.size and

            self.grid[x][y] == '.'
        )

    # =====================================================
    # ĐÁNH CỜ
    # =====================================================

    def make_move(self, x, y, player):

        self.grid[x][y] = player

    # =====================================================
    # UNDO NƯỚC ĐI
    # =====================================================

    def undo_move(self, x, y):

        self.grid[x][y] = '.'

    # =====================================================
    # KIỂM TRA BÀN CỜ ĐẦY
    # =====================================================

    def is_full(self):

        for row in self.grid:

            if '.' in row:
                return False

        return True

    # =====================================================
    # KIỂM TRA THẮNG
    # =====================================================

    def check_winner(self):

        # 4 hướng kiểm tra
        dirs = [

            (1, 0),   # dọc

            (0, 1),   # ngang

            (1, 1),   # chéo chính

            (1, -1)   # chéo phụ
        ]

        # Duyệt toàn bàn cờ
        for x in range(self.size):

            for y in range(self.size):

                p = self.grid[x][y]

                # Bỏ qua ô trống
                if p == '.':
                    continue

                # Kiểm tra từng hướng
                for dx, dy in dirs:

                    count = 1

                    # Đếm liên tiếp
                    for k in range(1, 4):

                        nx = x + dx * k
                        ny = y + dy * k

                        if (

                            0 <= nx < self.size and

                            0 <= ny < self.size and

                            self.grid[nx][ny] == p
                        ):

                            count += 1

                        else:
                            break

                    # Đủ 4 quân -> thắng
                    if count >= 4:
                        return p

        # Chưa ai thắng
        return None
