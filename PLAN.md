# Movie Box Office Prediction - Project Plan

## 1. Project Overview

**Goal:** Build a machine learning model to predict movie box office revenue (opening week and total domestic gross) based on pre-release data including budget, cast, genre, release timing, and marketing metrics.

**Why this matters:**
- Studios need revenue forecasts for investment decisions
- Demonstrates full data science workflow from collection to deployment
- Combines multiple data sources and complex feature engineering
- Real business application with measurable outcomes

**Target audience:** Movie studios, studio investors, data science hiring managers, recruiters, potential collaborators

---

## 2. Success Criteria

### Technical Metrics
- Model achieves R-squared greater than 0.70 on test set
- Mean Absolute Error (MAE) less than 25 million dollars
- Successfully collect data for at least 2,500 movies (2010-2024)
- Identify and validate top 5 most predictive features

### Deliverables
- Clean, well-documented Github repository
- 4-6 notebooks with code cells for interactive execution
- Comprehensive README with results and visualizations
- At least 3 compelling visualizations showing insights
- Optional: Simple Streamlit app for predictions

### Learning Outcomes
- Improve my API usage and web scraping
- Practice advanced feature engineering
- Compare multiple ML algorithms systematically
- Build portfolio piece that demonstrates full workflow

---

## 3. Data Collection Strategy

### 3.1 Primary Data Sources

**Source 1: TMDB (The Movie Database) API**
- **What:** Movie metadata including budget, cast, crew, genres, runtime, release dates
- **Access:** Free API key at themoviedb.org/setting/api
- **Rate limit:** 40 requests per 10 seconds
- **Endpoint:** `https://api.themoviedb.org/3/movie/{movie_id}`
- **Coverage:** Excellent for 2010+ films

**Source 2: Box Office Mojo**
- **What:** Actual box office revenue (opening weekend, total domestic, worldwide)
- **Access:** Web scraping (no official API)
- **URL pattern:** `boxofficemojo.com/title/tt{imdb_id}`
- **Method:** BeautifulSoup + requests
- **Note:** Respect robots.txt, add delays between requests

**Source 3: OMDb API (Backup/Supplement)**
- **What:** Additional metadata, IMDb ratings
- **Access:** Free tier allows 1,000 requests/day
- **Endpoint:** `http://www.omdbapi.com/?i={imdb_id}&apikey={key}`
- **Use case:** Fill gaps in TMDB data

**Source 4: YouTube Data API**
- **What:** Trailer view counts, engagement metrics
- **Access:** Free API keys via Google Cloud Console
- **Quota:** 10,000 units/day (sufficient for project)
- **Use case:** Marketing buzz indicator

### 3.2 Data Collection Step-by-Step

1. Set up API keys, test connections, explore data structure
2. Write scraping scripts with error handling and rate limiting
3. Collect TMDB data for 3,000 movies (2010-2024, major releases)
4. Scrape Box Office Mojo for revenue data, handling missing values
5. Collect YouTube trailer data for subset of movies

### 3.3 Target Dataset

**Size:** 2,500 - 3,000 movies after cleaning

**Time Range:** 2010-2024 (modern era, better data quality, avoids inflation complexity)

**Filters:**
- Wide releases only (1,000+ opening theaters)
- Exclude limited releases and documentaries
- Focus on theatrical releases (not streaming-first)
- Must have budget and revenue data (critical variables)

### 3.4 Data Storage

**Raw Data:** Save as CSV in `data/raw/` directory
- `movies_tmdb_raw.csv`
- `revenue_boxofficemojo_raw.csv`
- `trailers_youtube_raw.csv`

---

## 4. Feature Engineering Plan

### 4.1 Tier 1 Features

**Basic Movie Attributes:**
- Budget (numeric, millions)
- Runtime (numeric, minutes)
- Rating (categorical: G, PG, PG-13, R, NC-17)
- Genre_primary (categorical: Action, Comedy, Drama, etc.)
- Is_sequel (binary: 0 or 1)

**Temporal Features:**
- Release_month (numeric: 1-12)
- Release_quarter (categorical: Q1, Q2, Q3, Q4)
- Is_summer_release (binary: June, July, August)
- Is_holiday_release (binary: near Thanksgiving or Christmas)
- Day_of_week (categorical)

