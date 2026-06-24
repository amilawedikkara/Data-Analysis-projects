import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
from statsmodels.stats.proportion import proportions_ztest



# Load the real marketing A/B testing dataset from a CSV file
df = pd.read_csv("marketing_ab_testing.csv")

# Remove the unnecessary index column from the CSV
df = df.drop(columns=["Unnamed: 0"])

# Rename columns to make them easier to use in Python
df = df.rename(columns={
    "user id": "user_id",
    "test group": "test_group",
    "total ads": "total_ads",
    "most ads day": "most_ads_day",
    "most ads hour": "most_ads_hour"
})

print("First 5 rows of the cleaned dataset:")
print(df.head())

print("\nDataset shape after cleaning:")
print(df.shape)

print("\nCleaned column names:")
print(df.columns)

print("\nDataset information after cleaning:")
df.info()
print("\nMissing values by column:")
print(df.isnull().sum())

print("\nNumber of duplicate user IDs:")
print(df["user_id"].duplicated().sum())

print("\nTest group counts:")
print(df["test_group"].value_counts())

print("\nConverted value counts:")
print(df["converted"].value_counts())

overall_conversion_rate = df["converted"].mean()

print("\nOverall conversion rate:")
print(overall_conversion_rate)

print("\nOverall conversion rate as percentage:")
print(f"{overall_conversion_rate:.2%}")

conversion_rate_by_group = df.groupby("test_group")["converted"].mean()

print("\nConversion rate by test group:")
print(conversion_rate_by_group)

print("\nConversion rate by test group as percentage:")
print(conversion_rate_by_group.apply(lambda x: f"{x:.2%}"))

ad_conversion_rate = conversion_rate_by_group["ad"]
psa_conversion_rate = conversion_rate_by_group["psa"]

absolute_lift = ad_conversion_rate - psa_conversion_rate
relative_lift = absolute_lift / psa_conversion_rate

print("\nA/B test lift analysis:")
print(f"Ad conversion rate: {ad_conversion_rate:.2%}")
print(f"PSA conversion rate: {psa_conversion_rate:.2%}")
print(f"Absolute lift: {absolute_lift:.2%}")
print(f"Relative lift: {relative_lift:.2%}")

contingency_table = pd.crosstab(df["test_group"], df["converted"])

print("\nContingency table:")
print(contingency_table)

chi2_stat, p_value, dof, expected = chi2_contingency(contingency_table)

print("\nChi-square test results:")
print(f"Chi-square statistic: {chi2_stat:.4f}")
if p_value < 0.001:
    print("P-value: < 0.001")
else:
    print(f"P-value: {p_value:.6f}")
print(f"Degrees of freedom: {dof}")

if p_value < 0.05:
    print("Conclusion: The difference in conversion rates is statistically significant.")
else:
    print("Conclusion: The difference in conversion rates is not statistically significant.")

converted_counts = contingency_table[True]
total_counts = contingency_table.sum(axis=1)

z_stat, z_p_value = proportions_ztest(
    count=converted_counts,
    nobs=total_counts
)

print("\nTwo-proportion z-test results:")
print(f"Z-statistic: {z_stat:.4f}")

if z_p_value < 0.001:
    print("P-value: < 0.001")
else:
    print(f"P-value: {z_p_value:.6f}")

if z_p_value < 0.05:
    print("Conclusion: The conversion rates are statistically significantly different.")
else:
    print("Conclusion: The conversion rates are not statistically significantly different.")

# 95% confidence interval for the difference in conversion rates
ad_converted = contingency_table.loc["ad", True]
ad_total = contingency_table.loc["ad"].sum()

psa_converted = contingency_table.loc["psa", True]
psa_total = contingency_table.loc["psa"].sum()

ad_rate = ad_converted / ad_total
psa_rate = psa_converted / psa_total

rate_difference = ad_rate - psa_rate

standard_error = np.sqrt(
    (ad_rate * (1 - ad_rate) / ad_total) +
    (psa_rate * (1 - psa_rate) / psa_total)
)

z_critical = 1.96

ci_lower = rate_difference - z_critical * standard_error
ci_upper = rate_difference + z_critical * standard_error

