from shiny import App, render, ui
import pandas as pd
from plotnine import ggplot, geom_histogram, labs, aes
import numpy as np

app_ui = ui.page_fluid(
    ui.input_slider("n_rows", "Sample rows", 0, 100, 20),
    ui.row(ui.column(4, ui.output_table("df")), ui.column(8, ui.output_plot("hist"))),
)


def server(input):
    @render.table
    def df():
        rand = np.random.rand(input.n_rows(), 1)
        df = pd.DataFrame(rand, columns=["col_1"])
        return df

    @render.plot
    def hist():
        rand = np.random.rand(input.n_rows(), 1)
        df = pd.DataFrame(rand, columns=["col_1"])
        plot = (
            ggplot(df, aes(x="col_1"))
            + geom_histogram(binwidth=0.1, fill="blue", color="black")
            + labs(x="Random Values", y="Frequency", title="Histogram of Random Data")
        )
        return plot


app = App(app_ui, server)
