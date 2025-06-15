import streamlit as st
import numpy as np

st.title("🟩 オセロゲーム（簡易版）")

BOARD_SIZE = 8
EMPTY, BLACK, WHITE = 0, 1, -1

# 初期盤面
def initialize_board():
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board

# 方向
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),         (0, 1),
              (1, -1),  (1, 0), (1, 1)]

# 石を打てるかチェック
def is_valid_move(board, row, col, player):
    if board[row][col] != EMPTY:
        return False
    for dx, dy in DIRECTIONS:
        x, y = row + dx, col + dy
        found_opponent = False
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if board[x][y] == -player:
                found_opponent = True
            elif board[x][y] == player:
                if found_opponent:
                    return True
                break
            else:
                break
            x += dx
            y += dy
    return False

# 有効な手のリスト
def get_valid_moves(board, player):
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if is_valid_move(board, i, j, player)]

# 石を打つ
def make_move(board, row, col, player):
    board[row][col] = player
    for dx, dy in DIRECTIONS:
        x, y = row + dx, col + dy
        stones_to_flip = []
        while 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            if board[x][y] == -player:
                stones_to_flip.append((x, y))
            elif board[x][y] == player:
                for fx, fy in stones_to_flip:
                    board[fx][fy] = player
                break
            else:
                break
            x += dx
            y += dy
    return board

# 状態保存（Streamlitのセッション）
if "board" not in st.session_state:
    st.session_state.board = initialize_board()
    st.session_state.turn = BLACK  # 黒先（ユーザー）

# 現在の状態表示
st.write(f"あなたの手番（{'●' if st.session_state.turn == BLACK else '○'}）")

# 盤面表示
def render_board(board):
    for i in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE)
        for j in range(BOARD_SIZE):
            cell = board[i][j]
            if cell == BLACK:
                label = "●"
                cols[j].markdown(f"<div style='font-size:30px; text-align:center'>{label}</div>", unsafe_allow_html=True)
            elif cell == WHITE:
                label = "○"
                cols[j].markdown(f"<div style='font-size:30px; text-align:center'>{label}</div>", unsafe_allow_html=True)
            else:
                # 空マスで置けるところだけボタンを表示
                if is_valid_move(board, i, j, st.session_state.turn):
                    if cols[j].button("⬜", key=f"{i}-{j}"):
                        st.session_state.board = make_move(board, i, j, st.session_state.turn)
                        st.session_state.turn *= -1

                        # コンピュータのターン（簡易）
                        comp_moves = get_valid_moves(st.session_state.board, st.session_state.turn)
                        if comp_moves:
                            comp_move = comp_moves[np.random.randint(len(comp_moves))]
                            st.session_state.board = make_move(st.session_state.board, comp_move[0], comp_move[1], st.session_state.turn)
                            st.session_state.turn *= -1
                else:
                    cols[j].markdown("　")  # 空白


render_board(st.session_state.board)

# 勝敗表示
if not get_valid_moves(st.session_state.board, BLACK) and not get_valid_moves(st.session_state.board, WHITE):
    black_score = np.sum(st.session_state.board == BLACK)
    white_score = np.sum(st.session_state.board == WHITE)
    if black_score > white_score:
        st.success(f"あなたの勝ち！ ● {black_score} - ○ {white_score}")
    elif black_score < white_score:
        st.error(f"あなたの負け… ● {black_score} - ○ {white_score}")
    else:
        st.info(f"引き分け ● {black_score} - ○ {white_score}")

# リセットボタン
if st.button("ゲームをリセット"):
    st.session_state.board = initialize_board()
    st.session_state.turn = BLACK
