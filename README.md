# Coffee Sales Analysis

Meet your go-to sales cockpit for coffee shops. This Streamlit app turns the raw `Coffee Shop Sales.csv` file into interactive KPIs, time-series trends, category leaders, and downloadable reports - perfect for demos, stakeholders, or rapid what-if analysis.

---

## Why You'll Love Exploring It

- Executive KPIs - total revenue, transactions, top category, and peak hour in a slick KPI grid.
- Time Travel - hourly line trends plus daily/monthly bar charts to spot busy shifts or slow seasons.
- Product Insights - compare product categories, drill into the top 5 sellers, or view average ticket sizes.
- Store Showdown - benchmark each store location's revenue with sortable bars.
- Instant Export - download whatever you filter to Excel with one click.
- Cafe-Themed UI - custom CSS delivers cozy colors, hover effects, and responsive layouts.

---

## Tech Stack

- Python 3.11+
- Streamlit for the UI
- Pandas for wrangling
- Plotly Express for interactive charts
- OpenPyXL for Excel export

All dependencies live in `prerequisites.txt`, so a single `pip install -r prerequisites.txt` gets you ready.

---

## Dataset

The provided `Coffee Shop Sales.csv` includes:

- Temporal fields (`Month`, `Day`, `Hour`)
- Product metadata (`product_category`, `store_location`, `transaction_id`)
- Pricing columns (`unit_price`, `transaction_qty`)
- Derived `total_sales` calculated in-app

Swap in your own data by keeping the same column names (or tweak `app.py`).

---

## Quickstart

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/coffee-sales-dashboard.git
cd coffee-sales-dashboard
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS/Linux
```

### 3. Install prerequisites

```bash
pip install -r prerequisites.txt
```

### 4. Run the Streamlit app

```bash
python -m streamlit run app.py
```

Streamlit prints the local and network URLs (default `http://localhost:8501`). Add `--server.headless true` when deploying remotely.

---

## Dashboard Walkthrough
<img width="1920" height="1080" alt="Screenshot (86)" src="https://github.com/user-attachments/assets/856d2776-646d-4e09-b14a-4f399684a240" />
<img width="1920" height="1080" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/8b1495f3-b3d6-4c52-bf86-5709dd232c19" />
<img width="1920" height="1080" alt="Screenshot (88)" src="https://github.com/user-attachments/assets/ac2cf4f7-a358-4acd-8d23-bf5ba4e7d550" />
<img width="1920" height="1080" alt="Screenshot (89)" src="https://github.com/user-attachments/assets/9e0c10d7-121a-4e1e-a525-fc37e4fff8d8" />

1. Sidebar Filters - choose months, categories, and locations; reset anytime.
2. KPI Grid - compare filtered metrics vs overall totals.
3. Time Analysis - hourly line chart plus daily/monthly bars.
4. Product & Category Panels - horizontal bars and donut charts to rank what's selling.
5. Average Sales Section - understand ticket sizes by hour, day, and category.
6. Store Leaderboard - highlight best-performing locations.
7. Export Drawer - download the filtered dataframe as Excel.

---

## Contributing

1. Fork, then create a feature branch.
2. Make your improvements (new charts, themes, filters, etc.).
3. Run `python -m streamlit run app.py` to test.
4. Open a pull request with screenshots or Loom clips.

---

## Feedback

Ideas for new visualizations? Found a bug? Open an issue or reach out on GitHub - always happy to chat over a virtual cup of coffee.


