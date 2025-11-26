import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Set page configuration
st.set_page_config(
    page_title="Coffee Shop Sales Dashboard",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS
st.markdown("""
    <style>
    :root {
        --coffee-dark: #4A3C32;
        --coffee-medium: #6F4E37;
        --coffee-light: #B87E5F;
        --coffee-cream: #DAC7B7;
        --coffee-bg: #FDF6F0;
    }
    
    .main {
        padding: 0rem 1rem;
        background-color: var(--coffee-bg);
    }
    
    .stPlotlyChart {
        background-color: white;
        border-radius: 10px;
        padding: 0.5rem;
        margin-bottom: 0;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stPlotlyChart:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .dashboard-title {
        color: var(--coffee-dark);
        font-size: 2.2rem;
        text-align: center;
        margin: 1.5rem 0 2.5rem 0;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .kpi-box {
        background-color: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid var(--coffee-cream);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .kpi-box:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 2rem;
    }
    
    .kpi-item {
        text-align: center;
        padding: 1.5rem;
        border-radius: 8px;
        background-color: var(--coffee-bg);
        transition: all 0.3s ease;
        border: 1px solid var(--coffee-cream);
    }
    
    .kpi-item:hover {
        background-color: white;
        transform: scale(1.02);
        border-color: var(--coffee-medium);
    }
    
    .kpi-label {
        color: var(--coffee-medium);
        font-size: 1.1rem;
        margin-bottom: 0.8rem;
        font-weight: 500;
    }
    
    .kpi-value {
        color: var(--coffee-dark);
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
    
    .kpi-delta {
        font-size: 0.9rem;
        color: var(--coffee-light);
        font-weight: 500;
    }
    
    .section-title {
        color: var(--coffee-dark);
        font-size: 1.6rem;
        margin: 2.5rem 0 1.5rem 0;
        padding-bottom: 0.8rem;
        font-weight: 600;
        border-bottom: 2px solid var(--coffee-cream);
    }
    
    .graph-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid var(--coffee-cream);
        margin-bottom: 2rem;
        transition: all 0.3s ease;
    }
    
    .graph-container:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    .stSidebar {
        background-color: var(--coffee-bg);
        padding: 2rem 1rem;
    }
    
    .filter-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
        border: 1px solid var(--coffee-cream);
    }
    
    .filter-title {
        color: var(--coffee-dark);
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--coffee-cream);
    }
    
    .stButton > button {
        background-color: var(--coffee-medium);
        color: white;
        width: 100%;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: var(--coffee-dark);
        transform: translateY(-2px);
    }
    
    /* Fix for plotly graph containers */
    [data-testid="column"] > div:has(> .stPlotlyChart) {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid var(--coffee-cream);
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
        height: fit-content;
    }
    
    [data-testid="column"] > div:has(> .stPlotlyChart):hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

# Load data with caching
@st.cache_data
def load_data():
    df = pd.read_csv("Coffee Shop Sales.csv")
    df['total_sales'] = df['transaction_qty'] * df['unit_price']
    return df

# Download function
def get_download_link(df, filename):
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False)
    excel_buffer.seek(0)
    return excel_buffer

# Load the data
df = load_data()

# Initialize session state for filters if not exists
if 'months_filter' not in st.session_state:
    st.session_state.months_filter = sorted(df["Month"].unique())
if 'categories_filter' not in st.session_state:
    st.session_state.categories_filter = sorted(df["product_category"].unique())
if 'locations_filter' not in st.session_state:
    st.session_state.locations_filter = sorted(df["store_location"].unique())

# Sidebar Filters
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h2 style='color: #1a1f36; font-size: 1.5rem; margin-bottom: 0.5rem;'>☕ Filter Options</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='filter-title'>📅 Time Period</div>", unsafe_allow_html=True)
    selected_months = st.multiselect(
        "Select months",
        options=sorted(df["Month"].unique()),
        default=st.session_state.months_filter,
        key="months_filter"
    )

    st.markdown("<div class='filter-title'>🛍️ Product Categories</div>", unsafe_allow_html=True)
    selected_categories = st.multiselect(
        "Select categories",
        options=sorted(df["product_category"].unique()),
        default=st.session_state.categories_filter,
        key="categories_filter"
    )

    st.markdown("<div class='filter-title'>📍 Store Locations</div>", unsafe_allow_html=True)
    selected_locations = st.multiselect(
        "Select locations",
        options=sorted(df["store_location"].unique()),
        default=st.session_state.locations_filter,
        key="locations_filter"
    )

    # Check if any filter is empty
    if not selected_months or not selected_categories or not selected_locations:
        st.error("⚠️ Please select at least one option for each filter!")

    if st.button("Reset Filters", use_container_width=True):
        st.session_state.months_filter = sorted(df["Month"].unique())
        st.session_state.categories_filter = sorted(df["product_category"].unique())
        st.session_state.locations_filter = sorted(df["store_location"].unique())
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Filter the dataframe only if all filters have at least one selection
if selected_months and selected_categories and selected_locations:
    filtered_df = df[
        (df["Month"].isin(selected_months)) &
        (df["product_category"].isin(selected_categories)) &
        (df["store_location"].isin(selected_locations))
    ]
else:
    filtered_df = pd.DataFrame()  # Empty dataframe if any filter is empty

# Add Download Button after filtered_df is created
with st.sidebar:
    st.markdown("<div class='filter-title'>📥 Export Data</div>", unsafe_allow_html=True)
    excel_buffer = get_download_link(filtered_df, "coffee_shop_sales.xlsx")
    st.download_button(
        label="Download Filtered Data",
        data=excel_buffer,
        file_name="coffee_shop_sales.xlsx",
        mime="application/vnd.ms-excel",
        use_container_width=True,
    )
    
    # Show filter summary
    st.markdown("<div class='filter-title'>📊 Filter Summary</div>", unsafe_allow_html=True)
    st.markdown(f"""
        <div style='font-size: 0.9rem; color: #666;'>
        • Selected Months: {len(selected_months)}<br>
        • Selected Categories: {len(selected_categories)}<br>
        • Selected Locations: {len(selected_locations)}<br>
        • Filtered Rows: {len(filtered_df):,}
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Main Content
st.markdown("""
    <div class='dashboard-title'>
        ☕ Coffee Shop Sales Analytics
    </div>
""", unsafe_allow_html=True)

# KPI Metrics
if not filtered_df.empty:
    total_sales = filtered_df['total_sales'].sum()
    total_sales_change = ((total_sales / df['total_sales'].sum()) - 1) * 100
    total_transactions = filtered_df['transaction_id'].nunique()
    trans_change = ((total_transactions / df['transaction_id'].nunique()) - 1) * 100
    top_category = filtered_df.groupby("product_category")["total_sales"].sum().idxmax()
    overall_top = df.groupby("product_category")["total_sales"].sum().idxmax()
    peak_hour = filtered_df.groupby("Hour")["total_sales"].sum().idxmax()
    overall_peak = df.groupby("Hour")["total_sales"].sum().idxmax()

    st.markdown("""
        <div class="kpi-box">
            <div class="kpi-grid">
                <div class="kpi-item">
                    <div class="kpi-label">Total Revenue</div>
                    <div class="kpi-value">$""" + f"{total_sales:,.2f}" + """</div>
                    <div class="kpi-delta">""" + f"{total_sales_change:+.1f}% vs total" + """</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Total Transactions</div>
                    <div class="kpi-value">""" + f"{total_transactions:,}" + """</div>
                    <div class="kpi-delta">""" + f"{trans_change:+.1f}% vs total" + """</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Top Category</div>
                    <div class="kpi-value">""" + f"{top_category}" + """</div>
                    <div class="kpi-delta">""" + ("Same as overall" if top_category == overall_top else "Changed") + """</div>
                </div>
                <div class="kpi-item">
                    <div class="kpi-label">Peak Hour</div>
                    <div class="kpi-value">""" + f"{peak_hour}:00" + """</div>
                    <div class="kpi-delta">""" + ("Same as overall" if peak_hour == overall_peak else "Changed") + """</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Time Analysis
    st.markdown("<div class='section-title'>⏰ Time-based Analysis</div>", unsafe_allow_html=True)
    
    # Hourly Analysis
    hourly_sales = filtered_df.groupby("Hour")["total_sales"].sum()
    fig_hourly = px.line(
        x=hourly_sales.index,
        y=hourly_sales.values,
        title="Hourly Sales Trend",
        labels={"x": "Hour of Day", "y": "Total Sales ($)"},
        markers=True,
        height=400  # Set fixed height
    )
    fig_hourly.update_traces(
        line_color='#6F4E37',
        marker=dict(size=8, color='#4A3C32'),
        hovertemplate="Hour: %{x}:00<br>Sales: $%{y:,.2f}"
    )
    fig_hourly.update_layout(
        plot_bgcolor='rgba(253, 246, 240, 0.5)',
        paper_bgcolor='white',
        hovermode='x unified',
        margin=dict(l=50, r=20, t=50, b=50)  # Adjust margins
    )
    st.plotly_chart(fig_hourly, use_container_width=True)

    # Daily and Monthly Analysis
    col1, col2 = st.columns(2)
    
    with col1:
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_sales = filtered_df.groupby("Day")["total_sales"].sum().reindex(day_order)
        fig_daily = px.bar(
            x=daily_sales.index,
            y=daily_sales.values,
            title="Daily Sales Distribution",
            labels={"x": "Day", "y": "Sales ($)"},
            color_discrete_sequence=['#6F4E37'],
            height=350  # Set fixed height
        )
        fig_daily.update_traces(marker_color='#6F4E37')
        fig_daily.update_layout(
            title_font_color='#4A3C32',
            plot_bgcolor='rgba(253, 246, 240, 0.5)',
            paper_bgcolor='white',
            margin=dict(l=50, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_daily, use_container_width=True)

    with col2:
        monthly_order = ['January', 'February', 'March', 'April', 'May', 'June']
        monthly_sales = filtered_df.groupby("Month")["total_sales"].sum().reindex(monthly_order)
        fig_monthly = px.bar(
            x=monthly_sales.index,
            y=monthly_sales.values,
            title="Monthly Sales Distribution",
            labels={"x": "Month", "y": "Sales ($)"},
            color_discrete_sequence=['#B87E5F'],
            height=350  # Set fixed height
        )
        fig_monthly.update_traces(marker_color='#B87E5F')
        fig_monthly.update_layout(
            title_font_color='#4A3C32',
            plot_bgcolor='rgba(253, 246, 240, 0.5)',
            paper_bgcolor='white',
            margin=dict(l=50, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_monthly, use_container_width=True)

    # Product Analysis
    st.markdown("<div class='section-title'>🛍️ Product Analysis</div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        category_sales = filtered_df.groupby("product_category")["total_sales"].sum().sort_values(ascending=True)
        fig_category = px.bar(
            x=category_sales.values,
            y=category_sales.index,
            orientation='h',
            title="Sales by Category",
            labels={"x": "Sales ($)", "y": "Category"},
            color_discrete_sequence=['#8B4513'],
            height=350  # Set fixed height
        )
        fig_category.update_traces(marker_color='#8B4513')
        fig_category.update_layout(
            title_font_color='#4A3C32',
            plot_bgcolor='rgba(253, 246, 240, 0.5)',
            paper_bgcolor='white',
            margin=dict(l=150, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_category, use_container_width=True)

    with col2:
        top5_categories = filtered_df.groupby("product_category")["total_sales"].sum().sort_values(ascending=False).head(5)
        fig_pie = px.pie(
            values=top5_categories.values,
            names=top5_categories.index,
            title="Top 5 Product Categories",
            hole=0.4,
            height=350  # Set fixed height
        )
        fig_pie.update_traces(marker=dict(colors=['#6F4E37', '#8B4513', '#B87E5F', '#4A3C32', '#DAC7B7']))
        fig_pie.update_layout(
            title_font_color='#4A3C32',
            paper_bgcolor='white',
            margin=dict(l=20, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Average Sales Analysis
    st.markdown("<div class='section-title'>📈 Average Sales Analysis</div>", unsafe_allow_html=True)
    
    # Average Sales by Hour
    avg_hour_sales = filtered_df.groupby("Hour")["total_sales"].mean()
    fig_avg_hourly = px.line(
        x=avg_hour_sales.index,
        y=avg_hour_sales.values,
        title="Average Sales by Hour",
        labels={"x": "Hour of Day", "y": "Average Sales ($)"},
        markers=True,
        height=400  # Set fixed height
    )
    fig_avg_hourly.update_traces(
        line_color='#B87E5F',
        marker=dict(size=8, color='#4A3C32'),
        hovertemplate="Hour: %{x}:00<br>Avg Sales: $%{y:,.2f}"
    )
    fig_avg_hourly.update_layout(
        plot_bgcolor='rgba(253, 246, 240, 0.5)',
        paper_bgcolor='white',
        margin=dict(l=50, r=20, t=50, b=50)  # Adjust margins
    )
    st.plotly_chart(fig_avg_hourly, use_container_width=True)

    # Average Sales by Day and Category
    col1, col2 = st.columns(2)
    
    with col1:
        avg_day_sales = filtered_df.groupby("Day")["total_sales"].mean().reindex(day_order)
        fig_avg_daily = px.bar(
            x=avg_day_sales.index,
            y=avg_day_sales.values,
            title="Average Sales by Day",
            labels={"x": "Day", "y": "Average Sales ($)"},
            color_discrete_sequence=['#6F4E37'],
            height=350  # Set fixed height
        )
        fig_avg_daily.update_traces(marker_color='#6F4E37')
        fig_avg_daily.update_layout(
            title_font_color='#4A3C32',
            plot_bgcolor='rgba(253, 246, 240, 0.5)',
            paper_bgcolor='white',
            margin=dict(l=50, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_avg_daily, use_container_width=True)

    with col2:
        avg_category_sales = filtered_df.groupby("product_category")["total_sales"].mean().sort_values(ascending=True)
        fig_avg_category = px.bar(
            x=avg_category_sales.values,
            y=avg_category_sales.index,
            orientation='h',
            title="Average Sales by Category",
            labels={"x": "Average Sales ($)", "y": "Category"},
            color_discrete_sequence=['#8B4513'],
            height=350  # Set fixed height
        )
        fig_avg_category.update_traces(marker_color='#8B4513')
        fig_avg_category.update_layout(
            title_font_color='#4A3C32',
            plot_bgcolor='rgba(253, 246, 240, 0.5)',
            paper_bgcolor='white',
            margin=dict(l=150, r=20, t=50, b=50)  # Adjust margins
        )
        st.plotly_chart(fig_avg_category, use_container_width=True)

    # Store Location Analysis
    st.markdown("<div class='section-title'>📍 Store Location Analysis</div>", unsafe_allow_html=True)
    location_sales = filtered_df.groupby("store_location")["total_sales"].sum().sort_values(ascending=True)
    fig_location = px.bar(
        x=location_sales.values,
        y=location_sales.index,
        orientation='h',
        title="Sales by Store Location",
        labels={"x": "Total Sales ($)", "y": "Location"},
        color_discrete_sequence=['#6F4E37'],
        height=350  # Set fixed height
    )
    fig_location.update_traces(marker_color='#6F4E37')
    fig_location.update_layout(
        title_font_color='#4A3C32',
        plot_bgcolor='rgba(253, 246, 240, 0.5)',
        paper_bgcolor='white',
        margin=dict(l=150, r=20, t=50, b=50)  # Adjust margins
    )
    st.plotly_chart(fig_location, use_container_width=True)

else:
    st.warning("No data available for the selected filters. Please adjust your selection.")
