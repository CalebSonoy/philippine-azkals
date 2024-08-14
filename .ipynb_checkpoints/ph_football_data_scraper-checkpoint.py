# Import the libraries needed for scraping
import pandas as pd
import requests
from bs4 import BeautifulSoup

# All the Philippine National Football Team Results Pages in Wikipedia
azkals_results_urls = {"unofficial":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(unofficial_matches)",
                       "1913-1948":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(1913%E2%80%931948)",
                       "1950-1979":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(1950%E2%80%931979)",
                       "1980-1999":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(1980%E2%80%931999)",
                       "2000-2009":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(2000%E2%80%932009)",
                       "2010-2019":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(2010%E2%80%932019)",
                       "2020-Present":r"https://en.wikipedia.org/wiki/Philippines_national_football_team_results_(2020%E2%80%93present)"
                      }

# Initialize lists for placing column details
dates = []
competitions = []
home_teams = []
scores = []
away_teams = []
locations = []

# Extract HTML data from each page
for page in azkals_results_urls:
    html_text = requests.get(azkals_results_urls[page]).text
    soup = BeautifulSoup(html_text, 'lxml')
    results = soup.select('h2,div.vevent')

    # extract the details for each match in the page
    for result in results:
        if result.name == "h2":
            year = result.text.replace("[edit]", "").replace("Results", "")
        elif result.name == "div":
            try:
                date = result.table.tbody.tr.td.span.text.strip() + f" {year}"
            except AttributeError:
                date = None
            competition = result.table.tbody.tr.td.small.text.strip()
            home_team = result.table.tbody.tr.td.next_sibling.text.strip()
            score = result.table.tbody.tr.td.next_sibling.next_sibling.text.strip()
            away_team = result.table.tbody.tr.td.next_sibling.next_sibling.next_sibling.text.strip()
            location = result.table.tbody.tr.td.next_sibling.next_sibling.next_sibling.next_sibling.text.strip()

            # input details into lists
            dates.append(date)
            competitions.append(competition)
            home_teams.append(home_team)
            scores.append(score)
            away_teams.append(away_team)
            locations.append(location)

# place the data in a csv file
azkals_results = {"competition": competitions,
                "date": dates,
                "home_team": home_teams,
                "scores": scores,
                "away_team": away_teams,
                "location":locations,
                }
pd.DataFrame(azkals_results).to_csv("ph_national_football_team_results.csv", index=False)
