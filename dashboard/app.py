# ================================================================
# Diamonds Exploration
# ================================================================
# Sections:
# 1. Imports
# 2. Reactive Calculations (Filtered Data + Simulated Metric)
# 3. Shiny Express UI (Page, Sidebar, Main Content)
# ================================================================

# ------------------------------------------------
# 1. Imports
# ------------------------------------------------
from shiny.express import ui, input, render
from shiny import reactive
import seaborn as sns
import matplotlib.pyplot as plt
import random

# ------------------------------------------------
# Data Source
# ------------------------------------------------
# Using Seaborn's built-in diamonds dataset
diamonds = sns.load_dataset("diamonds")

# ------------------------------------------------
# 2. Reactive Calculations
# ------------------------------------------------

@reactive.calc
def filtered_data():
    """
    Filter the diamonds dataset based on user inputs.
    This drives all downstream outputs (summary, table, charts).
    """
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
    """
    Simulate a metric that updates every 5 seconds.
    Could represent a live KPI like average market price.
    """
    reactive.invalidate_later(5)  # updates every 5 seconds
    return round(random.uniform(3000, 5000), 2)

# Track history of fake metrics for live histogram
price_history = reactive.value([])

@reactive.effect
@reactive.event(fake_metric)
def _update_price_history():
    """
    Append each new fake metric to history for live histogram.
    Triggered only when fake_metric() produces a new value.
    Keeps only the last 50 values for performance.
    """
    new_value = fake_metric()
    history = price_history.get() + [new_value]
    price_history.set(history[-50:])  # keep last 50 values

# ------------------------------------------------
# 3. Shiny Express UI
# ------------------------------------------------

# --- Page Options ---
ui.page_opts(title="Foster Diamonds Inspection 💎", fillable=True)

# --- Sidebar ---
with ui.sidebar():
    ui.h3("Filters")

    # Cut (single select dropdown)
    ui.input_select(
        "cut",
        "Select cut:",
        choices=diamonds["cut"].unique().tolist(),
        selected="Ideal"
    )

    # Color (multi-select checkbox group)
    ui.input_checkbox_group(
        "color",
        "Select colors:",
        choices=diamonds["color"].unique().tolist(),
        selected=["D", "E", "F"]
    )

    # Price range (slider)
    ui.input_slider(
        "price_range",
        "Price range (USD):",
        min=int(diamonds["price"].min()),
        max=int(diamonds["price"].max()),
        value=(500, 5000),
        step=100
    )

# --- Main Content ---

# Value Box: Render dynamically for simulated avg price
@render.ui
def avg_price_box():
    return ui.value_box(
        value=f"${fake_metric()}",
        title="Avg Price (Simulated)",
        showcase="💰"
    )

# Card: Summary text
with ui.card():
    ui.card_header("Summary 💎")

    @render.text
    def summary_text():
        count = len(filtered_data())
        return f"{count} diamonds match your filters."

# Table: First 10 rows of filtered data (HTML)
@render.ui
def summary_table():
    df = filtered_data().head(10)
    html_table = df.to_html(classes="table table-striped", index=False, border=0)
    return ui.HTML(html_table)

# Chart: Histogram of filtered diamonds price
@render.plot
def price_histogram():
    plt.figure(figsize=(6, 4))
    sns.histplot(filtered_data()["price"], bins=30, kde=False, color="skyblue")
    plt.xlabel("Price (USD)")
    plt.ylabel("Count")
    plt.title("Price Distribution (Filtered Diamonds)")
    return plt.gcf()

# Chart: Scatterplot of carat vs price
@render.plot
def carat_vs_price():
    plt.figure(figsize=(6, 4))
    sns.scatterplot(
        data=filtered_data(),
        x="carat",
        y="price",
        hue="clarity",
        palette="viridis",
        alpha=0.7
    )
    plt.title("Carat vs Price by Clarity")
    return plt.gcf()

# Chart: Live histogram of simulated average prices
@render.plot
def simulated_price_histogram():
    """
    Histogram showing distribution of simulated average prices.
    Updates every 5 seconds alongside the value box.
    """
    plt.figure(figsize=(6, 4))
    data = price_history.get()

    # Handle case where no data yet
    if len(data) == 0:
        return plt.gcf()

    sns.histplot(data, bins=10, color="orange")
    plt.xlabel("Simulated Avg Price (USD)")
    plt.ylabel("Frequency")
    plt.title("Live Histogram of Simulated Avg Prices")
    return plt.gcf()



