import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Website Conversion Rate Dashboard", page_icon="📊", layout="wide")

# Dashboard title
st.title("Website Conversion Rate Optimization Dashboard")
st.markdown("Analyze website performance to identify optimization opportunities.")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("website_analytics.csv")
    df["conversions"] = df["conversions"].fillna(0)
    df["sessions"] = df["sessions"].replace(0, 1)  # Avoid division by zero
    df["conversionRate"] = df["conversions"] / df["sessions"] * 100
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filters")
page_filter = st.sidebar.multiselect("Select Page(s)", options=df["pagePath"].unique(), default=df["pagePath"].unique())
device_filter = st.sidebar.multiselect("Select Device(s)", options=df["deviceCategory"].unique(), default=df["deviceCategory"].unique())
source_filter = st.sidebar.multiselect("Select Source(s)", options=df["sourceMedium"].unique(), default=df["sourceMedium"].unique())

# Filter data
filtered_df = df[
    (df["pagePath"].isin(page_filter)) &
    (df["deviceCategory"].isin(device_filter)) &
    (df["sourceMedium"].isin(source_filter))
]

# KPIs
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)
avg_conversion = filtered_df["conversionRate"].mean()
total_sessions = filtered_df["sessions"].sum()
avg_bounce = filtered_df["bounceRate"].mean()
col1.metric("Avg Conversion Rate", f"{avg_conversion:.2f}%")
col2.metric("Total Sessions", f"{total_sessions:,}")
col3.metric("Avg Bounce Rate", f"{avg_bounce:.2f}%")

# Analysis
st.subheader("Analysis")
# Conversion Rate by Page
page_stats = filtered_df.groupby("pagePath").agg(
    {"sessions": "sum", "conversions": "sum", "conversionRate": "mean", "bounceRate": "mean"}
).sort_values("conversionRate", ascending=False)

# Conversion Rate by Device
device_stats = filtered_df.groupby("deviceCategory").agg(
    {"sessions": "sum", "conversions": "sum", "conversionRate": "mean", "bounceRate": "mean"}
)

# Conversion Rate by Source
source_stats = filtered_df.groupby("sourceMedium").agg(
    {"sessions": "sum", "conversions": "sum", "conversionRate": "mean", "bounceRate": "mean"}
).sort_values("conversionRate", ascending=False)

# Visualizations
st.subheader("Visualizations")
# Plot 1: Conversion Rate by Page
fig1 = px.bar(page_stats, x=page_stats.index, y="conversionRate", title="Conversion Rate by Page")
fig1.update_layout(xaxis_title="Page Path", yaxis_title="Conversion Rate (%)")
st.plotly_chart(fig1, use_container_width=True)

# Plot 2: Conversion Rate by Device
fig2 = px.bar(device_stats, x=device_stats.index, y="conversionRate", title="Conversion Rate by Device")
fig2.update_layout(xaxis_title="Device Category", yaxis_title="Conversion Rate (%)")
st.plotly_chart(fig2, use_container_width=True)

# Plot 3: Bounce Rate vs Conversion Rate
fig3 = px.scatter(
    filtered_df, x="bounceRate", y="conversionRate", size="sessions", color="pagePath",
    title="Bounce Rate vs Conversion Rate", hover_data=["pagePath", "deviceCategory", "sourceMedium"]
)
fig3.update_layout(xaxis_title="Bounce Rate (%)", yaxis_title="Conversion Rate (%)")
st.plotly_chart(fig3, use_container_width=True)

# Recommendations
st.subheader("Observations")
st.markdown("""
Based on the analysis:
- **Conversion Rate by Page**: The /checkout page has the highest conversion rate at approximately 5.42%, while the /product page has the lowest at approximately 4.92%.
- **Conversion Rate by Device**: Desktops have the highest conversion rate at approximately 5.33%, with mobile devices having the lowest at approximately 5.19%.
- **Conversion Rate by Traffic Source**: Traffic from Facebook CPC has the highest conversion rate at approximately 5.47%, while direct traffic has the lowest at approximately 5.19%.
""")

# Recommendations
st.subheader("Optimization Recommendations")
st.markdown("""
Page-Specific Recommendations
Checkout Page:
- **Strengths**: The /checkout page has the highest conversion rate.
- **Recommendations**: Continue to optimize this page by ensuring the checkout process is as seamless as possible. Consider A/B testing different layouts or adding trust signals like security badges or customer testimonials.

Product Page:
- **Strengths**: The /product page has the lowest conversion rate but likely serves as a critical point in the user journey.
- **Recommendations**: Improve product descriptions, images, and reviews. Consider adding videos or interactive elements to engage users more effectively. Ensure that calls-to-action (CTAs) are clear and compelling.

Cart Page:
- **Strengths**: The /cart page has a high conversion rate.
- **Recommendations**: Simplify the cart page to reduce distractions and make it easy for users to proceed to checkout. Offer incentives like free shipping thresholds or discounts to encourage completion of the purchase.
Device-Specific Recommendations

Desktop:
- **Strengths**: Desktops have the highest conversion rate.
- **Recommendations**: Ensure that the desktop experience is fully optimized. This includes fast load times, intuitive navigation, and a responsive design.

Mobile:
- **Strengths**: Mobile has the lowest conversion rate.
- **Recommendations**: Focus on improving the mobile user experience. This could involve simplifying navigation, increasing button sizes for touch, and ensuring fast load times. Consider implementing mobile-specific features like click-to-call or mobile wallets.

Tablet:
- **Strengths**: Tablets have a moderate conversion rate.
- **Recommendations: Ensure that the tablet experience is not neglected. Test the user interface on various tablet sizes to ensure usability.

Traffic Source Recommendations
Facebook / CPC:
- **Strengths**: This source has the highest conversion rate.
- **Recommendations**: Allocate more budget to Facebook CPC campaigns. Continue to refine targeting and ad creatives to maintain or improve conversion rates.

Email / Newsletter:
- **Strengths**: This source has a high conversion rate.
- **Recommendations**: Segment your email list to provide more personalized content. Test different email formats, subject lines, and CTAs to optimize performance.

Google / Organic:
- **Strengths**: This source has a moderate conversion rate.
- **Recommendations**: Invest in SEO to improve organic search rankings. Create high-quality content that addresses user queries and encourages engagement.

Direct / None:
- **Strengths**: This source has a moderate conversion rate.
- **Recommendations**: Enhance brand recall through consistent messaging across all channels. Use retargeting campaigns to bring back users who have shown interest but haven't converted.
""")

# Display Data
st.subheader("Raw Data")
st.dataframe(filtered_df)