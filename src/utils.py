from matplotlib.colors import LinearSegmentedColormap
from typing import Dict, Union, List, Tuple
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from scipy.stats import t
import seaborn as sns
import numpy as np
import requests
import random
import time
import re

def get_headers():
    """Returns a dictionary of headers with a randomly selected User-Agent"""
    # List of common User-Agent strings
    user_agents = [
        # Chrome on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        
        # Firefox on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        
        # Safari on macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_2_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
        
        # Chrome on macOS
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        
        # Edge on Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
        
        # Chrome on Android
        'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13; SM-S901B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
        
        # Safari on iOS
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 17_2_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1'
    ]
    
    # Common headers that most browsers send
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',  # Do Not Track
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0'
    }
    
    return headers


def make_request(url, delay=True):
    """
    Makes a request with random headers and optional delay
    
    Args:
        url (str): URL to request
        delay (bool): Whether to add a random delay between requests
    
    Returns:
        requests.Response object
    """
    if delay:
        time.sleep(random.uniform(.5, 1.5))
    
    headers = get_headers()
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None


def extract_boxscore_links(soup) -> Dict[int, List[str]]:
    """
    Extract boxscore links from the NFL schedule HTML content.
    
    Args:
        html_content (str): HTML content of the schedule page
        
    Returns:
        Dict[int, List[str]]: Dictionary mapping week numbers to lists of boxscore links
    """
    schedule_data = {}
    
    # Find all week dividers
    week_divs = soup.find_all('div', class_='ltbluediv')
    
    for week_div in week_divs:
        # Extract week number from the div header
        week_header = week_div.find(text=re.compile(r'Week \d+'))
        if not week_header:
            continue
            
        week_num = int(re.search(r'Week (\d+)', week_header).group(1))
        
        # Find the next table after the week header
        table = week_div.find_next('table')
        if not table:
            continue
            
        # Extract all boxscore links from the table
        boxscore_links = []
        for row in table.find_all('tr'):
            box_cell = row.find_all('td')[-1] if row.find_all('td') else None
            if box_cell and box_cell.find('a'):
                link = box_cell.find('a').get('href')
                if link and 'boxscore' in link:
                    # Add domain if the link is relative
                    if link.startswith('/'):
                        
                        link = f"https://www.footballdb.com/{link}"
                    boxscore_links.append(link)
        
        if boxscore_links:
            schedule_data[week_num] = boxscore_links
    
    return schedule_data


def extract_score_row_data(row) -> Tuple[str, List[int]]:
    """
    Extract team name and scores from a table row.
    
    Args:
        row: BeautifulSoup table row element
        
    Returns:
        Tuple containing team name and list of quarter scores
    """
    cells = row.find_all('td')
    
    # Extract team name from first cell, removing any extra whitespace and asterisks
    team_name = cells[0].text.strip().replace('*', '').strip()
    
    # Extract scores from remaining cells
    scores = []
    for cell in cells[1:]:  # Skip first cell (team name)
        # Extract number, handling both regular and bold scores
        score_text = cell.text.strip().replace('*', '')
        if score_text:
            try:
                scores.append(int(score_text))
            except ValueError:
                continue
                
    return team_name, scores


def get_boxscore(soup) -> Dict[str, Union[str, int]]:
    """
    Parse NFL boxscore HTML and return structured dictionary of game data.
    
    Args:
        html_content (str): Raw HTML content of boxscore page
        
    Returns:
        Dictionary containing structured game data
    """
    score_rows = soup.find_all('tr', class_='row0 center')
    
    away_team, away_scores = extract_score_row_data(score_rows[0])
    home_team, home_scores = extract_score_row_data(score_rows[1])
    
    # Create result dictionary
    result = {
        "home_team": home_team,
        "home_q1": home_scores[0],
        "home_q2": home_scores[1],
        "home_q3": home_scores[2],
        "home_q4": home_scores[3],
        "home_q5": home_scores[4] if len(home_scores) > 4 else 0,  # OT quarter if exists
        "home_final": home_scores[-1],  # Last score is final
        
        "away_team": away_team,
        "away_q1": away_scores[0],
        "away_q2": away_scores[1],
        "away_q3": away_scores[2],
        "away_q4": away_scores[3],
        "away_q5": away_scores[4] if len(away_scores) > 4 else 0,  # OT quarter if exists
        "away_final": away_scores[-1]  # Last score is final
    }
    
    return result

