from __future__ import annotations
from typing import Any, Optional, List
import load_data

gdp_info = load_data.load_all_series(load_data.API_KEY, load_data.gdp_series_ids)
# cpi_info = load_data.load_all_series(load_data.API_KEY, load_data.cpi_series_ids)
# sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
# interest = load_data.extract_interest_time_series_data(load_data.interest_info_file, load_data.countries_of_interest)


class Tree:
    """
    A recursive tree data structure.

    Representation Invariants:
        - self._root is not None or self._subtrees == []
        - all(not subtree.is_empty() for subtree in self._subtrees)
    """
    # Private Instance Attributes:
    #   - _root:
    #       The item stored at this tree's root, or None if the tree is empty.
    #   - _subtrees:
    #       The list of subtrees of this tree. This attribute is empty when
    #       self._root is None (representing an empty tree). However, this attribute
    #       may be empty when self._root is not None, which represents a tree consisting
    #       of just one item.
    _root: Optional[Any]
    _subtrees: list[Tree]

    def __init__(self, root: Optional[Any] = None, subtrees: List[Tree] = None) -> None:
        """Initialize a new Tree with the given root value and subtrees.

        If root is None, the tree is empty.

        Preconditions:
            - root is not none or subtrees == []
        """
        self._root = root
        self._subtrees = subtrees if subtrees is not None else []

    def is_empty(self) -> bool:
        """Return whether this tree is empty.

        >>> t1 = Tree(None, [])
         >>> t1.is_empty()
        True
        >>> t2 = Tree(3, [])
        >>> t2.is_empty()
        False
        """
        return self._root is None

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
                return []  # changes


tree = Tree("World")
tree.add_country(["Europe", "Developed", "Tertiary", "Long Run"], "England")
tree.add_country(["Asia", "Emerging", "Primary", "Short Run"], "India")
print(tree.query(["Europe", "Developed", "Tertiary", "Long Run"]))

"""
(i) Environmental Score - 7, 11, 12, 13, 14 and 15
(ii) Equity Score - 5, 10 and 16
(iii) Fair Labour Treatment - 1, 2, 3, 4 and 6
"""


def ethical_score(priority: list[str], goal_scores: list[int], trends_rank: dict[int, int]) -> int:
    """
    Calculates the ethical score based on user priorities and the trend for improvement of
    each SDG for a country

    Parameters:
    - priority: Priority of the different ethical areas given by the user (from 1 being the highest
    and 3 being the lowest)
    - goal_scores: The SDG scores between 1-100 of a country
    - trends_rank: Ranking of the trend of improvement in multiples of 20, from 20 to 100, stored in a dict
    mapping each SDG to its rank

    Returns:
    - A dynamic ethical score calculated based on the user's preferences
    """
    environmental = 0
    equitable = 0
    labour_treatment = 0
    for i in [7, 11, 12, 13, 14, 15]:
        environmental += ((goal_scores[i] + trends_rank[i]) / 2)
    environmental = environmental / 6

    for i in [5, 10, 16]:
        equitable += ((goal_scores[i] + trends_rank[i]) / 2)
    equitable = environmental / 3

    for i in [1, 2, 3, 4, 6]:
        labour_treatment += ((goal_scores[i] + trends_rank[i]) / 2)
    labour_treatment = labour_treatment / 5

    scores = {'env': environmental, 'equ': equitable, 'lab': labour_treatment}
    return (scores[priority[0]] * 0.4) + (scores[priority[1]] * 0.35) + (scores[priority[2]] * 0.25)


def classify_long_term_investments(gdp_info, gdp_per_capita_info) -> tuple[list, list]:
    """
    Classify countries based on their ave rage GDP growth rate from 1980 to 2019.

    Parameters:
    - gdp_info: pandas data frame

    Returns:
    - A list of country codes suitable for long-term investment.
    """

    long_term_investment_temp = []
    long_term_investment_countries = []
    short_term_investment_countries = []

    for country1, df1 in gdp_info.items():
        period_df_lt = df1[(df1['date'] >= 1980) & (df1['date'] <= 2019)].copy()
        period_df_st = df1[(df1['date'] >= 2014) & (df1['date'] <= 2019)].copy()
        period_df_lt['growth_rate'] = period_df_lt['value'].pct_change() * 100
        period_df_st['growth_rate'] = period_df_lt['value'].pct_change() * 100
        avg_growth_rate_lt = period_df_lt['growth_rate'].mean()
        avg_growth_rate_st = period_df_st['growth_rate'].mean()

        if avg_growth_rate_lt > 2:
            long_term_investment_temp.append(country1)

        if not avg_growth_rate_st < 0:
            short_term_investment_countries.append(country1)

    for country2, df2 in gdp_per_capita_info:
        per_capita = df2[(df2['date'] >= 1980) & (df2['date'] <= 2019)].copy()
        per_capita['growth_rate'] = per_capita['value'].pct_change() * 100
        per_capita_rate = per_capita['growth_rate'].mean()

        if per_capita_rate > 2 and country2 in long_term_investment_temp:
            long_term_investment_countries.append(country2)

    return (long_term_investment_countries, short_term_investment_countries)


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
    """
    Helper function that normalizes the series
    """
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


def add_countries_to_tree(dt: Tree, country_info_df, sectors_info, gdp_info, per_capita_info, sdg, priority, trends_rank):
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

    long_term_countries, short_term_countries = classify_long_term_investments(gdp_info, per_capita_info)
    sectors_map = map_countries_to_sectors(sectors_info)

    for index, row in country_info_df.iterrows():
        country = row['Country Name']

        development_status = row['Developed']
        region = row['Region']

        investment_term = []
        ethical_category = 'Good' if ethical_score(priority, sdg, trends_rank) >= 50 else 'Bad'

        if country in long_term_countries:
            investment_term.append('Long Run')
        if country in short_term_countries:
            investment_term.append('Short Run')

        country_sectors = sectors_map.get(country, [])

        for sector in country_sectors:
            if 'Long Run' in investment_term:
                dt.add_country([region, development_status, sector, 'Long Run', ethical_category], country)
            if 'Short Run' in investment_term:
                dt.add_country([region, development_status, sector, 'Short Run', ethical_category], country)


def main_func(country_info_df, sectors_info, gdp_info, per_capita_info, sdg, priority, trends_rank, user_criteria,
              cpi_info, interest_info, sdg8_scores):
    """
    Main function which creates tree and returns ranked list of countries to user
    """
    # Tree Creation
    ranked_countries = []
    dt = Tree()
    add_countries_to_tree(dt, country_info_df, sectors_info, gdp_info, per_capita_info, sdg, priority, trends_rank)
    unranked_countries = dt.query(user_criteria)
    country_scores_dict = calculate_economic_performance(gdp_info, cpi_info, interest_info, sdg8_scores)
    sorted_country_scores = sorted(country_scores_dict.items(), key=lambda x: x[1])
    for country_and_rank in sorted_country_scores:
        if country_and_rank[1] in unranked_countries:
            ranked_countries.append(country_and_rank[1])

    return ranked_countries


# tree = Tree("World")
# add_countries_to_tree(tree, country_info_df, sectors_info, gdp_info, sdg, priority)

# def economics_score(indicator:
# List Contries & Data on interest raes and SDGS
# for loop on the countries
# CPI, Interest Rates, GDP
# Ethical Score = 0.4(1) + 0.3(2) + 0.2(3) + 0.1(
# [equ, env, lab]

# Additional Stuff:
# Post Covid measurement
# Optional Test file with mini-datasets for doctest
# Output ka input: {'country':[*economic score*, *ethical score*]}
