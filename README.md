# Movie Box Office Revenue Prediction

A machine learning project that predicts movie box office revenue using pre-release data including budget, cast, genre, release timing, and marketing metrics.

## Project Overview

This project builds predictive models to forecast movie box office performance based on information available before a film's release. The goal is to help studios and investors make better decisions by predicting opening weekend and total domestic gross revenue.

**Key Features:**
- Predicts total domestic box office revenue
- Analyzes 2,500+ movies from 2010-2024
- Combines multiple data sources (TMDB, Box Office Mojo, YouTube)
- Advanced feature engineering including star power metrics and competition analysis
- Compares multiple ML algorithms (Linear Regression, Random Forest, XGBoost)

## Project Structure

```
Movie_Box_Office_Success/
├── data/
│   ├── raw/                    # Raw data from APIs and web scraping
│   └── processed/              # Cleaned and processed datasets
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_data_cleaning_eda.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_modeling.ipynb
│   └── 05_evaluation_insights.ipynb
├── scripts/                    # Reusable Python scripts
├── models/                     # Saved model files
├── visualizations/             # Generated plots and charts
├── requirements.txt
├── plan.md
└── README.md
```

## Data Sources

1. **TMDB (The Movie Database) API** - Movie metadata including budget, cast, crew, genres, runtime, release dates
2. **Box Office Mojo** - Actual box office revenue data (web scraping)
3. **OMDb API** - Supplemental metadata and IMDb ratings
4. **YouTube Data API** - Trailer view counts and engagement metrics

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- API keys for TMDB, OMDb, and YouTube Data API

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/Movie_Box_Office_Success.git
cd Movie_Box_Office_Success
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up API Keys
Create a `.env` file in the project root:
```
TMDB_API_KEY=your_tmdb_api_key_here
OMDB_API_KEY=your_omdb_api_key_here
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**How to get API keys:**
- TMDB: [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)
- OMDb: [omdbapi.com/apikey.aspx](http://www.omdbapi.com/apikey.aspx)
- YouTube: [Google Cloud Console](https://console.cloud.google.com/)

### Step 5: Run the Notebooks
Open Jupyter and run the notebooks in order:
```bash
jupyter notebook
```

## Key Features Engineered

### Tier 1 Features
- **Budget & Production**: Budget, runtime, rating (G/PG/PG-13/R), genre, sequel status
- **Temporal**: Release month/quarter, summer/holiday release indicators
- **Cast & Crew**: Director average gross, lead actor average gross, number of A-list actors
- **Marketing**: Trailer views, days since trailer release
- **Competition**: Number of releases same weekend/month

### Tier 2 Features
- Budget categories, franchise indicators, genre counts
- Director-genre match, release month historical averages
- Franchise number and years since last installment

### Tier 3 Features
- 3D/IMAX availability, recent actor hits, director awards
- Language and production country metrics

## Model Performance

*Results will be updated after model training is complete*

| Model | R² Score | MAE ($M) | RMSE ($M) |
|-------|----------|----------|-----------|
| Linear Regression | TBD | TBD | TBD |
| Random Forest | TBD | TBD | TBD |
| XGBoost | TBD | TBD | TBD |
| Ridge Regression | TBD | TBD | TBD |

**Target Metrics:**
- R² > 0.70
- Mean Absolute Error (MAE) < $25M

## Key Insights

*This section will be populated with findings from the analysis, including:*
- Most important features for predicting box office success
- Relationship between budget and revenue
- Impact of release timing on performance
- Value of star power and franchise status
- Genre-specific patterns

## Technologies Used

**Programming & Analysis:**
- Python 3.8+
- Jupyter Notebook

**Data Manipulation:**
- pandas
- numpy

**Data Collection:**
- requests
- beautifulsoup4
- python-dotenv

**Visualization:**
- matplotlib
- seaborn

**Machine Learning:**
- scikit-learn
- xgboost

**Development Tools:**
- Git/GitHub
- Virtual Environment (venv)

## Methodology

### 1. Data Collection
- Collected data for 3,000 movies (2010-2024)
- Filtered for wide releases (1,000+ opening theaters)
- Merged data from multiple sources using IMDb IDs

### 2. Data Cleaning
- Handled missing values using median imputation by genre/year
- Removed duplicate entries
- Validated data ranges and fixed data type issues
- Dropped movies missing critical variables (budget or revenue)

### 3. Exploratory Data Analysis
- Analyzed distributions of key variables
- Identified correlations between features and revenue
- Examined seasonal patterns and genre performance
- Created visualizations to understand relationships

### 4. Feature Engineering
- Calculated historical averages for directors and actors
- Created temporal features (release timing indicators)
- Built competition metrics (concurrent releases)
- Engineered star power and franchise indicators

### 5. Model Training & Evaluation
- Time-based train/test split (2010-2021 train, 2022-2024 test)
- Trained multiple models with hyperparameter tuning
- Used 5-fold cross-validation
- Evaluated using R², MAE, and RMSE

## Future Improvements

- [ ] Add international box office predictions
- [ ] Incorporate social media sentiment analysis
- [ ] Build interactive Streamlit dashboard for predictions
- [ ] Add ensemble methods combining multiple models
- [ ] Adjust for inflation to improve temporal predictions
- [ ] Include critic review scores from Rotten Tomatoes/Metacritic
- [ ] Expand dataset to include 2000-2009 movies
- [ ] Develop separate models for opening weekend vs total gross

## Limitations

- Model performance depends on data quality and completeness
- Historical patterns may not perfectly predict future trends
- Does not account for unexpected events (pandemics, theater closures)
- Limited to wide theatrical releases in the US market
- Star power metrics based on past performance may not reflect current popularity

## Author

Nate Demoro

## License

This project is open source and available for educational purposes.

## Acknowledgments

- TMDB for providing comprehensive movie metadata
- Box Office Mojo for historical revenue data
- YouTube Data API for marketing metrics
