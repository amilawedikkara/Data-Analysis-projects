import pandas as pd
import matplotlib.pyplot as plt

# =========================
# 1. Load datasets
# =========================

movies = pd.read_csv("tmdb_5000_movies.csv")
credits = pd.read_csv("tmdb_5000_credits.csv")

print("Movies dataset preview:")
print(movies.head())

print("\nCredits dataset preview:")
print(credits.head())

print("\nMovies shape:")
print(movies.shape)

print("\nCredits shape:")
print(credits.shape)

print("\nMovies columns:")
print(movies.columns)

print("\nCredits columns:")
print(credits.columns)

print("\nMovies info:")
movies.info()

print("\nCredits info:")
credits.info()


# =========================
# 2. Missing values and duplicates
# =========================

print("\nMissing values in movies:")
print(movies.isnull().sum())

print("\nMissing values in credits:")
print(credits.isnull().sum())

print("\nDuplicate movie IDs in movies:")
print(movies["id"].duplicated().sum())

print("\nDuplicate movie IDs in credits:")
print(credits["movie_id"].duplicated().sum())

print("\nDuplicate movie titles in movies:")
print(movies["title"].duplicated().sum())

print("\nDuplicate movie titles in credits:")
print(credits["title"].duplicated().sum())

print("\nDuplicate titles in movies:")
print(
    movies[movies["title"].duplicated(keep=False)]
    .sort_values("title")[["id", "title", "release_date"]]
)


# =========================
# 3. Validate relationship between movies and credits
# =========================

print("\nMovie IDs in movies but not in credits:")
print((~movies["id"].isin(credits["movie_id"])).sum())

print("\nMovie IDs in credits but not in movies:")
print((~credits["movie_id"].isin(movies["id"])).sum())


# =========================
# 4. Merge datasets
# =========================

movies_merged = movies.merge(
    credits,
    left_on="id",
    right_on="movie_id",
    how="inner",
    suffixes=("_movie", "_credit")
)

print("\nMerged dataset shape:")
print(movies_merged.shape)

print("\nMerged dataset columns:")
print(movies_merged.columns)


# =========================
# 5. Clean merged dataset
# =========================

# Drop duplicate columns that are no longer needed after a successful merge
movies_clean = movies_merged.drop(columns=["movie_id", "title_credit"])

# Rename title_movie back to title for easier analysis
movies_clean = movies_clean.rename(columns={"title_movie": "title"})

# Convert release_date from text/object to datetime
movies_clean["release_date"] = pd.to_datetime(
    movies_clean["release_date"],
    errors="coerce"
)

# Extract release year from release_date
movies_clean["release_year"] = movies_clean["release_date"].dt.year

# Create profit column
movies_clean["profit"] = movies_clean["revenue"] - movies_clean["budget"]

print("\nCleaned dataset shape:")
print(movies_clean.shape)

print("\nCleaned dataset columns:")
print(movies_clean.columns)

print("\nData types after cleaning:")
print(movies_clean[["release_date", "release_year", "budget", "revenue", "profit"]].dtypes)

print("\nMissing values after cleaning:")
print(movies_clean.isnull().sum())


# =========================
# 6. Check zero budget and zero revenue values
# =========================

print("\nMovies with zero budget:")
print((movies_clean["budget"] == 0).sum())

print("\nMovies with zero revenue:")
print((movies_clean["revenue"] == 0).sum())

print("\nMovies with both zero budget and zero revenue:")
print(((movies_clean["budget"] == 0) & (movies_clean["revenue"] == 0)).sum())


# =========================
# 7. Summary statistics
# =========================

numeric_columns = [
    "budget",
    "revenue",
    "profit",
    "runtime",
    "popularity",
    "vote_average",
    "vote_count",
    "release_year"
]

print("\nSummary statistics for selected numeric columns:")
print(movies_clean[numeric_columns].describe())


# =========================
# 8. Top movies
# =========================

print("\nTop 10 movies by revenue:")
print(
    movies_clean.sort_values("revenue", ascending=False)
    [["title", "release_year", "budget", "revenue", "profit"]]
    .head(10)
)

print("\nTop 10 movies by profit:")
print(
    movies_clean.sort_values("profit", ascending=False)
    [["title", "release_year", "budget", "revenue", "profit"]]
    .head(10)
)

print("\nTop 10 movies by budget:")
print(
    movies_clean.sort_values("budget", ascending=False)
    [["title", "release_year", "budget", "revenue", "profit"]]
    .head(10)
)

print("\nTop 10 movies by popularity:")
print(
    movies_clean.sort_values("popularity", ascending=False)
    [["title", "release_year", "popularity", "vote_average", "vote_count"]]
    .head(10)
)

print("\nTop 10 highest-rated movies with at least 1000 votes:")
popular_rated_movies = movies_clean[movies_clean["vote_count"] >= 1000]

print(
    popular_rated_movies.sort_values("vote_average", ascending=False)
    [["title", "release_year", "vote_average", "vote_count"]]
    .head(10)
)


# =========================
# 9. Basic yearly analysis
# =========================

yearly_revenue = (
    movies_clean.groupby("release_year")["revenue"]
    .sum()
    .sort_index()
)

yearly_profit = (
    movies_clean.groupby("release_year")["profit"]
    .sum()
    .sort_index()
)

print("\nTotal revenue by release year:")
print(yearly_revenue.tail(10))

print("\nTotal profit by release year:")
print(yearly_profit.tail(10))
