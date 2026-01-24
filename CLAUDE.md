# Movie Box Office Revenue Prediction

**Author**: Nate DeMoro

## Quick Summary
ML project predicting movie box office revenue using pre-release data (budget, cast, genre, timing, marketing). **Target**: R² > 0.70, MAE < $25M on 2,500+ movies (2010-2024).

## Documentation
**Project notes and detailed planning are now managed in Obsidian.**
- **Vault Location**: `/Users/ndemoro/Desktop/FOLDERS/Nate_Obsidian/Movie_project_folder`
- This CLAUDE.md file provides quick reference for core project info and AI assistant context
- For detailed notes, plans, analysis, and documentation, refer to the Obsidian vault

**Documentation Workflow**:
- **When completing major phases** (e.g., Phase 2 EDA, Phase 3 Feature Engineering, Phase 5 Model Optimization):
  - Create a new Obsidian markdown file: `Movie Box Office - [Phase Name] Findings.md`
  - Document key findings, insights, decisions, and next steps
  - Example: `Movie Box Office - EDA Findings.md` was created after completing Phase 2
  - Save to: `/Users/ndemoro/Desktop/FOLDERS/Nate_Obsidian/Movie_project_folder/`
  - Sync to repo using `./sync_obsidian_notes.sh` and commit

## PROJECT PROGRESS TRACKER

**Last Updated**: 2026-01-24

### Phase 1: Data Collection - COMPLETE
- __Step 1.1: Project setup, API keys, initial functions__
- __Step 1.2: TMDB data collection (5,100 movies)__
- __Step 1.3: Box Office Mojo scraping and data merging__

### Phase 2: Data Cleaning & Initial EDA - COMPLETE
- __Step 2.1: Load, inspect, identify issues__
- __Step 2.2: Complete cleaning, handle missing values (2,095 final movies)__
- __Step 2.3: Create visualizations, document findings__

**Key Findings from Phase 2**:
- Budget is strongest pre-release predictor: r=0.73, R²=0.54
- Identified invalid predictors: vote_count, vote_average, popularity (post-release data)
- Dataset: 1,618 movies (2010-2024), 67.5% profitable
- Top genres: Adventure ($386M), Family ($350M), Animation ($261M)
- Best release months: June ($268M), July ($213M), May ($183M)

### Phase 3: Deep EDA & Feature Engineering - COMPLETE
- __Step 3.1: Bivariate analysis, correlation analysis__
- __Step 3.2: Engineer Tier 1 features (cast/crew, temporal, competition)__
- __Step 3.3: EDA on engineered features, finalize feature set__

**Key Findings from Phase 3**:
- Created 28 features: 9 original + 13 Tier 1 + 6 Tier 2
- Top 3 features explain 77.5%: budget (49.6%), director_historical_avg (19.3%), lead_actor_historical_avg (8.5%)
- Strict no-leakage approach: all historical averages exclude current movie
- Final dataset: movies_features.csv (2,095 × 36 columns)
- VIF analysis: acceptable multicollinearity (most features VIF < 5)

### Phase 4: Preprocessing & Baseline Modeling - NEXT
- Step 4.1: Train/test split (time-based: 2010-2021 train, 2022-2024 test) **[NEXT STEP]**
- Step 4.2: Feature encoding and scaling
- Step 4.3: Train baseline models (Linear Regression, Ridge)

### Phase 5-7: Not Started
- Step 5: Model Optimization & Comparison
- Step 6: Evaluation and Interpretation
- Step 7: Documentation & Polish

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

### Invalid Predictors (DO NOT USE)
**TMDB Metrics (Post-Release Data)**:
- **vote_count**: Number of TMDB user ratings - accumulates AFTER release (older movies have more votes)
- **vote_average**: Average TMDB rating - contaminated with post-release audience scores
- **popularity**: TMDB popularity metric - includes post-release viewership/engagement

**Why excluded**: These metrics were collected at scrape time (2024+) and include years of post-release data. Successful movies accumulate more votes over time. Using them would be data leakage - you cannot predict pre-release revenue using post-release audience metrics.

**Note**: Budget has strongest pre-release correlation (r=0.73, R²=0.54) with revenue.

## Modeling

### Train/Test Split
- **Preferred**: Time-based (2010-2021 train, 2022-2024 test)
- **Alternative**: Random 80/20 stratified by genre

### Target Variable
- Total worldwide box office gross (millions)
- May need log transformation if skewed

### Models
1. **Linear Regression**: Baseline with budget only (R² ~0.54 observed in EDA)
2. **Random Forest**: Main model (target R² > 0.70-0.75)
3. **XGBoost**: Alternative if RF insufficient
4. **Ridge**: Handle multicollinearity

**Baseline established**: Budget alone achieves R²=0.54. Goal is to improve to R² > 0.70 by adding genre, timing, cast/crew features.

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
- ✅ Worldwide box office (domestic + international)
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

1. **Data Collection** ✅
   - TMDB API calls, Box Office Mojo scraping completed

2. **Cleaning & EDA** 🔄
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

---

## Note on Documentation Strategy
This project uses **Obsidian** for detailed notes, planning, and documentation. The Obsidian folder (`/Users/ndemoro/Desktop/FOLDERS/Nate_Obsidian/Movie_project_folder`) contains:
- Detailed project plans and analysis
- Meeting notes and decisions
- Research and references
- Iteration logs

**Syncing to GitHub**: Key documentation files are copied to the `docs/` folder and committed to version control. To sync updates:
```bash
# Copy notes to docs folder
cp /Users/ndemoro/Desktop/FOLDERS/Nate_Obsidian/Movie_project_folder/*.md docs/
# OR use the sync script
./sync_obsidian_notes.sh

# Then commit
git add docs/
git commit -m "Update documentation"
git push
```

This CLAUDE.md file serves as a condensed reference guide for AI assistants and quick project overview. For comprehensive documentation and planning materials, consult the Obsidian vault or the `docs/` folder.
