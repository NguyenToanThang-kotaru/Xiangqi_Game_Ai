from tkinter import *
import config_font
def create_board(main_window):
    CELL_SIZE = 40
    def create_broad(canvas):
        for col in range(9):
            x = (col + 1) * CELL_SIZE
            if col == 0 or col == 8:
                canvas.create_line(x, CELL_SIZE, x, 10*CELL_SIZE, width=2, fill="#FF3399")
            else:
                canvas.create_line(x, CELL_SIZE, x, 5*CELL_SIZE, width=2,fil="#FF3399")
                canvas.create_line(x, 6*CELL_SIZE, x, 10*CELL_SIZE, width=2,fill="#FF3399")
        for row in range(10):
            y = (row + 1) * CELL_SIZE
            canvas.create_line(CELL_SIZE, y, CELL_SIZE * 9, y, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE, CELL_SIZE*6, CELL_SIZE*3, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*3, CELL_SIZE*6, CELL_SIZE, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*8, CELL_SIZE*6, CELL_SIZE*10, width=2,fill="#FF3399")
        canvas.create_line(CELL_SIZE*4, CELL_SIZE*10, CELL_SIZE*6, CELL_SIZE*8, width=2,fill="#FF3399")

    board = Toplevel()
    config_font.center_window(board, 800, 440)
    board.configure(bg="#333333")
    board.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(board,main_window))
    board.title("Xiangqi")
    canvas = Canvas(board, height=400, width=400,highlightthickness=0)
    canvas.configure(bg="#333333")
    canvas.pack()
    create_broad(canvas)

    # board.mainloop()
    # board = Toplevel()
    # config_font.center_window(board, 800, 440)
    # board.configure(bg="#333333")
    # board.protocol("WM_DELETE_WINDOW", lambda: config_font.close_all(board,main_window))
    # board.title("Xiangqi")
    # canvas = Canvas(board, height=400, width=400,highlightthickness=0)
    # canvas.configure(bg="#333333")
    # canvas.pack()
    # create_broad(canvas)

    # board.mainloop()
