import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    def draw_figure_mpl():
        fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
        index = ["окт 2020", "ноя 2020", "дек 2020", "янв 2021", "фев 2021"]
        values = [5, 7, 3, 4, 6]
        fig.add_subplot(111).bar(index, values)
        return fig



