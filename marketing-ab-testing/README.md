# Marketing A/B Testing Analysis

## Project Overview

This project analyzes a marketing A/B testing dataset to compare the conversion performance of an advertisement group against a PSA/control group.

The goal is to determine whether users exposed to ads converted at a higher rate than users in the PSA group, and whether the observed difference is statistically significant.

## Dataset

The dataset contains user-level marketing experiment data.

### Columns

| Column          | Description                           |
| --------------- | ------------------------------------- |
| `user_id`       | Unique user identifier                |
| `test_group`    | Experiment group: `ad` or `psa`       |
| `converted`     | Whether the user converted            |
| `total_ads`     | Total number of ads shown to the user |
| `most_ads_day`  | Day when the user saw the most ads    |
| `most_ads_hour` | Hour when the user saw the most ads   |

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
```

## Key Results

| Metric                    |                 Result |
| ------------------------- | ---------------------: |
| Overall conversion rate   |                  2.52% |
| Ad group conversion rate  |                  2.55% |
| PSA group conversion rate |                  1.79% |
| Absolute lift             | 0.77 percentage points |
| Relative lift             |                 43.09% |
| 95% confidence interval   |         0.60% to 0.94% |

The ad group had a higher observed conversion rate than the PSA group. The absolute difference was 0.77 percentage points, with a relative lift of 43.09%.

## Statistical Testing

Two statistical tests were used to evaluate whether the conversion-rate difference between the ad and PSA groups was statistically significant.

| Test                  | Result          |
| --------------------- | --------------- |
| Chi-square test       | p-value < 0.001 |
| Two-proportion z-test | p-value < 0.001 |

Both tests suggest that the conversion rates between the ad group and PSA group are statistically significantly different.

## Visualizations

The project includes the following charts:

| Chart                           | Description                                         |
| ------------------------------- | --------------------------------------------------- |
| `conversion_by_group.png`       | Compares conversion rates between ad and PSA groups |
| `conversion_by_day.png`         | Shows conversion rate by most ads day               |
| `conversion_by_hour.png`        | Shows the top 5 hours by conversion rate            |
| `conversion_by_ad_exposure.png` | Shows conversion rate by ad exposure bucket         |

Charts are saved in the `charts/` folder.

## Business Conclusion

The advertising campaign appears to have improved conversion performance compared with the PSA group. The ad group achieved a higher conversion rate, and the difference was statistically significant.

From a business perspective, this suggests that the ad campaign was more effective than the PSA campaign in driving conversions. However, the analysis should still consider campaign cost, audience targeting, and potential external factors before making a final marketing decision.

## Limitations

* The ad group is much larger than the PSA group, so group imbalance should be considered.
* The dataset shows conversion outcomes, but it does not include campaign cost or revenue per conversion.
* Higher ad exposure is associated with higher conversion rates, but this does not prove that showing more ads always causes more conversions.
* External factors such as audience segment, timing, or user intent may also affect conversion behavior.

## How to Run

1. Clone the repository.

```bash
git clone https://github.com/amilawedikkara/Data-Analysis-projects.git
```

2. Navigate to the project folder.

```bash
cd Data-Analysis-projects/marketing-ab-testing
```

3. Install the required Python libraries.

```bash
pip install pandas numpy matplotlib scipy statsmodels
```

4. Run the analysis script.

```bash
python ab_testing_analysis.py
```
