# Foster Diamonds Inspection 💎
## Author: Lindsay Foster
## Date: July 2025
This dashboard explores the Seaborn Diamonds dataset using PyShiny and Plotly.
It allows users to filter diamonds by cut, color, and price range and view interactive charts, tables, and a live simulated KPI with both histogram and sparkline visualizations.

## Features
### Reactive Aspects
@reactive.calc: filtered_data() dynamically updates whenever sidebar inputs change.

All outputs (text, table, plots) depend on this reactive dataset.

### UI Inputs
Cut (Dropdown) – Select a single cut (e.g., Ideal, Premium).

Color (Checkbox Group) – Select multiple color grades.

Price Range (Slider) – Adjust the minimum and maximum diamond price.

### Sidebar Components
Contains all filtering inputs for controlling the dataset.

### Main Content
Summary Card (Text Output) – Shows count of diamonds matching filters.

HTML Table (First 10 Rows) – Displays filtered data without requiring Jinja2.

Histogram (Matplotlib + Seaborn) – Price distribution of filtered diamonds.

Scatterplot (Matplotlib + Seaborn) – Carat vs Price, colored by clarity.

### Dataset
Uses the built-in Seaborn diamonds dataset:

54,000 rows of diamond data

Columns: carat, cut, color, clarity, price, dimensions (x, y, z)

### How It Meets Project Requirements
Reactive calc: filtered_data() used by text, table, and plots.

UI Inputs in Sidebar: Dropdown, checkbox group, slider.

Main Content Outputs: Card with text, table, two charts.

Template: Uses ui.page_opts (basic template, no columns or navigation required).

Visual Enhancements: Emojis added to title and summary for engagement.

### Resources
Dataset
Diamonds dataset (CSV)

Input Component API
ui.input_slider – Shiny Express API

Output Component API (Data)
ui.HTML – Shiny Express API

Output Component API (Charts)
render.plot – Shiny Express API

## Additional Features (Live Simulation)
#### Simulated Metric
A reactive calc fake_metric() generates a random “average price” every 5 seconds to mimic live data.

Displayed in a value box with an emoji: 💰.

Automatically refreshes without user input (demonstrates reactive.invalidate_later()).

#### Live Histogram
Tracks the last 50 simulated metric values using a reactive value price_history.

Uses @reactive.effect combined with @reactive.event(fake_metric) to append new data points only when fake_metric changes (avoiding infinite loops).

Plots a histogram (orange) of simulated price values updating every 5 seconds.

#### How It Works
Reactive Flow

fake_metric() → triggers every 5 seconds.

@reactive.effect listens for changes and appends to price_history.

simulated_price_histogram() renders a histogram of recent values.

Performance Handling

price_history is trimmed to last 50 values to prevent memory bloat or slow rendering.

UI Placement

Value box and live histogram are shown in the main content area alongside filtered data visuals.

#### Project Requirement Highlights
Reactive Aspects:

filtered_data() for user-driven filtering

fake_metric() + price_history for time-driven updates

Multiple Output Types:

Static histogram & scatterplot (filtered diamonds)

Live histogram (simulated metric)

Summary card and HTML table

Demonstrates advanced reactivity:

Combination of reactive.calc, reactive.event, and reactive.value.

#### Helpful API References
Reactive calc: reactive.calc()

Reactive effect/event: reactive.effect() and reactive.event()

Value box: ui.value_box()

Plot output: render.plot()


### Updated Features:

Live Sparkline: Minimal line chart showing real-time trend of simulated prices.
Enhancements

Plotly Interactive Charts

Replaced Matplotlib/Seaborn with Plotly for zoom, pan, and hover tooltips.

Allows users to export plots as images directly from the interface.

Empty Dataset Handling

Gracefully shows “No diamonds match your filters” message if no data matches filters.

Prevents errors when filters return 0 rows.

Live Sparkline Trend

Added minimalist line chart for real-time KPI trend.

Complements live histogram for better understanding of simulated metric.

How It Works
Reactive Design

filtered_data() updates whenever filter inputs change.

fake_metric() generates random price values every 5 seconds.

price_history stores the last 50 simulated values for histogram and sparkline.

All charts and tables reactively update based on these reactive values.
