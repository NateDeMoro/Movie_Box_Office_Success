# Project Context: Movie Box Office Revenue Prediction

## Quick Summary
Machine learning project predicting movie box office revenue using pre-release data (budget, cast, genre, timing, marketing). Target: R² > 0.70, MAE < $25M on 2,500+ movies from 2010-2024.

## Current Status
- **Phase**: Initial setup complete
- **Completed**: Virtual environment, API keys configured, project structure, plan.md, 5 skeleton notebooks
- **Next Steps**: Data collection from TMDB, Box Office Mojo, YouTube APIs

## Project Structure
```
Movie_Box_Office_Success/
├── data/
│   ├── raw/                    # Raw API/scraped data
│   └── processed/              # Cleaned datasets
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation_insights.ipynb
├── scripts/                    # Reusable functions
├── models/                     # Saved .pkl files
├── visualizations/             # Plots
├── .env                        # API keys (gitignored)
├── requirements.txt
├── plan.md                     # Detailed project plan
└── README.md                   # Public documentation
```

## Data Sources & Collection

### APIs (with rate limits)
1. **TMDB**: Movie metadata (40 requests/10 sec)
2. **OMDb**: Supplemental data (1,000 requests/day)
3. **YouTube Data API**: Trailer metrics (10,000 units/day)

### Web Scraping
- **Box Office Mojo**: Revenue data (respect robots.txt, add delays)

### Target Dataset
- **Size**: 2,500-3,000 movies after cleaning
- **Time Range**: 2010-2024
- **Filters**: Wide releases only (1,000+ theaters), exclude limited/documentaries, must have budget + revenue

### Raw Data Files
- `movies_tmdb_raw.csv`
- `revenue_boxofficemojo_raw.csv`
- `trailers_youtube_raw.csv`

## Key Features to Engineer

### Tier 1 (Essential)
- **Basic**: budget, runtime, rating (G/PG/PG-13/R), genre_primary, is_sequel
- **Temporal**: release_month, release_quarter, is_summer_release, is_holiday_release
- **Cast/Crew**: director_avg_gross, lead_actor_avg_gross, num_a_list_actors
- **Marketing**: trailer_views, days_since_trailer
- **Competition**: num_releases_same_weekend, num_opening_same_month

### Tier 2 (Important)
- budget_category, is_franchise, franchise_number, years_since_last_installment
- director_genre_match, release_month_avg_revenue
- genre_count, runtime_category

### Tier 3 (Nice-to-have)
- is_3d, is_imax, lead_actor_recent_hit
- director_awards, spoken_language_english

### Feature Calculations
**Star Power Index**: Average box office of actor's last 5 films, weighted by recency
**Director Historical Avg**: Mean box office of previous films (exclude current film)
**Competition Metrics**: Count wide releases same weekend, weight by genre overlap

## Modeling Approach

### Train/Test Split
- **Preferred**: Time-based (2010-2021 train, 2022-2024 test)
- **Alternative**: Random 80/20 with stratification by genre

### Target Variable
- **Primary**: Total domestic box office gross (millions)
- **Secondary**: Opening weekend gross
- **Consideration**: May need log transformation if skewed

### Models to Compare
1. **Linear Regression**: Baseline, interpretable (expect R² ~0.60-0.70)
2. **Random Forest**: Best performer likely, handles non-linearity (expect R² ~0.75-0.80)
3. **XGBoost**: If RF insufficient (expect similar to RF)
4. **Ridge Regression**: Compare with linear, handles multicollinearity

### Hyperparameter Tuning
- **Method**: RandomizedSearchCV with 5-fold CV
- **Random Forest params**: n_estimators [100-500], max_depth [10-30, None], min_samples_split [2,5,10]
- **XGBoost params**: learning_rate [0.01-0.3], max_depth [3-9], n_estimators [100-300]

### Evaluation Metrics
- R² (proportion of variance explained)
- MAE (mean absolute error in millions)
- RMSE (penalizes large errors)

## Data Cleaning Strategy

### Missing Values
- **Budget** (critical): If <10% missing → drop rows; if 10-30% → impute with median by genre/year
- **Revenue** (target): Drop any missing (cannot train without ground truth)
- **Others**: Impute or create binary missing indicators

