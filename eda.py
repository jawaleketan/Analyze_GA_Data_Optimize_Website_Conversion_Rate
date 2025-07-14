# Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("whitegrid")  # You can choose from styles like "darkgrid", "whitegrid", "dark", "white", and "ticks"

# Loading Dataset

df = pd.read_csv("website_analytics.csv")

print(f"First 5 rows from dataset: \n", df.head())

print(df.info())

print(f"Checking NULL values in dataset: \n", df.isnull().sum())

# Data Cleaning

df["conversions"] = df["conversions"].fillna(0)
df["sessions"] = df["sessions"].replace(0, 1)  # Avoid division by zero
df["conversionRate"] = df["conversions"] / df["sessions"] * 100

# Exploratory Data Analysis

# 1.Conversion Rate by Page

page_stats = df.groupby("pagePath").agg(
    {
        "sessions": "sum",
        "conversions": "sum",
        "conversionRate": "mean",
        "bounceRate": "mean"
    }
).sort_values("conversionRate", ascending=False)

print(f"Conversion Rate by Page: \n", page_stats.head())

# 2.Conversion Rate by Device

device_stats = df.groupby("deviceCategory").agg(
    {
        "sessions": "sum",
        "conversions": "sum",
        "conversionRate": "mean",
        "bounceRate": "mean"
    }
)

print(f"Conversion Rate by Page: \n", device_stats.head())

# 3.Conversion Rate by Traffic Source

source_stats = df.groupby("sourceMedium").agg(
    {
        "sessions": "sum",
        "conversions": "sum",
        "conversionRate": "mean",
        "bounceRate": "mean"
    }
).sort_values("conversionRate", ascending=False)

print(f"Conversion Rate by Traffic Source: \n", source_stats.head())

# Visualizations

# Plot 1: Conversion Rate by Page

plt.figure(figsize=(10, 6))
sns.barplot(x="conversionRate", y=page_stats.index, data=page_stats)
plt.title("Conversion Rate by Page")
plt.xlabel("Conversion Rate (%)")
plt.ylabel("Page Path")
plt.tight_layout()
plt.savefig("conversion_rate_by_page.png")
plt.show()

# Plot 2: Conversion Rate by Device

plt.figure(figsize=(8, 5))
sns.barplot(x=device_stats.index, y="conversionRate", data=device_stats)
plt.title("Conversion Rate by Device")
plt.xlabel("Device Category")
plt.ylabel("Conversion Rate (%)")
plt.tight_layout()
plt.savefig("conversion_rate_by_device.png")
plt.show()

# Plot 3: Bounce Rate vs Conversion Rate

plt.figure(figsize=(8, 5))
sns.scatterplot(x="bounceRate", y="conversionRate", size="sessions", hue="pagePath", data=df)
plt.title("Bounce Rate vs Conversion Rate")
plt.xlabel("Bounce Rate (%)")
plt.ylabel("Conversion Rate (%)")
plt.tight_layout()
plt.savefig("bounce_vs_conversion.png")
plt.show()

# Print Analysis Results

print("=== Conversion Rate by Page ===")
print(page_stats[["sessions", "conversions", "conversionRate", "bounceRate"]])
print("\n=== Conversion Rate by Device ===")
print(device_stats[["sessions", "conversions", "conversionRate", "bounceRate"]])
print("\n=== Conversion Rate by Traffic Source ===")
print(source_stats[["sessions", "conversions", "conversionRate", "bounceRate"]])

# Save Analysis Results

# Save Analysis Results
page_stats.to_csv("page_stats.csv")
device_stats.to_csv("device_stats.csv")
source_stats.to_csv("source_stats.csv")

# Observations

def save_observations_to_file(file_path):
    # Define the observations
    observations = """=== Observations ===

Conversion Rate by Page: The /checkout page has the highest conversion rate at approximately 5.42%, while the /product page has the lowest at approximately 4.92%.

Conversion Rate by Device: Desktops have the highest conversion rate at approximately 5.33%, with mobile devices having the lowest at approximately 5.19%.

Conversion Rate by Traffic Source: Traffic from Facebook CPC has the highest conversion rate at approximately 5.47%, while direct traffic has the lowest at approximately 5.19%.
"""

    # Write the observations to a text file
    with open(file_path, 'w') as file:
        file.write(observations)

# Call the function to save observations to a file
save_observations_to_file('observations.txt')

# Optimization Recommendations

def save_recommendations_to_file(file_path):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Page-Specific Recommendations
        file.write("=== Page-Specific Recommendations ===\n\n")
        file.write("Checkout Page:\n")
        file.write("Strengths: The /checkout page has the highest conversion rate.\n")
        file.write("Recommendations: Continue to optimize this page by ensuring the checkout process is as seamless as possible. Consider A/B testing different layouts or adding trust signals like security badges or customer testimonials.\n\n")

        file.write("Product Page:\n")
        file.write("Strengths: The /product page has the lowest conversion rate but likely serves as a critical point in the user journey.\n")
        file.write("Recommendations: Improve product descriptions, images, and reviews. Consider adding videos or interactive elements to engage users more effectively. Ensure that calls-to-action (CTAs) are clear and compelling.\n\n")

        file.write("Cart Page:\n")
        file.write("Strengths: The /cart page has a high conversion rate.\n")
        file.write("Recommendations: Simplify the cart page to reduce distractions and make it easy for users to proceed to checkout. Offer incentives like free shipping thresholds or discounts to encourage completion of the purchase.\n\n")

        # Device-Specific Recommendations
        file.write("=== Device-Specific Recommendations ===\n\n")
        file.write("Desktop:\n")
        file.write("Strengths: Desktops have the highest conversion rate.\n")
        file.write("Recommendations: Ensure that the desktop experience is fully optimized. This includes fast load times, intuitive navigation, and a responsive design.\n\n")

        file.write("Mobile:\n")
        file.write("Strengths: Mobile has the lowest conversion rate.\n")
        file.write("Recommendations: Focus on improving the mobile user experience. This could involve simplifying navigation, increasing button sizes for touch, and ensuring fast load times. Consider implementing mobile-specific features like click-to-call or mobile wallets.\n\n")

        file.write("Tablet:\n")
        file.write("Strengths: Tablets have a moderate conversion rate.\n")
        file.write("Recommendations: Ensure that the tablet experience is not neglected. Test the user interface on various tablet sizes to ensure usability.\n\n")

        # Traffic Source Recommendations
        file.write("=== Traffic Source Recommendations ===\n\n")
        file.write("Facebook / CPC:\n")
        file.write("Strengths: This source has the highest conversion rate.\n")
        file.write("Recommendations: Allocate more budget to Facebook CPC campaigns. Continue to refine targeting and ad creatives to maintain or improve conversion rates.\n\n")

        file.write("Email / Newsletter:\n")
        file.write("Strengths: This source has a high conversion rate.\n")
        file.write("Recommendations: Segment your email list to provide more personalized content. Test different email formats, subject lines, and CTAs to optimize performance.\n\n")

        file.write("Google / Organic:\n")
        file.write("Strengths: This source has a moderate conversion rate.\n")
        file.write("Recommendations: Invest in SEO to improve organic search rankings. Create high-quality content that addresses user queries and encourages engagement.\n\n")

        file.write("Direct / None:\n")
        file.write("Strengths: This source has a moderate conversion rate.\n")
        file.write("Recommendations: Enhance brand recall through consistent messaging across all channels. Use retargeting campaigns to bring back users who have shown interest but haven't converted.\n")

# Call the function to save recommendations to a file
save_recommendations_to_file('recommendations.txt')