import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Load data
df = pd.read_csv("formatted_output.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")
df["Region"] = df["Region"].str.lower()

app = Dash(__name__)

app.layout = html.Div(
    className="app-container",
    children=[
        html.H1("Soul Foods Pink Morsel Sales Visualiser", className="main-title"),

        html.Div(
            className="controls-card",
            children=[
                html.Label("Filter by region:", className="control-label"),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "All", "value": "all"},
                        {"label": "North", "value": "north"},
                        {"label": "East", "value": "east"},
                        {"label": "South", "value": "south"},
                        {"label": "West", "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    className="radio-group",
                    inputClassName="radio-input",
                    labelClassName="radio-label",
                ),
            ],
        ),

        html.Div(
            className="chart-card",
            children=[
                dcc.Graph(id="sales-chart")
            ],
        ),
    ],
)


@app.callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value")
)
def update_chart(selected_region):
    filtered_df = df.copy()

    if selected_region != "all":
        filtered_df = filtered_df[filtered_df["Region"] == selected_region]

    daily_sales = (
        filtered_df.groupby("Date", as_index=False)["Sales"]
        .sum()
        .sort_values("Date")
    )

    region_title = "All Regions" if selected_region == "all" else selected_region.capitalize()

    fig = px.line(
        daily_sales,
        x="Date",
        y="Sales",
        title=f"Pink Morsel Sales Over Time - {region_title}",
        labels={"Date": "Date", "Sales": "Sales"},
        markers=True
    )

    fig.add_vline(
        x="2021-01-15",
        line_width=2,
        line_dash="dash",
        line_color="red"
    )

    fig.add_annotation(
        x="2021-01-15",
        y=daily_sales["Sales"].max() if not daily_sales.empty else 0,
        text="Price increase: 15 Jan 2021",
        showarrow=True,
        arrowhead=2
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        title_x=0.5
    )

    fig.update_xaxes(showgrid=True, gridcolor="#e5e7eb")
    fig.update_yaxes(showgrid=True, gridcolor="#e5e7eb")

    return fig


if __name__ == "__main__":
    app.run(debug=True)