### Cleaning Checklist
- Remove duplicates
- Fix data types (strings→numbers, dates→datetime)
- Standardize categoricals (USA vs US vs United States)
- Validate ranges (budget > 0, runtime 60-240)
- Document all decisions

## EDA Focus Areas

### Key Questions
- What's the typical budget-to-revenue ratio?
- Which genre has highest average revenue? Best ROI?
- What percentage of movies are profitable?
- How much does release timing matter?
- Do sequels reliably outperform originals?
- What's the relationship between runtime and revenue?

### Analysis Types
- **Univariate**: Distributions, summary stats, check skewness
- **Bivariate**: Budget vs revenue, genre vs revenue, release timing vs revenue
- **Correlation**: Heatmap, identify multicollinearity, find top predictors

## Technical Decisions Made

### Included
- Domestic box office only (not international)
- Nominal revenue values (not inflation-adjusted)
- Modern era only (2010-2024 for data quality)
- Wide releases only (excludes limited/art house)

### To Decide During Analysis
- Log-transform target or keep as-is?
- Which preprocessing for Random Forest?
- Drop highly correlated features or keep?
- Threshold for dropping missing data?

## Success Criteria

### Technical Metrics
- R² > 0.70 on test set
- MAE < $25M
- Successfully collect 2,500+ movies
- Identify top 5 most predictive features

### Deliverables
- ✅ Clean GitHub repository
- ✅ 5 notebooks with clear structure
- ✅ Comprehensive README
- ⬜ 3+ compelling visualizations
- ⬜ Feature importance plot
- ⬜ Actual vs predicted plot
- ⬜ Model comparison table
- ⬜ Optional: Streamlit app

## Python Libraries

### Core
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- scikit-learn (modeling, preprocessing, metrics)
- xgboost (gradient boosting)

### Data Collection
- requests (API calls)
- beautifulsoup4 (web scraping)
- python-dotenv (API key management)

### Optional
- streamlit (deployment)

## Workflow Steps

### Step 1: Data Collection ⬜
- Set up API connections
- Collect TMDB data for 3,000 movies
- Scrape Box Office Mojo revenue
- Collect YouTube trailer data
- Save raw CSVs

### Step 2: Cleaning & Initial EDA ⬜
- Load and inspect raw data
- Handle missing values and outliers
- Create cleaned dataset
- Initial distributions and summary stats

### Step 3: Deep EDA & Feature Engineering ⬜
- Bivariate analysis
- Correlation analysis
- Engineer all features (Tier 1, 2, 3)
- Validate engineered features

### Step 4: Preprocessing & Baseline ⬜
- Train/test split
- Encode categoricals
- Scale features (for linear models)
- Train Linear Regression baseline

### Step 5: Model Optimization ⬜
- Train Random Forest + tune
- Train XGBoost + tune
- Compare all models
- Feature importance analysis

### Step 6: Evaluation & Interpretation ⬜
- Detailed evaluation of best model
- Error analysis
- Create visualizations
- Document insights and limitations

### Step 7: Documentation & Polish ⬜
- Update README with results
- Clean code and add docstrings
- Test reproducibility
- Optional: Streamlit deployment

## Important Notes

### For Data Collection
- Respect rate limits (add delays)
- Handle errors gracefully
- Save intermediate results
- Document API endpoints used

### For Feature Engineering
- Calculate historical metrics excluding current film
- Handle first-time directors/actors (use median or category average)
- Weight recent films more in star power calculations
- Cap outliers in ensemble cast scenarios

### For Modeling
- Use time-based split to simulate real prediction
- Check for data leakage (no future info in training)
- Validate feature importance aligns with EDA
- Document surprising findings

### For Evaluation
- Focus on interpretable errors (dollars, not just R²)
- Analyze where model fails (which movies?)
- Compare predictions on recent hits/flops
- Consider business context (25M error on 200M movie = 12.5%)

## Common Pitfalls to Avoid
- Don't use future information in training (data leakage)
- Don't ignore missing data patterns
- Don't over-engineer features without validation
- Don't tune on test set (use CV on training only)
- Don't forget to document assumptions and limitations
- Don't include movies still in theaters (incomplete revenue)

## Questions for Future Work
- Should sequels/franchises have separate models?
- Can sentiment analysis improve predictions?
- What about international revenue prediction?
- How does streaming impact theatrical performance?
- Can we predict flops vs hits (classification)?
