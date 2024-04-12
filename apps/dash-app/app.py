import dash
from dash import dcc, html, Input, Output
import pandas as pd
from pathlib import Path
import plotly.graph_objs as go
from plots import (
    plot_score_distribution,
    plot_auc_curve,
    plot_precision_recall_curve,
)

file_path = Path(__file__).parent / "simulated-data.csv"


def load_data():
    out = pd.read_csv(file_path)
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    return out


app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [
                dcc.Dropdown(
                    id="account-dropdown",
                    options=[
                        {"label": "Berge & Berge", "value": "Berge & Berge"},
                        {"label": "Fritsch & Fritsch", "value": "Fritsch & Fritsch"},
                        {"label": "Hintz & Hintz", "value": "Hintz & Hintz"},
                        {"label": "Mosciski and Sons", "value": "Mosciski and Sons"},
                        {"label": "Wolff Ltd", "value": "Wolff Ltd"},
                    ],
                    value="Berge & Berge",  # Default value
                ),
                dcc.Dropdown(
                    id="metric-dropdown",
                    options=[
                        {"label": "ROC Curve", "value": "ROC Curve"},
                        {"label": "Precision-Recall", "value": "Precision-Recall"},
                    ],
                    value="ROC Curve",  # Default value
                ),
            ],
            style={"columnCount": 2},
        ),
        html.Div(
            [
                dcc.Graph(id="metric-plot"),
            ],
            style={"height": "350px"},
        ),
        html.Div(
            [
                dcc.Graph(id="score-dist-plot"),
            ],
            style={"height": "350px"},
        ),
    ]
)


@app.callback(
    Output("metric-plot", "figure"),
    [Input("account-dropdown", "value"), Input("metric-dropdown", "value")],
)
def update_metric_plot(selected_account, selected_metric):
    df_val = load_data()
    df_filt = df_val[df_val["account"] == selected_account]
    if selected_metric == "ROC Curve":
        return plot_auc_curve(
            df_filt,
            "is_electronics",
            "training_score",
        )
    else:
        return plot_precision_recall_curve(df_filt, "is_electronics", "training_score")


@app.callback(Output("score-dist-plot", "figure"), [Input("account-dropdown", "value")])
def update_score_distribution_plot(selected_account):
    df_val = load_data()
    df_filt = df_val[df_val["account"] == selected_account]
    return plot_score_distribution(df_filt)


if __name__ == "__main__":
    app.run_server(debug=True)