**Cast and Crew:**
- Director_avg_gross (numeric: historical average of director's films)
- Lead_actor_avg_gross (numeric: historical average of top billed actor)
- Num_a_list_actors (numeric: count of actors with avg gross > 100M)
- Cast_total_experience (numeric: sum of years active)

**Production:**
- Studio_tier (categorical: major studio vs independent)
- Production_company_count (numeric: number of production companies)

**Marketing:**
- Trailer_views (numeric: YouTube views, if available)
- Days_since_trailer (numeric: marketing runway)

**Competition:**
- Num_releases_same_weekend (numeric: count of wide releases)
- Num_opening_same_month (numeric: market saturation)

### 4.2 Tier 2 Features

- Budget_category (categorical: low, medium, high, tentpole based on quartiles)
- Genre_count (numeric: number of genres listed)
- Is_franchise (binary: part of established franchise)
- Franchise_number (numeric: which installment - 2, 3, 4, etc.)
- Years_since_last_installment (numeric: franchise fatigue indicator)
- Runtime_category (categorical: short, normal, long)
- Is_based_on_book (binary: adapted from literature)
- Is_based_on_comic (binary: Marvel, DC, etc.)
- Director_genre_match (binary: director's typical genre matches this film)
- Release_month_avg_revenue (numeric: historical average for that month)

### 4.3 Tier 3 Features

- Is_3d (binary: 3D release)
- Is_imax (binary: IMAX availability)
- Lead_actor_recent_hit (binary: star had hit in last 2 years)
- Director_awards (numeric: Oscar wins/nominations)
- Sentiment_trailer_comments (numeric: if doing NLP)
- Google_trends_score (numeric: search volume if available)
- Spoken_language_english (binary: English vs others)
- Production_countries_count (numeric: international co-production)

### 4.4 Feature Engineering Notes

**Star Power Index Calculation:**
- For each actor in top 3 billing: calculate average box office of their last 5 films
- Weight by recency (more recent films weighted higher)
- Cap at reasonable maximum to avoid outliers from ensemble casts

**Director Historical Average:**
- Calculate mean box office of director's previous films
- Exclude current film from calculation
- Handle first-time directors (assign category average or median)

**Competition Metrics:**
- Count number of wide releases (1000+ theaters) opening same weekend
- Weight by genre overlap (Action vs Action = high competition)
- Consider budget of competing films

---

## 5. Exploratory Data Analysis Plan

### 5.1 Data Quality Assessment

**Missing Values:**
- Identify percentage missing for each variable
- Decide on imputation strategy vs dropping rows
- Document decisions and rationale

**Outliers:**
- Box plots for numeric features (budget, revenue, runtime)
- Identify extreme values (Avatar, Endgame type outliers)
- Decide whether to keep, cap, or transform

**Data Types:**
- Ensure numeric columns are float/int
- Ensure dates are datetime objects
- Ensure categorical variables are properly encoded

### 5.2 Univariate Analysis

**For Numeric Variables:**
- Distribution plots (histograms)
- Summary statistics (mean, median, std, min, max, Q1, Q3, etc.)
- Check for skewness (revenue is likely right-skewed)

**For Categorical Variables:**
- Count plots showing frequency of each category
- Analyze balance (are all genres equally represented?)

### 5.3 Bivariate Analysis

**Key Relationships to Explore:**
- Budget vs revenue (scatter plot - expect strong positive correlation)
- Genre vs Average Revenue (bar chart - which genres perform best?)
- Release Month vs Revenue (look for seasonal patterns)
- Rating vs Revenue (does R rating hurt box office?)
- Sequel vs Original (do sequels make more money?)
- Star Power vs Revenue

### 5.4 Correlation Analysis

- Correlation matrix heatmap for all numeric features
- Identify highly correlated features (multicollinearity issues)
- Identify features with strong correlation to target (revenue)
- Document top 10 most correlated features

### 5.5 Key Questions to Answer in EDA

- What is the typical budget-to-revenue ratio?
- Which genre has the highest average revenue? Best ROI?
- What percentage of movies are profitable?
- How much does release timing matter?
- Do sequels reliably outperform originals?
- What's the relationship between runtime and revenue?
- Are there interaction effects? (e.g., high budget + action genre)

---

## 6. Data Cleaning Strategy

### 6.1 Missing Value Handling

**Budget (Critical variable):**
- If missing < 10% of rows, drop the rows
- If missing 10-30%: Impute with median by genre, year, director etc.
- Document all movies that were dropped

**Revenue (target variable):**
- Drop any movies with revenue missing
- This is the target variable - cannot predict without knowing the ground truth

### 6.3 Data Cleaning Checklist

- Remove exact duplicates
- Handle missing values with documented strategy (likely filling in with median value from that genre/director/cast etc.)
- Fix data type issues (strings to numbers, dates to datetime)
- Standardize categorical variables (USA vs US vs United States)
- Remove movies with missing target variable (revenue)
- Create binary indicators for missing data where appropriate
- Validate ranges (budget > 0, runtime between 60-240, etc.)
- Document all cleaning decisions in notebook

---

## 7. Modeling Strategy

### 7.1 Train/Test Split

**Approach:** Time-based split (not random)
- **Train:** 2010-2021 movies (approximately 70-75% of data)
- **Test:** 2022-2024 movies (approximately 25-30% of data)

**Rationale:** Simulates real prediction scenario (predicting future movies based on historical data)

**Alternative:** Random 80/20 split with stratification by genre

### 7.2 Target Variable

**Primary Target:** Total domestic box office gross (in millions)

**Consideration:** May need log transformation if highly skewed

**Secondary Target:** Opening weekend gross

### 7.3 Evaluation Metrics

**Primary Metrics:**
- R-squared (proportion of variance explained)
- Mean Absolute Error (MAE in millions)
- Root Mean Squared Error (RMSE - penalizes large errors)

**Success Threshold:**
- R-squared > 0.70
- MAE < $25M

**Why these metrics:** Regression problem with continuous target, need interpretable error in dollars

### 7.4 Models to Try

**Model 1: Linear Regression**
- **Purpose:** Baseline, interpretable
- **Preprocessing:** StandardScaler for numeric features, one-hot encoding for categorical
- **Expectation:** R-squared around 0.60-0.70
- **Advantage:** Simple, interpretable coefficients

**Model 2: Random Forest Regressor**
- **Purpose:** Likely best performer, handles non-linearity
- **Preprocessing:** Minimal (no scaling needed), encode categoricals as integers
- **Parameters to tune:** n_estimators, max_depth, min_samples_split
- **Expectation:** R-squared around 0.75-0.80
- **Advantage:** Feature importance, robust to outliers

**Model 3: Gradient Boosting (XGBoost)**
- **Purpose:** If Random Forest isn't sufficient
- **Preprocessing:** Similar to Random Forest
- **Parameters to tune:** learning_rate, max_depth, n_estimators
- **Expectation:** Similar or slightly better than Random Forest
- **Advantage:** Often best performance on tabular data

**Model 4: Ridge Regression**
- **Purpose:** Compare with linear regression, handles multicollinearity
- **Preprocessing:** Same as linear regression
- **Parameters to tune:** alpha (regularization strength)

### 7.5 Hyperparameter Tuning

**Method:** RandomizedSearchCV (faster than GridSearch)

**Cross-validation:** 5-fold cross-validation on training set

**For Random Forest:**
- n_estimators: [100, 200, 300, 500]
- max_depth: [10, 20, 30, None]
- min_samples_split: [2, 5, 10]
- min_samples_leaf: [1, 2, 4]

**For XGBoost:**
- learning_rate: [0.01, 0.05, 0.1, 0.3]
- max_depth: [3, 5, 7, 9]
- n_estimators: [100, 200, 300]
- subsample: [0.8, 1.0]

### 7.6 Feature Importance Analysis

After training best model:
- Extract feature importance scores
- Visualize top 15 most important features
- Validate against EDA findings (should align)
- Document surprising findings

### 7.7 Model Interpretation

**Key questions to answer:**
- Which features matter most for prediction?
- How does budget impact revenue? (linear? non-linear?)
- What's the value of having A-list actors?
- How much does release timing matter?
- Are sequels reliably more valuable?

---

## 8. Project Step-by-Step

### Step 1: Data Collection and Setup

**Step 1.1**
- Set up project structure (folders, PLAN.md, requirements.txt)
- Register for API keys (TMDB, OMDb, YouTube)
- Test API connections
- Write initial data collection functions

**Step 1.2**
- Collect TMDB data for 3,000 movies (2010-2024)
- Handle rate limiting and errors
- Save raw data to CSV
- Initial data inspection

**Step 1.3**
- Scrape Box Office Mojo revenue data
- Merge with TMDB data on IMDb ID
- Save combined raw dataset

### Step 2: Data Cleaning & Initial EDA

**Step 2.1**
- Load and inspect raw data
- Identify missing values, outliers, issues
- Document data quality problems
- Begin cleaning process

**Step 2.2**
- Complete data cleaning
- Handle missing values
- Create cleaned dataset
- Initial EDA: distributions, summary stats

**Step 2.3**
- Create initial visualizations
- Document key findings

### Step 3: Deep EDA & Feature Engineering

**Step 3.1**
- Bivariate analysis (feature vs revenue)
- Correlation analysis
- Identify patterns and insights
- Document findings

**Step 3.2**
- Engineer Tier 1 features (cast/crew metrics, temporal, competition)
- Calculate star power indices
- Create derived features
- Validate engineered features

**Step 3.3**
- EDA on engineered features
- Finalize feature set

### Step 4: Preprocessing & Baseline Modeling

**Step 4.1**
- Train/test split
- Encode categorical variables
- Scale features for linear models
- Prepare different preprocessing pipelines

**Step 4.2**
- Train Linear Regression (baseline)
- Evaluate on test set
- Document baseline performance
- Analyze residuals

**Step 4.3**
- Train Random Forest
- Initial hyperparameter tuning
- Compare to baseline

### Step 5: Model Optimization & Comparison

**Step 5.1**
- Systematic hyperparameter tuning for Random Forest
- Cross-validation
- Feature selection experiments
- Document best configuration

**Step 5.2**
- Train XGBoost model
- Hyperparameter tuning
- Compare all models
- Select best performer

**Step 5.3**
- Feature importance analysis
- Document model insights

### Step 6: Evaluation and Interpretation

**Step 6.1**
- Detailed evaluation of best model
- Error analysis (where does model fail?)
- Test on edge cases
- Validate assumptions

**Step 6.2**
- Create compelling visualizations (actual vs predicted, feature importance, etc.)
- Write interpretation of results
- Document limitations and potential improvements

**Step 6.3**
- Begin README.md
- Organize repository
- Clean up code

### Step 7: Document & Polish

**Step 7.1**
- Complete README with results
- Add docstrings to functions
- Ensure reproducibility (requirements.txt, clear instructions)

**Step 7.2**
- Create final presentation notebook
- Polish visualizations
- Write conclusions and future work section
- Test that someone else could run your code

**Step 7.3**
- Deploy simple Streamlit app
- OR create additional visualizations
- OR write blog post about findings

---

## 9. Deliverables Checklist

### Code & Repository
- [ ] Clean, organized GitHub repository
- [ ] 4-6 Jupyter notebooks
- [ ] requirements.txt with all dependencies
- [ ] Proper folder structure (data/, scripts/, models/)
- [ ] .gitignore (exclude large data files, API keys)

### Documentation
- [ ] Comprehensive README.md with:
  - Project overview
  - Key findings with visualizations
  - How to reproduce results
  - Technologies used
  - Future improvements
- [ ] PLAN.md file (updated with learnings)
- [ ] Docstrings in all functions
- [ ] Comments explaining complex logic

### Analysis Artifacts
- [ ] Cleaned dataset (or subset if too large)
- [ ] At least 5 compelling visualizations
- [ ] Feature importance plot
- [ ] Actual vs predicted scatter plot
- [ ] Model comparison table
- [ ] Saved best model (.pkl file)

---

## 10. Open Questions & Decisions

### Questions to Resolve During EDA
- Should I predict opening weekend or total gross?
- How to handle inflation? Adjust all revenue to 2024 dollars or use nominal value?
- Include international box office or domestic only?
- How to handle movies still in theaters (ongoing revenue)?
- Log-transform target variable or keep as-is?

### Technical Decisions
- Which preprocessing approach works best for Random Forest?
- Is feature scaling helping or hurting certain models?
- Should I drop highly correlated features or keep them?
- What threshold for dropping missing data?
- How many features is too many? (overfitting risk)

---

## 11. Resources & References

### Documentation
- TMDB API Docs: developers.themoviedb.org/3
- YouTube Data API: developers.google.com/youtube/v3
- Scikit-learn: scikit-learn.org/stable/
- XGBoost: xgboost.readthedocs.io

### Python Libraries Needed
- pandas, numpy (data manipulation)
- matplotlib, seaborn (visualization)
- scikit-learn (modeling, preprocessing)
- xgboost (gradient boosting)
- requests, beautifulsoup4 (web scraping)
- python-dotenv (API key management)
