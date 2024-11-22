# Football Squares Analysis

This repository contains the analysis and visualizations for the "Football Squares" project, exploring historical NFL scoring patterns and their implications for the popular Football Squares game. The project spans data collection, statistical analysis, and heatmap visualizations, providing insights into optimal square pricing, scoring trends, and the effects of NFL rule changes over time.

## Project Overview
Football Squares is a popular game where players choose squares on a grid, and winners are determined by the final digits of team scores. This project uses historical NFL data (1978–2023) to:
- Analyze scoring patterns and digit distributions.
- Determine fair value prices for each square.
- Evaluate biases (home vs. away teams) and adjust square prices accordingly.
- Examine the impact of the 1994 rule changes (e.g., the two-point conversion) on scoring trends.

## Repository Structure
/project-root
├── data/                     # Raw and processed datasets
│   ├── nfl box scores.csv     # Main dataset (1978–2023)
│   ├── nfl box scores 2.csv   # Pre-1994 dataset
├── src/                      # Utility functions
│   ├── utils.py               # Helper functions for analysis and visualization
├── plots/                    # Generated figures
│   ├── fig2_fig3_digits.png   # Figures 2 & 3: Digit distribution and frequency
│   ├── fig4_fig5_fig6.png     # Figures 4, 5, & 6: Square pricing and bias adjustments
├── data scraper.ipynb        # Notebook for data scraping from FootballDB
├── football squares.ipynb    # Main analysis notebook
└── README.md                 # This README file

## Data
The datasets used in this project were scraped from [FootballDB](https://www.footballdb.com). They include game-level data from 1978–2023, with fields such as:
- Team names (home and away).
- Quarterly scores and final scores.
- Game years and weeks.

## Key Analysis and Visualizations
1. **Frequency and Fair Value Matrices**:
   - Frequency matrices capture how often specific score combinations occur.
   - Fair value matrices assign monetary values to each square based on frequency.

2. **Figures**:
   - **Figure 2**: Heatmap of Football Squares frequencies (1978–2023).
   - **Figure 3**: Horizontal bar plot of digit distribution.
   - **Figure 4**: Optimal square prices calculated from historical data.
   - **Figure 5**: Bias-adjusted square prices to remove home/away discrepancies.
   - **Figure 6**: Bias-adjusted differences before and after 1994.

3. **Statistical Tests**:
   - Custom t-tests were performed to analyze:
     - Differences in square pricing before and after 1994.
     - Impact of home/away bias adjustments.

## Notebooks
### `data scraper.ipynb`
This notebook scrapes game data from FootballDB, processes it, and outputs CSV files used in the analysis.

### `football squares.ipynb`
The main analysis notebook covers:
- Data preprocessing and cumulative score calculations.
- Heatmap visualizations for frequency and fair value matrices.
- Statistical tests to evaluate rule changes and scoring trends.

## Setup Instructions
1. Clone this repository: git clone https://github.com/joerich1/Analytics-Day---Shared.git
2. Install the required Python packages: pip install -r requirements.txt
3. Run the Jupyter notebooks:
- Start Jupyter Notebook:
  ```
  jupyter notebook
  ```
- Open and execute the notebooks in the following order:
  1. `data scraper.ipynb` (to scrape or reprocess the raw data, if needed).
  2. `football squares.ipynb` (to reproduce the analysis and visualizations).

## Results and Key Insights
- **Digit Bias**: Digits like 0, 7, and 3 are more common due to typical scoring methods (e.g., touchdowns, field goals).
- **Home/Away Bias**: Biases in optimal square prices were identified and corrected.
- **Rule Changes**: The 1994 rule changes significantly altered scoring trends, as confirmed by statistical tests.

## Contact
For questions or collaborations, feel free to reach out:
- **Name**: Joseph Richardson
- **Email**: jrich256@students.kennesaw.edu
- **GitHub**: https://github.com/joerich1