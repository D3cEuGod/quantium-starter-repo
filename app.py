import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px

# Load the formatted data from Task 2
df = pd.read_csv("formatted_output.csv")

# Make sure types are correct
df["Date"] = pd.to_datetime(df["Date"])
df["Sales"] = pd.to_numeric(df["Sales"], errors="coerce")

# Total sales per day across all regions
daily_sales = (
    df.groupby("Date", as_index=False)["Sales"]
    .sum()
    .sort_values("Date")
)

# Create the line chart
fig = px.line(
    daily_sales,
    x="Date",
    y="Sales",
    title="Pink Morsel Sales Over Time",
    labels={
        "Date": "Date",
        "Sales": "Sales"
    }
)

# Mark the price increase date
fig.add_vline(
    x="2021-01-15",
    line_width=2,
    line_dash="dash",
    line_color="red"
)

fig.add_annotation(
    x="2021-01-15",
    y=daily_sales["Sales"].max(),
    text="Price increase: 15 Jan 2021",
    showarrow=True,
    arrowhead=2
)

# Build the Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Soul Foods Pink Morsel Sales Visualiser"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)