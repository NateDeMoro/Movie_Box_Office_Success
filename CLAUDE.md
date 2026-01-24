# Movie Box Office Revenue Prediction

## Quick Summary
ML project predicting movie box office revenue using pre-release data (budget, cast, genre, timing, marketing). **Target**: R² > 0.70, MAE < $25M on 2,500+ movies (2010-2024).

## Current Status
- **Phase**: Data collection in progress
- **Completed**: Environment setup, API config, TMDB data collection, Box Office Mojo scraping, initial data merging
- **In Progress**: 01_data_collection.ipynb - refining merged dataset
- **Next**: Data cleaning & EDA (notebook 02)

## Project Structure
```
Movie_Box_Office_Success/
├── data/
│   ├── raw/                    # Raw API/scraped data
│   └── processed/              # Cleaned datasets
├── notebooks/                  # 01-05: collection → evaluation
├── scripts/                    # Reusable functions
├── models/                     # Saved .pkl files
├── visualizations/
└── .env                        # API keys (gitignored)
```

## Data Sources

### APIs
- **TMDB**: Movie metadata (40 req/10 sec)
- **OMDb**: Supplemental data (1,000 req/day)
- **YouTube Data API**: Trailer metrics (10,000 units/day)

### Web Scraping
- **Box Office Mojo**: Revenue data (respect robots.txt, add delays)

### Target Dataset
- **Size**: 2,500-3,000 movies
- **Years**: 2010-2024
- **Filter**: Wide releases (1,000+ theaters), must have budget + revenue

## Key Features

### Tier 1 (Essential)
- **Basic**: budget, runtime, rating, genre_primary, is_sequel
- **Temporal**: release_month, release_quarter, is_summer_release, is_holiday_release
- **Cast/Crew**: director_avg_gross, lead_actor_avg_gross, num_a_list_actors
- **Marketing**: trailer_views, days_since_trailer
- **Competition**: num_releases_same_weekend, num_opening_same_month

### Tier 2 (Important)
- budget_category, is_franchise, franchise_number, years_since_last_installment
- director_genre_match, release_month_avg_revenue, genre_count, runtime_category

### Tier 3 (Nice-to-have)
- is_3d, is_imax, lead_actor_recent_hit, director_awards, spoken_language_english

### Feature Calculations
- **Star Power**: Average box office of actor's last 5 films, weighted by recency
- **Director Historical Avg**: Mean box office of previous films (exclude current)
- **Competition**: Count wide releases same weekend, weight by genre overlap

## Modeling

### Train/Test Split
- **Preferred**: Time-based (2010-2021 train, 2022-2024 test)
- **Alternative**: Random 80/20 stratified by genre

### Target Variable
- Total domestic box office gross (millions)
- May need log transformation if skewed

### Models
1. **Linear Regression**: Baseline (expect R² ~0.60-0.70)
2. **Random Forest**: Main model (expect R² ~0.75-0.80)
3. **XGBoost**: Alternative if RF insufficient
4. **Ridge**: Handle multicollinearity

### Hyperparameters
- **Method**: RandomizedSearchCV, 5-fold CV
- **RF**: n_estimators [100-500], max_depth [10-30, None], min_samples_split [2,5,10]
- **XGBoost**: learning_rate [0.01-0.3], max_depth [3-9], n_estimators [100-300]

### Metrics
- **R²**: Variance explained
- **MAE**: Mean absolute error (millions)
- **RMSE**: Penalizes large errors

## Data Cleaning

### Missing Values
- **Budget**: Drop if <10% missing; impute median by genre/year if 10-30%
- **Revenue** (target): Drop any missing
- **Others**: Impute or create missing indicators

### Checklist
- Remove duplicates
- Fix data types (strings→numbers, dates→datetime)
- Standardize categoricals
- Validate ranges (budget > 0, runtime 60-240)
- Document decisions

## EDA Focus

### Key Questions
- Budget-to-revenue ratio?
- Genre with highest revenue/ROI?
- Profitability percentage?
- Release timing impact?
- Sequels vs originals performance?
- Runtime-revenue relationship?

### Analysis
- **Univariate**: Distributions, summary stats, skewness
- **Bivariate**: Budget vs revenue, genre vs revenue, timing vs revenue
- **Correlation**: Heatmap, multicollinearity, top predictors

## Technical Decisions

### Scope
- ✅ Domestic box office only
- ✅ Nominal values (not inflation-adjusted)
- ✅ 2010-2024 only
- ✅ Wide releases only

### To Decide
- Log-transform target?
- Feature selection approach?
- Missing data thresholds?

## Success Criteria

### Metrics
- R² > 0.70 on test set
- MAE < $25M
- Collect 2,500+ movies
- Identify top 5 predictive features

### Deliverables
- ✅ Clean repo structure
- ✅ 5 organized notebooks
- ✅ Comprehensive README
- ⬜ 3+ visualizations
- ⬜ Feature importance plot
- ⬜ Actual vs predicted plot
- ⬜ Model comparison table

## Libraries

### Core
- pandas, numpy, matplotlib, seaborn, scikit-learn, xgboost

### Data Collection
- requests, beautifulsoup4, python-dotenv

## Workflow

1. **Data Collection** 🔄
   - TMDB API calls, Box Office Mojo scraping, YouTube trailer data

2. **Cleaning & EDA** ⬜
   - Handle missing values, outliers, distributions, correlations

3. **Feature Engineering** ⬜
   - Create Tier 1-3 features, validate engineered features

4. **Baseline Model** ⬜
   - Train/test split, encoding, scaling, Linear Regression

5. **Model Optimization** ⬜
   - Random Forest + XGBoost tuning, feature importance

6. **Evaluation** ⬜
   - Error analysis, visualizations, insights

7. **Documentation** ⬜
   - Update README, clean code, test reproducibility

## Critical Notes

### Data Collection
- Respect rate limits (add delays between requests)
- Save intermediate results
- Handle API errors gracefully

### Feature Engineering
- Calculate historical metrics **excluding current film** (avoid data leakage)
- Handle first-time directors/actors with median/category average
- Weight recent films more for star power

### Modeling
- Use time-based split for realistic evaluation
- **No data leakage**: No future information in training
- Validate feature importance aligns with EDA

### Common Pitfalls
- ❌ Future information in training (data leakage)
- ❌ Tuning on test set (use CV on training only)
- ❌ Movies still in theaters (incomplete revenue)
- ❌ Over-engineering without validation
- ❌ Ignoring missing data patterns

## Future Work
- Separate models for sequels/franchises?
- Sentiment analysis integration?
- International revenue prediction?
- Classification model (flop vs hit)?
