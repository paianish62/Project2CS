from __future__ import annotations
from typing import Any, Optional, List
import load_data

gdp_info = load_data.load_all_series(load_data.API_KEY, load_data.gdp_series_ids)
#cpi_info = load_data.load_all_series(load_data.API_KEY, load_data.cpi_series_ids)
#sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
#interest = load_data.extract_interest_time_series_data(load_data.interest_info_file, load_data.countries_of_interest)

class Tree:
    def __init__(self, root: Optional[Any] = None, subtrees: List[Tree] = None) -> None:
        self._root = root
        self._subtrees = subtrees if subtrees is not None else []

    def is_empty(self) -> bool:
        return self._root is None
# hi ravit
    def add_country(self, criteria_path: List[str], country: str):
        if not criteria_path:
            self._subtrees.append(Tree(country))
        else:
            criterion = criteria_path[0]
            subtree = self._find_subtree(criterion)
            if subtree is None:
                subtree = Tree(criterion)
                self._subtrees.append(subtree)
            subtree.add_country(criteria_path[1:], country)

    def _find_subtree(self, criterion: str) -> Optional[Tree]:
        for subtree in self._subtrees:
            if subtree._root == criterion:
                return subtree
        return None

    def query(self, criteria_path: List[str]) -> List[str]:
        if not criteria_path:
            return [subtree._root for subtree in self._subtrees]
        else:
            criterion = criteria_path[0]
            subtree = self._find_subtree(criterion)
            if subtree is not None:
                return subtree.query(criteria_path[1:])
            else:
                return []#changes

tree = Tree("World")
tree.add_country(["Europe", "Developed", "Tertiary", "Long Run"], "England")
tree.add_country(["Asia", "Emerging", "Primary", "Short Run"], "India")
print(tree.query(["Europe", "Developed", "Tertiary", "Long Run"]))

"""
(i) Environmental Score - 7, 11, 12, 13, 14 and 15
(ii) Equity Score - 5, 10 and 16
(iii) Fair Labour Treatment - 1, 2, 3, 4 and 6
"""
def ethical_score(priority: list[str], goal_scores: list[int]) -> int:
    environmental = (goal_scores[7] + goal_scores[11] + goal_scores[12] + goal_scores[13] + goal_scores[14] +
                     goal_scores[15])/6
    equitable = (goal_scores[5] + goal_scores[10] + goal_scores[16])/3
    labour_treatment = (goal_scores[1] + goal_scores[2] + goal_scores[3] + goal_scores[4] + goal_scores[6])/5
    scores = {'env': environmental, 'equ': equitable, 'lab': labour_treatment}
    return (scores[priority[0]])*0.4 + (scores[priority[1]])*0.35 + (scores[priority[2]])*0.25
#edit to include trends

def classify_long_term_investments(gdp_info):
    """
    Classify countries based on their average GDP growth rate from 1980 to 2019.

    Parameters:
    - gdp_info: pandas data frame

    Returns:
    - A list of country codes suitable for long-term investment.
    """
    long_term_investment_countries = []

    for country, df in gdp_info.items():
        period_df = df[(df['date'] >= 1980) & (df['date'] <= 2019)].copy()
        period_df['growth_rate'] = period_df['value'].pct_change() * 100
        avg_growth_rate = period_df['growth_rate'].mean()
        if avg_growth_rate > 2:
            long_term_investment_countries.append(country)

    return long_term_investment_countries


def map_countries_to_sectors(sectors_info):
    """
    Maps each country to the sectors it participates in based on a DataFrame.

    Parameters:
    - sectors_info: DataFrame with columns for country, industry, agriculture, and services,
                    where each row corresponds to a country and boolean values indicate participation.

    Returns:
    - A dictionary where each key is a country and the value is a list of sectors it participates in.
    """
    sectors_map = {}
    for index, row in sectors_info.iterrows():
        sectors = []
        if row['industry']:
            sectors.append('Secondary')
        if row['agriculture']:
            sectors.append('Primary')
        if row['services']:
            sectors.append('Tertiary')
        sectors_map[row['Country/Economy']] = sectors

    return sectors_map