print("\n95% confidence interval for conversion rate difference:")
print(f"Rate difference: {rate_difference:.2%}")
print(f"95% CI: [{ci_lower:.2%}, {ci_upper:.2%}]")

conversion_by_day = df.groupby("most_ads_day")["converted"].agg(["count", "sum", "mean"])

conversion_by_day = conversion_by_day.rename(columns={
    "count": "total_users",
    "sum": "converted_users",
    "mean": "conversion_rate"
})

conversion_by_day = conversion_by_day.sort_values("conversion_rate", ascending=False)

print("\nConversion rate by most ads day:")
print(conversion_by_day)

print("\nConversion rate by most ads day as percentage:")
print(conversion_by_day["conversion_rate"].apply(lambda x: f"{x:.2%}"))

conversion_by_hour = df.groupby("most_ads_hour")["converted"].agg(["count", "sum", "mean"])

conversion_by_hour = conversion_by_hour.rename(columns={
    "count": "total_users",
    "sum": "converted_users",
    "mean": "conversion_rate"
})

conversion_by_hour = conversion_by_hour.sort_values("conversion_rate", ascending=False)

print("\nConversion rate by most ads hour:")
print(conversion_by_hour)

print("\nTop 5 hours by conversion rate:")
print(conversion_by_hour.head(5))

print("\nTop 5 hours by conversion rate as percentage:")
print(conversion_by_hour["conversion_rate"].head(5).apply(lambda x: f"{x:.2%}"))

ads_by_conversion = df.groupby("converted")["total_ads"].agg([
    "count", "mean", "median", "min", "max"
])

ads_by_conversion = ads_by_conversion.rename(index={
    False: "not_converted",
    True: "converted"
})

print("\nTotal ads summary by conversion status:")
print(ads_by_conversion)

ad_bins = [0, 10, 50, 100, 200, df["total_ads"].max()]
ad_labels = ["1-10", "11-50", "51-100", "101-200", "201+"]

df["ad_exposure_bucket"] = pd.cut(
    df["total_ads"],
    bins=ad_bins,
    labels=ad_labels,
    include_lowest=True
)

conversion_by_ad_bucket = df.groupby(
    "ad_exposure_bucket",
    observed=False
)["converted"].agg(["count", "sum", "mean"])

conversion_by_ad_bucket = conversion_by_ad_bucket.rename(columns={
    "count": "total_users",
    "sum": "converted_users",
    "mean": "conversion_rate"
})

print("\nConversion rate by ad exposure bucket:")
print(conversion_by_ad_bucket)

print("\nConversion rate by ad exposure bucket as percentage:")
print(conversion_by_ad_bucket["conversion_rate"].apply(lambda x: f"{x:.2%}"))

# Bar chart: conversion rate by test group
plt.figure(figsize=(6, 4))

conversion_rate_by_group.plot(kind="bar")

plt.title("Conversion Rate by Test Group")
plt.xlabel("Test Group")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("charts/conversion_by_group.png")
plt.close()

print("\nChart saved: charts/conversion_by_group.png")

# Bar chart: conversion rate by most ads day
plt.figure(figsize=(8, 4))

conversion_by_day["conversion_rate"].plot(kind="bar")

plt.title("Conversion Rate by Most Ads Day")
plt.xlabel("Most Ads Day")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/conversion_by_day.png")
plt.close()

print("Chart saved: charts/conversion_by_day.png")

# Bar chart: top 5 conversion rates by most ads hour
plt.figure(figsize=(8, 4))

conversion_by_hour["conversion_rate"].head(5).plot(kind="bar")

plt.title("Top 5 Hours by Conversion Rate")
plt.xlabel("Most Ads Hour")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig("charts/conversion_by_hour.png")
plt.close()

print("Chart saved: charts/conversion_by_hour.png")

# Bar chart: conversion rate by ad exposure bucket
plt.figure(figsize=(8, 4))

conversion_by_ad_bucket["conversion_rate"].plot(kind="bar")

plt.title("Conversion Rate by Ad Exposure Bucket")
plt.xlabel("Total Ads Bucket")
plt.ylabel("Conversion Rate")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/conversion_by_ad_exposure.png")
plt.close()

print("Chart saved: charts/conversion_by_ad_exposure.png")