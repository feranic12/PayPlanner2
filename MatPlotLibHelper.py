import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import util
import matplotlib
# matplotlib.use("TkAgg")


class MatPlotLibHelper:
    @staticmethod
    def draw_figure_psg(canvas, figure):
        figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
        figure_canvas_agg.draw()
        figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
        return figure_canvas_agg

    @staticmethod
    def draw_figure_mpl(db_driver):
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        values = util.make_dataset(db_driver)
        fig.add_subplot(111).bar(index, values)
        return fig



