import math
import time


class Agent:
    """
    Class AI sử dụng:
    - Minimax
    - Alpha-Beta Pruning
    """

    def __init__(self, depth=3):

        # Độ sâu tìm kiếm
        self.depth = depth

        # Quân cờ
        self.ai = 'O'
        self.human = 'X'

        # Đếm số node đã duyệt
        self.nodes = 0

        # Lưu thống kê lần chạy cuối
        self.last_stats = {}

    # =====================================================
    # HÀM ĐÁNH GIÁ TRẠNG THÁI
    # =====================================================

    def evaluate(self, board):

        winner = board.check_winner()

        # AI thắng
        if winner == self.ai:
            return 1000000

        # Người chơi thắng
        if winner == self.human:
            return -1000000

        # Chưa kết thúc -> dùng heuristic
        return self.heuristic(board)

    # =====================================================
    # HEURISTIC
    # =====================================================

    def heuristic(self, board):

        score = 0

        # 4 hướng kiểm tra
        dirs = [
            (1, 0),   # dọc
            (0, 1),   # ngang
            (1, 1),   # chéo chính
            (1, -1)   # chéo phụ
        ]

        # Duyệt toàn bàn cờ
        for x in range(board.size):

            for y in range(board.size):

                # Bỏ qua ô trống
                if board.grid[x][y] == '.':
                    continue

                player = board.grid[x][y]

                # Kiểm tra từng hướng
                for dx, dy in dirs:

                    count = 1
                    block = 0

                    # ======== Đếm xuôi ========

                    nx = x + dx
                    ny = y + dy

                    while (
                        0 <= nx < board.size and
                        0 <= ny < board.size and
                        board.grid[nx][ny] == player
                    ):
                        count += 1
                        nx += dx
                        ny += dy

                    # Nếu bị chặn đầu
                    if (
                        not (0 <= nx < board.size and 0 <= ny < board.size)
                        or board.grid[nx][ny] != '.'
                    ):
                        block += 1

                    # ======== Đếm ngược ========

                    nx = x - dx
                    ny = y - dy

                    while (
                        0 <= nx < board.size and
                        0 <= ny < board.size and
                        board.grid[nx][ny] == player
                    ):
                        count += 1
                        nx -= dx
                        ny -= dy

                    # Nếu bị chặn đầu còn lại
                    if (
                        not (0 <= nx < board.size and 0 <= ny < board.size)
                        or board.grid[nx][ny] != '.'
                    ):
                        block += 1

                    value = 0

                    # ======== TÍNH ĐIỂM ========

                    if count >= 4:

                        value = 1000000

                    elif count == 3:

                        # 3 mở
                        if block == 0:
                            value = 200000

                        # 3 bị chặn 1 đầu
                        elif block == 1:
                            value = 50000

                    elif count == 2:

                        if block == 0:
                            value = 10000

                        elif block == 1:
                            value = 3000

                    elif count == 1:

                        value = 50

                    # AI cộng điểm
                    if player == self.ai:

                        score += value

                    # Người chơi trừ điểm mạnh hơn
                    else:

                        score -= value * 2.2

        return score

    # =====================================================
    # ĐÁNH GIÁ NHANH NƯỚC ĐI
    # =====================================================

    def quick_score(self, board, x, y):

        score = 0

        dirs = [
            (1, 0),
            (0, 1),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in dirs:

            ai_count = 0
            human_count = 0

            # ======== Đếm xuôi ========

            for i in range(1, 4):

                nx = x + dx * i
                ny = y + dy * i

                if (
                    0 <= nx < board.size and
                    0 <= ny < board.size
                ):

                    if board.grid[nx][ny] == self.ai:
                        ai_count += 1

                    elif board.grid[nx][ny] == self.human:
                        human_count += 1

            # ======== Đếm ngược ========

            for i in range(1, 4):

                nx = x - dx * i
                ny = y - dy * i

                if (
                    0 <= nx < board.size and
                    0 <= ny < board.size
                ):

                    if board.grid[nx][ny] == self.ai:
                        ai_count += 1

                    elif board.grid[nx][ny] == self.human:
                        human_count += 1

            # ======== ƯU TIÊN CHẶN ========

            if human_count >= 3:
                score += 100000

            elif human_count == 2:
                score += 20000

            elif human_count == 1:
                score += 1000

            # ======== TẤN CÔNG ========

            if ai_count >= 3:
                score += 80000

            elif ai_count == 2:
                score += 10000

            elif ai_count == 1:
                score += 500

        # Ưu tiên gần trung tâm
        center = board.size // 2

        score -= (
            abs(x - center) +
            abs(y - center)
        ) * 10

        return score

    # =====================================================
    # SINH NƯỚC ĐI
    # =====================================================

    def generate_moves(self, board):

        moves = []

        visited = set()

        # ======== Nếu bàn cờ trống ========

        empty = True

        for row in board.grid:

            if 'X' in row or 'O' in row:
                empty = False
                break

        if empty:

            center = board.size // 2

            return [(center, center)]

        # ======== Chỉ xét gần quân đã đánh ========

        for x in range(board.size):

            for y in range(board.size):

                if board.grid[x][y] != '.':

                    # Quét vùng lân cận
                    for dx in range(-2, 3):

                        for dy in range(-2, 3):

                            nx = x + dx
                            ny = y + dy

                            if (
                                0 <= nx < board.size and
                                0 <= ny < board.size and
                                board.grid[nx][ny] == '.' and
                                (nx, ny) not in visited
                            ):

                                visited.add((nx, ny))

                                score = self.quick_score(
                                    board,
                                    nx,
                                    ny
                                )

                                moves.append(
                                    ((nx, ny), score)
                                )

        # Sắp xếp theo điểm giảm dần
        moves.sort(
            key=lambda x: x[1],
            reverse=True
        )

        # Chỉ lấy top 10
        return [m[0] for m in moves[:10]]

    # =====================================================
    # MINIMAX
    # =====================================================

    def minimax(self, board, depth, maximizing):

        self.nodes += 1

        winner = board.check_winner()

        # Điều kiện dừng
        if (
            depth == 0 or
            winner or
            board.is_full()
        ):

            return self.evaluate(board)

        moves = self.generate_moves(board)

        # ======== MAX ========

        if maximizing:

            best = -math.inf

            for x, y in moves:

                board.make_move(x, y, self.ai)

                val = self.minimax(
                    board,
                    depth - 1,
                    False
                )

                board.undo_move(x, y)

                best = max(best, val)

            return best

        # ======== MIN ========

        else:

            best = math.inf

            for x, y in moves:

                board.make_move(x, y, self.human)

                val = self.minimax(
                    board,
                    depth - 1,
                    True
                )

                board.undo_move(x, y)

                best = min(best, val)

            return best

    # =====================================================
    # ALPHA BETA
    # =====================================================

    def alphabeta(
        self,
        board,
        depth,
        alpha,
        beta,
        maximizing
    ):

        self.nodes += 1

        winner = board.check_winner()

        # Điều kiện dừng
        if (
            depth == 0 or
            winner or
            board.is_full()
        ):

            return self.evaluate(board)

        moves = self.generate_moves(board)

        # ======== MAX ========

        if maximizing:

            value = -math.inf

            for x, y in moves:

                board.make_move(x, y, self.ai)

                value = max(
                    value,
                    self.alphabeta(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        False
                    )
                )

                board.undo_move(x, y)

                alpha = max(alpha, value)

                # Cắt nhánh
                if beta <= alpha:
                    break

            return value

        # ======== MIN ========

        else:

            value = math.inf

            for x, y in moves:

                board.make_move(x, y, self.human)

                value = min(
                    value,
                    self.alphabeta(
                        board,
                        depth - 1,
                        alpha,
                        beta,
                        True
                    )
                )

                board.undo_move(x, y)

                beta = min(beta, value)

                # Cắt nhánh
                if beta <= alpha:
                    break

            return value

    # =====================================================
    # TÌM NƯỚC ĐI TỐT NHẤT
    # =====================================================

    def get_best_move(self, board, algo='alphabeta'):

        # Reset node
        self.nodes = 0

        best_move = None

        best_score = -math.inf

        start = time.time()

        moves = self.generate_moves(board)

        for x, y in moves:

            board.make_move(x, y, self.ai)

            # Nếu thắng ngay
            if board.check_winner() == self.ai:

                board.undo_move(x, y)

                best_move = (x, y)

                best_score = 999999

                break

            # Chạy minimax
            if algo == 'minimax':

                score = self.minimax(
                    board,
                    self.depth - 1,
                    False
                )

            # Chạy alphabeta
            else:

                score = self.alphabeta(
                    board,
                    self.depth - 1,
                    -math.inf,
                    math.inf,
                    False
                )

            board.undo_move(x, y)

            # Chọn nước tốt nhất
            if score > best_score:

                best_score = score

                best_move = (x, y)

        end = time.time()

        duration = round(end - start, 3)

        # Tốc độ duyệt node
        speed = int(
            self.nodes / max(duration, 0.001)
        )

        # Lưu thống kê
        self.last_stats = {

            'algorithm': algo.upper(),

            'move': best_move,

            'score': best_score,

            'nodes': self.nodes,

            'duration': duration,

            'speed': speed,

            'depth': self.depth
        }

        return best_move
