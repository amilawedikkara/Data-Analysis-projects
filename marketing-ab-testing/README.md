# Marketing A/B Testing Analysis

## Project Overview

This project analyzes a marketing A/B testing dataset to compare the conversion performance of an advertisement group against a PSA/control group.

The goal is to determine whether users exposed to ads converted at a higher rate than users in the PSA group, and whether the observed difference is statistically significant.

## Dataset

The dataset contains user-level marketing experiment data.

### Columns

| Column | Description |
|---|---|
| `user_id` | Unique user identifier |
| `test_group` | Experiment group: `ad` or `psa` |
| `converted` | Whether the user converted |
| `total_ads` | Total number of ads shown to the user |
| `most_ads_day` | Day when the user saw the most ads |
| `most_ads_hour` | Hour when the user saw the most ads |

## Project Structure

```text
marketing-ab-testing/
│
├── ab_testing_analysis.py
├── marketing_ab_testing.csv
├── README.md
└── charts/
    ├── conversion_by_group.png
    ├── conversion_by_day.png
    ├── conversion_by_hour.png
    └── conversion_by_ad_exposure.png