def normalize_series(series):
    return 100 * (series - series.min()) / (series.max() - series.min())


def calculate_economic_performance(gdp_info, cpi_info, interest_info, sdg8_scores):
    economic_performance_scores = {}

    for country, gdp_df in gdp_info.items():
        #GDP
        period_gdp_df = gdp_df[(gdp_df['date'] >= 1980) & (gdp_df['date'] <= 2019)].copy()
        period_gdp_df['growth_rate'] = period_gdp_df['value'].pct_change().fillna(0)
        normalized_gdp_growth = normalize_series(period_gdp_df['growth_rate'].mean())

        #Inflation
        period_cpi_df = cpi_info[country]
        period_cpi_df = period_cpi_df[(period_cpi_df['date'] >= 1980) & (period_cpi_df['date'] <= 2019)].copy()
        period_cpi_df['inflation_rate'] = period_cpi_df['value'].pct_change().fillna(0)
        normalized_cpi_inflation = 100 - normalize_series(period_cpi_df['inflation_rate'].mean())

        #Interest rates
        period_interest_df = interest_info[country]
        period_interest_df = period_interest_df[
            (period_interest_df['date'] >= 1980) & (period_interest_df['date'] <= 2019)].copy()
        normalized_interest_rate = 100 - normalize_series(period_interest_df['value'].mean())

        #SDG
        sdg8_score = sdg8_scores[country][7]

        economic_score = (normalized_gdp_growth * 0.4) + \
                         (normalized_cpi_inflation * 0.2) + \
                         (normalized_interest_rate * 0.2) + \
                         (sdg8_score * 0.2)

        economic_performance_scores[country] = economic_score

    return economic_performance_scores


def add_countries_to_tree(tree: Tree, country_info_df, sectors_info, gdp_info, sdg, priority):
    """
    Iterates over all countries and adds them to the tree based on various criteria.

    Parameters:
    - tree: An instance of the Tree class to which countries will be added.
    - country_info_df: DataFrame with columns for country name, emerging/developed, and region.
    - sectors_info: DataFrame with information about which sectors countries participate in.
    - gdp_info: DataFrame with GDP growth rate information for classification of long/short run.
    - sdg: List containing SDG scores for countries.
    - priority: List containing priority areas for ethical scoring.

    The function does not return anything, but it updates the tree in place.
    """

    long_term_investment_countries = classify_long_term_investments(gdp_info)
    sectors_map = map_countries_to_sectors(sectors_info)

    for index, row in country_info_df.iterrows():
        country = row['Country Name']

        development_status = row['Developed']
        region = row['Region']

        ethical_category = 'Good' if ethical_score(priority, sdg) >= 50 else 'Bad'

        investment_term = 'Long Run' if country in long_term_investment_countries else 'Short Run'
#short run function
        country_sectors = sectors_map[country]

        for sector in country_sectors:
            if investment_term == 'Long Run':
                tree.add_country([region, development_status, sector, 'Long Run', ethical_category],
                                 country)
                tree.add_country([region, development_status, sector, 'Short Run', ethical_category],
                                 country)
#modify to include sr
            else:
                tree.add_country([region, development_status, sector, 'Short Run', ethical_category],
                                 country)



#tree = Tree("World")
#add_countries_to_tree(tree, country_info_df, sectors_info, gdp_info, sdg, priority)

#def economics_score(indicator:
# List Contries & Data on interest raes and SDGS
# for loop on the countries
# CPI, Interest Rates, GDP
# Ethical Score = 0.4(1) + 0.3(2) + 0.2(3) + 0.1(
#[equ, env, lab]

#Additional Stuff:
#Post Covid measurement
#Short Run, create function and change the three creating function
#Change ethical score (qualitative trends, score 1-100)
#Optional Test file with mini-datasets for doctest
