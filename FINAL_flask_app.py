from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import datetime as dt
import psycopg2
from config import DB_CONFIG   # your database config


# -------------------------------------------------------------
# LOAD DATA FROM POSTGRES
# -------------------------------------------------------------
def load_data():
    pg_string = (
        f"host={DB_CONFIG['host']} "
        f"port={DB_CONFIG['port']} "
        f"dbname={DB_CONFIG['dbname']} "
        f"user={DB_CONFIG['user']} "
        f"password={DB_CONFIG['password']}"
    )

    conn = psycopg2.connect(pg_string)
    query = "SELECT * FROM data_daily;"
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["salesdate"] = pd.to_datetime(df["salesdate"], errors="coerce")
    return df


# -------------------------------------------------------------
# KPI CARD COMPONENT
# -------------------------------------------------------------
def kpi_card(title, value):
    return html.Div(
        style={
            "backgroundColor": "white",
            "padding": "20px",
            "borderRadius": "8px",
            "width": "22%",
            "textAlign": "center",
            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
        },
        children=[html.H4(title), html.H2(value, style={"color": "#c21299"})],
    )


# -------------------------------------------------------------
# DASH APP SETUP
# -------------------------------------------------------------
app = Dash(name="Sales_Dashboard")


# -------------------------------------------------------------
# LAYOUT WITH FILTERS + KPI + VISUALS
# -------------------------------------------------------------
def serve_layout():

    df = load_data()

    # KPIs
    total_items = df["itemssold"].sum()
    avg_discount = df["discount"].mean().round(2)
    free_ship_rate = f"{df['freeship'].mean() * 100:.2f}%"

    last_date = df["salesdate"].max()
    days_old = (pd.Timestamp.today().date() - last_date.date()).days
    pipeline_status = "Pipeline Fresh" if days_old <= 1 else "Pipeline Stale"

    return html.Div(
        style={"padding": "20px", "font-family": "Arial, sans-serif"},
        children=[

            # HEADER
            html.Div(
                style={
                    "backgroundColor": "#c21299",
                    "padding": "15px",
                    "borderRadius": "6px",
                    "color": "white",
                    "marginBottom": "20px",
                },
                children=[html.H1("Sales Monitoring Dashboard", style={"textAlign": "center"})],
            ),

            html.Div(f"Data last loaded on: {last_date.date()}", style={"textAlign": "center"}),
            html.Div(f"Pipeline Status: {pipeline_status}", style={"textAlign": "center"}),
            html.Br(),

            # KPIs
            html.Div(
                style={"display": "flex", "justifyContent": "space-around"},
                children=[
                    kpi_card("Total Items Sold", f"{total_items:,}"),
                    kpi_card("Average Discount", avg_discount),
                    kpi_card("Free Shipping Rate", free_ship_rate),
                ],
            ),

            html.Br(),

            # FILTERS
            html.Div(
                style={
                    "backgroundColor": "white",
                    "padding": "15px",
                    "borderRadius": "8px",
                    "marginBottom": "20px",
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "width": "40%",
                },
                children=[
                    html.H4("Filters"),
                    html.Label("Region:"),
                    dcc.Dropdown(
                        id="region-filter",
                        options=[{"label": r.upper(), "value": r} for r in sorted(df["region"].unique())],
                        value=None,
                        clearable=True,
                    ),
                    html.Br(),
                    html.Label("Product ID:"),
                    dcc.Dropdown(
                        id="product-filter",
                        options=[{"label": p, "value": p} for p in sorted(df["productid"].unique())],
                        value=None,
                        clearable=True,
                    ),
                ],
            ),

            # VISUALIZATIONS
            dcc.Graph(id="items-trend"),
            dcc.Graph(id="region-product-bar"),
            dcc.Graph(id="productid-items-bar"),
        ],
    )

app.layout = serve_layout


# -------------------------------------------------------------
# CALLBACKS — 3 NEW VISUALIZATIONS
# -------------------------------------------------------------

@app.callback(
    Output("items-trend", "figure"),
    Output("region-product-bar", "figure"),
    Output("productid-items-bar", "figure"),
    Input("region-filter", "value"),
    Input("product-filter", "value"),
)
def update_graphs(region, product):

    df = load_data()

    if region:
        df = df[df["region"] == region]

    if product:
        df = df[df["productid"] == product]

    # ---------------------------------------------------------
    # 1. LINE CHART: Items Sold Over Time (LIGHT PINK)
    # ---------------------------------------------------------
    trend = df.groupby("salesdate")["itemssold"].sum().reset_index()

    fig_trend = px.line(
        trend,
        x="salesdate",
        y="itemssold",
        title="Daily Items Sold Over Time",
        markers=True,
    )
    fig_trend.update_traces(line=dict(color="#ffc6e5"), marker=dict(color="#ffc6e5", size=8))
    fig_trend.update_layout(
        xaxis_title="Sales Date",
        yaxis_title="Items Sold",
        plot_bgcolor="white"
    )

    # ---------------------------------------------------------
    # 2. BAR CHART: Sales by Region (HOT PINK)
    # ---------------------------------------------------------
    region_sales = df.groupby("region")["itemssold"].sum().reset_index()

    fig_bar = px.bar(
        region_sales,
        x="region",
        y="itemssold",
        title="Sales by Region",
        text_auto=True
    )
    fig_bar.update_traces(marker_color="#ff4fa3")
    fig_bar.update_layout(
        xaxis_title="Region",
        yaxis_title="Items Sold",
        plot_bgcolor="white"
    )

    # ---------------------------------------------------------
    # 3. BAR CHART: Product ID vs Items Sold (YOUR PINK)
    # ---------------------------------------------------------
    prod_sales = df.groupby("productid")["itemssold"].sum().reset_index()

    fig_bar2 = px.bar(
        prod_sales,
        x="productid",
        y="itemssold",
        title="Product ID vs Items Sold",
        text_auto=True
    )
    fig_bar2.update_traces(marker_color="#c21299")
    fig_bar2.update_layout(
        xaxis_title="Product ID",
        yaxis_title="Items Sold",
        plot_bgcolor="white"
    )

    return fig_trend, fig_bar, fig_bar2


# -------------------------------------------------------------
# RUN SERVER
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