def winner_winner_chicken_dinner(scores):
    """
    Returns the ones digits of the home and away scores for each quarters 1, 2, and 3, and the final score.

    Parameters:
        scores (pandas.Series): A df row with data from one game.
                       
    Returns:
        tuple: A tuple of tuples, each containing the ones digits for (home, away) in q1, q2, q3, and final.
    """
    q1 = (scores["home_q1"] % 10, scores["away_q1"] % 10)
    q2 = (scores["home_q2"] % 10, scores["away_q2"] % 10)
    q3 = (scores["home_q3"] % 10, scores["away_q3"] % 10)
    final = (scores["home_final"] % 10, scores["away_final"] % 10)
    
    return q1, q2, q3, final


def create_frequency_matrices(df):
    """
    Creates frequency matrices of winning squares for each quarter across all games.

    Parameters:
        df (pd.DataFrame): DataFrame of game data.

    Returns:
        np.ndarray: Shape (4, 10, 10), with a 10x10 matrix for each quarter showing winning square frequencies.
    """
    # create maatrix representing game board
    freq_boards = np.zeros(shape=(4, 10, 10))
    # get winning squares for each game and each quarter
    winners = df.apply(winner_winner_chicken_dinner, axis=1)
    
    # per quarter, update freq for each winning square
    for quarter in range(4):
        # get winners for each quarter for all games
        quarter_ind = np.array([w[quarter] for w in winners])
        
        # build frequencies
        np.add.at(freq_boards[quarter], (quarter_ind[:, 0], quarter_ind[:, 1]), 1)

    # replace zeroes with 1
    freq_boards = np.where(freq_boards == 0, 1, freq_boards)

    
    return freq_boards.astype(int)

def create_fair_value_matrices(mat, board_value):
    # probability matrices
    probability_matrices = np.empty(shape=(4, 10, 10))
    
    for i in range(mat.shape[0]):
            cumulative_sum = mat[i].sum()
            probability_matrices[i] = mat[i] / cumulative_sum
    
    # fair value matrices
    fair_value_matrices = probability_matrices * board_value
    
    return fair_value_matrices


def create_hm(mat, title, save_name, colors, fmt = "d"):
    mid_value = np.median(mat[3])
    cmap = LinearSegmentedColormap.from_list("GoldToWhite", colors)

    title = title

    plt.figure(figsize=(13.7, 10.96))

    plt.rcParams['font.family'] = 'Palatino'
    
    sns.heatmap(mat[3], annot=True, annot_kws={"size": 20}, fmt=fmt, cmap=cmap, center=mid_value,
            cbar=True, square=True, linewidths=0.5)

    plt.imshow(mat[3], cmap=cmap, vmin=0, vmax=6)

    plt.title(title, fontname="Palatino", fontsize=20)
    plt.xlabel("Away Team", fontsize=20)
    plt.ylabel("Home Team", fontsize=20)
    plt.tick_params(axis='both', which='major', labelsize=20)

    plt.tight_layout()
    plt.savefig(f"data/{save_name}.png")
    return plt


def custom_ttest(mat, k):
    flat_ind = np.argpartition(np.abs(mat).flatten(), -k)[-k:]
    indices_2d = np.array(np.unravel_index(flat_ind, np.abs(mat).shape)).T
    top_diffs = mat[tuple(indices_2d.T)]
    
    mean_diff = np.mean(top_diffs)
    std_dev_full = np.std(mat, ddof=1)
    n = len(top_diffs)

    t_stat = mean_diff / (std_dev_full / np.sqrt(n))

    p_value = 2 * t.sf(np.abs(t_stat), df=n-1)

    return t_stat, p_value