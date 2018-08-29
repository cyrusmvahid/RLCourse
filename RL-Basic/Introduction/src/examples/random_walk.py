import numpy as np
import tkinter as tk
import time
import sys


class RandomWalk:
    def __init__(self, start_point=2, transition_matrix=None, string_length=10, target=9, penalty=1):
        self.start_point = start_point
        self.string_length = string_length
        self.target = target
        self.penalty = penalty
        if transition_matrix == None:
             #                     pos  0    1    2    3    4    5    6    7    8    9
            self.transition_matrix = [[0.5, 5.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # pos 0
                                      [0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # pos 1
                                      [0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # pos 2
                                      [0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0], # pos 3
                                      [0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0], # pos 4
                                      [0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0, 0.0], # pos 5
                                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.0, 0.0], # pos 6
                                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5, 0.0], # pos 7
                                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5, 0.0, 0.5], # pos 8
                                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], # pos 9
                                     ]
        else:
            self.transition_matrix = transition_matrix
    def move(self):
        trajectory = []
        current_pos = self.start_point
        while current_pos != self.target:
            legal_moves = np.nonzero(self.transition_matrix[current_pos])
            left = legal_moves[0][0]
            right = legal_moves[0][1]
            leftP = self.transition_matrix[current_pos][left] * self.penalty
            rightP = self.transition_matrix[current_pos][right] * self.penalty
            current_pos = np.random.choice([left, right], 1, [leftP, rightP])[0]
            trajectory.append(current_pos)
        return trajectory




class VisualizeRandomWalk:
    def __init__(self, rw, height=55, width=510, pad=5):
        self.height = height
        self.width = width
        self.pad = pad
        self.rw=rw
        self. master = tk.Tk()
        self.cell_width = (width-2*pad)//rw.string_length
        self.cell_height = height - 10
        self.canvas = self._make_canvas()
        self.sleep = .1

    def _make_canvas(self):
        pad = self.pad
        height = self.height
        width = self.width
        cell_width = self.cell_width
        canvas = tk.Canvas(master=self.master, height=height+50, width=width)
        canvas.pack()
        canvas.create_line(pad, pad, width-pad, pad)
        canvas.create_line(pad, height-pad, width-pad,height-pad)
        for x in range(pad, width+cell_width-pad, cell_width):
            canvas.create_line(x, pad, x, height-pad)
        frame = tk.Frame(master=self.master, height=10, width=50)
        frame.pack()
        tk.Button(master=frame, text="start", command=self.run).pack(side=tk.LEFT)
        tk.Button(master=frame, text="quit", command=sys.exit).pack(side=tk.RIGHT)
        tk.Button(master=frame, text='pause 5 sec', command=self._pause).pack(side=tk.RIGHT)
        canvas.bind('<Double-1>', self._onCanvasClick)
        return canvas


    def _pause(self):
        time.sleep(5)

    def _calc_ccordinate(self, pos):
        pad = self.pad
        #height = self.height
        #width = self.width
        cell_width = self.cell_width
        cell_height = self.cell_height
        top_left = [pos * cell_width + pad + pad, pad + pad]
        buttom_right = [(1 + pos) * cell_width - pad - pad, cell_height]
        return [top_left, buttom_right]

    def _onCanvasClick(self, event):
        self.sleep = (1 if self.sleep==.1 else .1)

    def run(self):
        steps = rw.move()
        oval = self.canvas.create_oval(self._calc_ccordinate(rw.start_point), fill='blue')
        msg = self.canvas.create_text(250, 75, text="current positoin: {}\npolicy: {}".format(rw.start_point, rw.transition_matrix[rw.start_point]))
        for step in steps:
            self.canvas.delete(oval)
            self.canvas.delete(msg)

            si = steps.index(step)
            next_step = (steps[si+1] if (step < 9) else 9)
            next_move = '-'
            if next_step > step:
                next_move = '->'
            elif next_step < step:
                next_move = '<-'
            oval = self.canvas.create_oval(self._calc_ccordinate(step), fill='blue')
            msg = self.canvas.create_text(250, 75, text="current positoin: {}\npolicy: {}\nnext_move: {}".format(step,
                                                                                                                 rw.transition_matrix[step],
                                                                                                                 next_move))
            time.sleep(self.sleep)
            self.canvas.update()





if __name__ == "__main__":
    rw = RandomWalk()
    vr = VisualizeRandomWalk(rw=rw)
    tk.mainloop()