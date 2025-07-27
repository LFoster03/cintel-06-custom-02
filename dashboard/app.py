# ================================================================
# Diamonds Exploration (Plotly Version with Sparkline)
# ================================================================
from shiny.express import ui, input, render
from shiny import reactive
from shinywidgets import render_plotly
import seaborn as sns
import pandas as pd
import random
import plotly.express as px

# Load diamonds dataset
diamonds = sns.load_dataset("diamonds")

# ------------------------------------------------
# Reactive Calculations
# ------------------------------------------------

@reactive.calc
def filtered_data():
    """Filter diamonds based on user inputs."""
    df = diamonds.copy()

    # Filter by cut
    df = df[df["cut"] == input.cut()]

    # Filter by color
    df = df[df["color"].isin(input.color())]

    # Filter by price range
    min_price, max_price = input.price_range()
    df = df[(df["price"] >= min_price) & (df["price"] <= max_price)]

    return df

@reactive.calc
def fake_metric():
    """Simulate metric (updates every 5 seconds)."""
    reactive.invalidate_later(5)
    return round(random.uniform(3000, 5000), 2)

# Track metric history
price_history = reactive.value([])

@reactive.effect
@reactive.event(fake_metric)
def _update_price_history():
    history = price_history.get() + [fake_metric()]
    price_history.set(history[-50:])  # keep last 50 values

# ------------------------------------------------
# UI
# ------------------------------------------------

ui.page_opts(title="Foster Diamonds Inspection 💎", fillable=True)

with ui.sidebar():
    ui.h3("Filters")

    ui.input_select(
        "cut",
        "Select cut:",
        choices=diamonds["cut"].unique().tolist(),
        selected="Ideal"
    )

    ui.input_checkbox_group(
        "color",
        "Select colors:",
        choices=diamonds["color"].unique().tolist(),
        selected=["D", "E", "F"]
    )

    ui.input_slider(
        "price_range",
        "Price range (USD):",
        min=int(diamonds["price"].min()),
        max=int(diamonds["price"].max()),
        value=(500, 5000),
        step=100
    )

# Value Box
@render.ui
def avg_price_box():
    return ui.value_box(
        value=f"${fake_metric()}",
        title="Avg Price (Simulated)",
        showcase="💰"
    )

# Summary card
with ui.card():
    ui.card_header("Summary 💎")

    @render.text
    def summary_text():
        count = len(filtered_data())
        return f"{count} diamonds match your filters."

# Table
@render.ui
def summary_table():
    df = filtered_data()
    if df.empty:
        return ui.HTML("<p style='color:red;'>No diamonds match your filters.</p>")

    html_table = df.head(10).to_html(classes="table table-striped", index=False, border=0)
    return ui.HTML(html_table)

# Plotly Histogram (Filtered Diamonds)
@render_plotly
def price_histogram():
    df = filtered_data()
    if df.empty:
        return px.histogram(pd.DataFrame({"price": []}))  # empty plot

    fig = px.histogram(df, x="price", nbins=30, title="Price Distribution (Filtered Diamonds)")
    fig.update_layout(xaxis_title="Price (USD)", yaxis_title="Count")
    return fig

# Plotly Scatterplot (Carat vs Price)
@render_plotly
def carat_vs_price():
    df = filtered_data()
    if df.empty:
        return px.scatter(pd.DataFrame({"carat": [], "price": []}))

    fig = px.scatter(
        df,
        x="carat",
        y="price",
        color="clarity",
        title="Carat vs Price by Clarity",
        opacity=0.7
    )
    return fig

# Plotly Histogram (Simulated Prices)
@render_plotly
def simulated_price_histogram():
    data = price_history.get()

    if len(data) == 0:
        return px.histogram(pd.DataFrame({"price": []}))

    fig = px.histogram(
        pd.DataFrame({"Simulated Price": data}),
        x="Simulated Price",
        nbins=10,
        title="Live Histogram of Simulated Avg Prices",
        color_discrete_sequence=["orange"]
    )
    return fig

# Plotly Line Chart (Sparkline for Simulated Price Trend)
@render_plotly
def simulated_price_sparkline():
    data = price_history.get()

    # Handle case where no data yet
    if len(data) == 0:
        return px.line(pd.DataFrame({"Price": []}))

    # Create line chart (sparkline style: minimal axes)
    df = pd.DataFrame({"Index": range(len(data)), "Price": data})
    fig = px.line(df, x="Index", y="Price", title="Live Simulated Price Trend")

    fig.update_layout(
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False),
        margin=dict(l=20, r=20, t=40, b=20),
        height=200
    )

    return fig
