# Movie Box Office Revenue Prediction - EDA Findings

**Project**: Movie Box Office Success Prediction
**Phase**: Data Cleaning & EDA
**Date**: 2026-01-23
**Status**: Initial EDA Complete

---

## Dataset Overview

- **Original Size**: 5,100 movies
- **Cleaned Dataset**: 2,095 movies (after removing missing budget/revenue and duplicates)
- **Time Range**: 2010-2024
- **Success Rate**: 67.5% profitable (1,414 movies), 32.5% loss-making (681 movies)
- **Median ROI**: 2.09x

---

## Key Finding: Budget is the Dominant Pre-Release Predictor

**Budget** is by far the strongest predictor of box office revenue with:
- **Correlation coefficient (r)**: 0.74 with worldwide revenue
- **R² value**: 0.55 (explains 55% of revenue variance)

**Note**: R² = r² = 0.74² = 0.55. The correlation of 0.74 is very strong, and an R² of 0.55 from a single predictor is excellent for box office prediction.

This is the most important pre-release metric available and significantly outperforms all other features.

---

## Pre-Release Predictor Variables

### Valid Pre-Release Predictors
| Variable   | Correlation | R² | Notes                                       |
| ---------- | ----------- | -- | ------------------------------------------- |
| **budget** | **0.74**    | **0.55** | Strongest predictor - available pre-release |
| runtime    | 0.23        | 0.05 | Weak but valid - available pre-release |

### INVALID Predictors (Post-Release Data - DO NOT USE)
| Variable     | Correlation | Why Invalid |
| ------------ | ----------- | ----------- |
| vote_count   | 0.72        | ❌ **TMDB user rating count** - accumulates AFTER release. Older movies have more votes (e.g., Inception 2010 has 38,539 votes vs recent 2024 movie with 75 votes). This is post-release audience engagement, not a pre-release predictor. |
| vote_average | 0.23        | ❌ **TMDB average rating** - contaminated with post-release audience scores. Not reliable pre-release data. |
| popularity   | 0.59        | ❌ **TMDB popularity metric** - includes post-release viewership and engagement data from years after release. |

**Critical Finding**: These TMDB metrics (vote_count, vote_average, popularity) were collected in 2024+ and include cumulative post-release data. Using them would be **data leakage** - we cannot predict pre-release revenue using post-release audience metrics. Successful movies naturally accumulate more votes/popularity over time.

### Post-Release Metrics (DO NOT USE as predictors)
| Variable | Correlation | Reason |
|----------|-------------|--------|
| domestic_total | 0.94 | Post-release revenue data |
| opening_weekend | 0.90 | Post-release revenue data |

**Important**: We are predicting revenue using only pre-release data. Variables like domestic_total and opening_weekend have extremely high correlations but cannot be used as they represent actual revenue outcomes, not predictors.

---

## Genre Performance Analysis

### Top 5 Genres by Mean Revenue
1. **Adventure**: $386M average (108 movies)
2. **Family**: $350M average (63 movies)
3. **Animation**: $261M average (120 movies)
4. **Science Fiction**: $250M average (83 movies)
5. **Action**: $222M average (443 movies)

**Insight**: Family-friendly content (Adventure, Family, Animation) dominates box office performance.

---

## Rating Performance Analysis

### Revenue by MPAA Rating
- **G-rated**: $328M average (highest)
- **PG**: $303M average
- **PG-13**: $288M average
- **R-rated**: $86M average (lowest - significantly lower)

**Insight**: Family-accessible ratings (G, PG, PG-13) generate 3-4x more revenue than R-rated films on average.

---

## Release Timing Insights

### Best Performing Months
1. **June**: $268M average
2. **July**: $213M average
3. **May**: $183M average

### Worst Performing Months
1. **August**: $78M average
2. **September**: $82M average

**Insight**: Summer blockbuster season (May-July) significantly outperforms other months. Avoid late summer/early fall releases.

---

## Data Distribution Characteristics

### Skewness (All Highly Right-Skewed)
- **Revenue**: 3.38
- **Budget**: 2.08
- **Domestic Total**: 3.18
- **Opening Weekend**: 4.02

**Recommendation**: Apply log transformation to budget and revenue for modeling to handle extreme skewness.

---

## Data Quality Notes

### Strengths
- High completion rate: 2,095/2,100 usable records (99.8%)
- Minimal missing values in key columns
- Well-cleaned dataset with duplicates removed

### Issues Identified
- **Outliers present**: e.g., "The Quiet Girl" with 6,807,187x ROI (likely data quality issue)
- **Language distribution**: 73.6% English-language films - may affect generalizability
- **Vote metrics timing**: Need to verify if vote_count and vote_average are truly pre-release or include post-release data

---

## Critical Decisions for Feature Engineering

### ~~Variables to Verify Timing~~ ✅ RESOLVED
- ~~**popularity**~~: ❌ INVALID - Confirmed to include post-release data
- ~~**vote_count & vote_average**~~: ❌ INVALID - Confirmed to be post-release audience metrics

**Decision**: Exclude all TMDB vote/popularity metrics from modeling. Focus on true pre-release predictors only.

### Recommended Feature Engineering Priorities
1. **Budget-based features**: Budget categories, budget relative to genre average
2. **Temporal features**: Release month, quarter, summer/holiday flags
3. **Genre features**: Genre combinations, primary genre
4. **Rating features**: MPAA rating categories
5. **Cast/Director features**: Historical performance metrics (to be engineered)

---

## Next Steps

1. ~~**Verify timing** of vote_count, vote_average, and popularity metrics~~ ✅ COMPLETE - Confirmed invalid
2. **Feature engineering**: Create Tier 1 features (temporal, genre, budget categories, cast/crew metrics)
3. **Calculate star power**: Director and actor historical performance metrics (must exclude current film to avoid leakage)
4. **Handle outliers**: Address extreme ROI values and potential data errors
5. **Log transformation**: Consider applying to budget and revenue for modeling
6. **Baseline model**: Train linear regression with budget as primary predictor (baseline R² = 0.55 established)

---

## Key Takeaway

**Budget is the foundation** - With an R² of 0.55 from budget alone (correlation of 0.74), our goal is to improve prediction by adding complementary pre-release features (cast, genre, timing, marketing). Success means achieving R² > 0.70-0.75 by incorporating these additional signals.
