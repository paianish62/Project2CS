from __future__ import annotations
from typing import Any, Optional, List
import load_data

"""
This file assess and categorizes countries for investment opportunities ,based on their economic performance and 
ethical standings. It features the implementation of a Tree data structure to organize countries according to various 
criteria, including GDP growth, CPI inflation, interest rates, sector participation, and Sustainable Development 
Goals (SDGs). Functions within this file handle the normalization of economic data, calculation of ethical 
scores, classification of countries into investment terms, and mapping of countries to their respective economic 
sectors. The goal is to provide a structured and queryabl representation of countries for informed investment 
decision-making.
Copyright © 2023 GeoInvest. All rights reserved.
"""

gdp_info = load_data.load_all_series(load_data.API_KEY, load_data.gdp_series_ids)
cpi_info = load_data.load_all_series(load_data.API_KEY, load_data.cpi_series_ids)
#sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
interest = load_data.extract_interest_time_series_data(load_data.interest_info_file, load_data.countries_of_interest)
region_development = load_data.extract_region_info(load_data.region_info_file, load_data.countries_of_interest)
sdg_info = load_data.extract_sdg_info(load_data.sdg_info_file, load_data.countries_of_interest)

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
            # If the criteria path is empty, add the country directly as a subtree.
            self._subtrees.append(Tree(country))
        else:
            # Find or create the subtree for the next criterion in the path.
            criterion = criteria_path[0]
            subtree = self._find_subtree(criterion)
            if subtree is None:
                subtree = Tree(criterion)
                self._subtrees.append(subtree)
                # Recursively add the country to the appropriate subtree.
            subtree.add_country(criteria_path[1:], country)

    def _find_subtree(self, criterion: str) -> Optional[Tree]:
        for subtree in self._subtrees:
            if subtree._root == criterion:
                return subtree
        return None

    def query(self, criteria_path: List[str]) -> List[str]:
        # If the criteria path is empty, return the roots of all subtrees (countries).
        if not criteria_path:
            return [subtree._root for subtree in self._subtrees]
        else:
            criterion = criteria_path[0]
            subtree = self._find_subtree(criterion)
            if subtree is not None:
                # Recursively query the matching subtree for the next criteria in the path.
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


def ethical_score(priority: list[str], sdg_information) -> int:
    """
    Calculates the ethical score based on user priorities and the trend for improvement of
    each SDG for a country

    Parameters:
    - priority: Priority of the different ethical areas given by the user (from 1 being the highest
    and 3 being the lowest)
    - sdg_information: The SDG scores and trends between 1-100 of a country

    Returns:
    - A dynamic ethical score calculated based on the user's preferences
    """
    environmental = 0
    equitable = 0
    labour_treatment = 0
    # Calculate the environmental score as the average of selected SDGs
    for i in [7, 11, 12, 13, 14, 15]:
        environmental += (sum(sdg_information[i]) / 2)
    environmental = environmental / 6

    for i in [5, 10, 16]:
        # Calculate the equitable score as the average of selected SDGs
        equitable += (sum(sdg_information[i]) / 2)
    equitable = equitable / 3

    for i in [1, 2, 3, 4, 6]:
        # Calculate the labour treatment score as the average of selected SDGs
        labour_treatment += (sum(sdg_information[i]) / 2)
    labour_treatment = labour_treatment / 5

    # Store the scores in a dictionary
    scores = {'env': environmental, 'equ': equitable, 'lab': labour_treatment}

    # Calculate the final score based on user priorities
    return (scores[priority[0]] * 0.4) + (scores[priority[1]] * 0.35) + (scores[priority[2]] * 0.25)


def classify_long_term_investments(gdp_info: Any, gdp_per_capita_info: Any) -> tuple[list, list]:
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
        # Filter data from 1980 to 2019 for both long-term and short-term analysis
        period_df_lt = df1[(df1['date'] >= 1980) & (df1['date'] <= 2019)].copy()
        period_df_st = df1[(df1['date'] >= 2014) & (df1['date'] <= 2019)].copy()

        # Calculate growth rates
        period_df_lt['growth_rate'] = period_df_lt['value'].pct_change() * 100
        period_df_st['growth_rate'] = period_df_st['value'].pct_change() * 100
        avg_growth_rate_lt = period_df_lt['growth_rate'].mean()
        avg_growth_rate_st = period_df_st['growth_rate'].mean()

        # Filter countries based on long-term/short-term growth criteria
        if avg_growth_rate_lt > 2:
            long_term_investment_temp.append(country1)

        if not avg_growth_rate_st < 0:
            short_term_investment_countries.append(country1)

    # Filter based on GDP per capita growth rate
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

    # Iterate over each row in the DataFrame to process each country's sector participation.
    for index, row in sectors_info.iterrows():
        sectors = []

        # Check if the country participates in the industry sector and add 'Secondary' to the sectors list if true.
        if row['industry']:
            sectors.append('Secondary')

        # Check if the country participates in the agriculture sector and add 'Primary' to the sectors list if true.
        if row['agriculture']:
            sectors.append('Primary')

        # Check if the country participates in the services sector and add 'Tertiary' to the sectors list if true.
        if row['services']:
            sectors.append('Tertiary')
        sectors_map[row['Country/Economy']] = sectors

    return sectors_map


def normalize_series(series):
    """
    Normalizes a pandas Series to a range between 0 and 100.

    This normalization method applies a linear transformation to the original
    data, ensuring that the minimum value of the series maps to 0, and the
    maximum value maps to 100.

    Parameters:
    - series: A pandas Series to be normalized.

    Returns:
    - A pandas Series where each value is normalized to a scale of 0 to 100.
    """
    # Subtract the minimum value in the series from every element. This shifts the series
    # such that its minimum value is now 0.
    # Divide the shifted series by the range (max - min) of the original series.
    # This scales the series to have a maximum value of 1.
    # Multiply by 100 to scale the series to a range between 0 and 100.
    return 100 * (series - series.min()) / (series.max() - series.min())


def calculate_economic_performance(gdp_info, cpi_info, interest_info, sdg_info) -> dict[str, int]:

    """
    Calculates the economic performance scores for each country based on normalized
    values of GDP growth rate, CPI inflation rate, interest rate, and SDG 8 scores.

    Parameters:
    - gdp_info: Dictionary of pandas DataFrames with GDP data for each country.
    - cpi_info: Dictionary of pandas DataFrames with CPI data for each country.
    - interest_info: Dictionary of pandas DataFrames with interest rate data for each country.
    - sdg_info: Dictionary of pandas DataFrames with SDG data for each country.

    Returns:
    - A dictionary mapping country codes to their economic performance scores.
    """
    economic_performance_scores = {}

    for country, gdp_df in gdp_info.items():
        #GDP
        # Filter the GDP data for the desired period and calculate the growth rate
        period_gdp_df = gdp_df[(gdp_df['date'] >= 1980) & (gdp_df['date'] <= 2019)].copy()
        period_gdp_df['growth_rate'] = period_gdp_df['value'].pct_change().fillna(0)
        # Normalize the average GDP growth rate across the period for the country (also takes care of negative values)
        normalized_gdp_growth = normalize_series(period_gdp_df['growth_rate'].mean())

        #Inflation
        # Filter the CPI data for the desired period and calculate the growth rate
        period_cpi_df = cpi_info[country]
        period_cpi_df = period_cpi_df[(period_cpi_df['date'] >= 1980) & (period_cpi_df['date'] <= 2019)].copy()
        period_cpi_df['inflation_rate'] = period_cpi_df['value'].pct_change().fillna(0)
        normalized_cpi_inflation = 100 - normalize_series(period_cpi_df['inflation_rate'].mean())

        #Interest rates
        # Filter the Intersest data for the desired period and calculate the growth rate
        period_interest_df = interest_info[country]
        period_interest_df = period_interest_df[
            (period_interest_df['date'] >= 1980) & (period_interest_df['date'] <= 2019)].copy()
        normalized_interest_rate = 100 - normalize_series(period_interest_df['value'].mean())

        #SDG
        # Retrieve the SDG 8 score for the country
        sdg8_score = sum(sdg_info[country][8])/2

        # Calculate the combined economic score with assigned weights
        economic_score = (normalized_gdp_growth * 0.4) + \
                         (normalized_cpi_inflation * 0.2) + \
                         (normalized_interest_rate * 0.2) + \
                         (sdg8_score * 0.2)

        economic_performance_scores[country] = round(economic_score)

    return economic_performance_scores


def add_countries_to_tree(dt: Tree, region_development, sectors_info, gdp_info, per_capita_info, sdg_information,
                          priority) -> None:
    """
    Iterates over all countries and adds them to the tree based on various criteria including
    development status, region, sector participation, investment term (long/short run), and
    ethical category. The countries are organized within the tree to facilitate queries based
    on these criteria.

    Parameters:
    - dt: An instance of the Tree class where countries will be categorized and added.
    - country_info_df: DataFrame with columns for country name, emerging/developed status, and region.
    - sectors_info: DataFrame with information on the sectors (Primary, Secondary, Tertiary) each country participates in.
    - gdp_info: DataFrame with GDP growth rate information used for classifying countries into long/short investment terms.
    - per_capita_info: DataFrame with GDP per capita growth rate information, also used for investment term classification.
    - sdg: List containing Sustainable Development Goals (SDG) scores for countries.
    - priority: List indicating the priority areas for ethical scoring, used to categorize countries ethically.
    - trends_rank: Dictionary mapping SDG scores to their improvement trends, used in ethical scoring.

    This function does not return anything but updates the tree in place by adding countries according to the specified criteria.
    """
    # Classify countries based on their investment potential (long-term vs short-term)
    long_term_countries, short_term_countries = classify_long_term_investments(gdp_info, per_capita_info)
    # Map each country to the sectors it participates in
    sectors_map = map_countries_to_sectors(sectors_info)

    # Iterate over each country in the country information DataFrame
    for cont in region_development:
        country = cont

        # Development status (emerging/developed)'
        development_status = 'Developed' if region_development[cont][1] == 1 else 'Emerging'

        region = region_development[cont][0] # Geographical region

        # Determine the ethical category based on scoring
        ethical_category = 'Good' if ethical_score(priority, sdg_information) >= 50 else 'Bad'

        # Determine the investment term based on classification
        investment_term = []
        if country in long_term_countries:
            investment_term.append('Long Run')
        if country in short_term_countries:
            investment_term.append('Short Run')

        # Retrieve the list of sectors the country is involved in
        country_sectors = sectors_map[country]

        # Add the country to the tree under each sector it participates in
        for sector in country_sectors:
            if 'Long Run' in investment_term:
                dt.add_country([region, development_status, sector, 'Long Run', ethical_category], country)
            if 'Short Run' in investment_term:
                dt.add_country([region, development_status, sector, 'Short Run', ethical_category], country)


def main_func(country_info_df, sectors_info, gdp_info, per_capita_info, sdg_information, priority, user_criteria,
              cpi_info, interest_info, sdg8_scores, goal_scores):
    """
    Main function which creates tree and returns ranked list of countries to user
    """
    output = {}
    dt = Tree()
    add_countries_to_tree(dt, country_info_df, sectors_info, gdp_info, per_capita_info, sdg_information, priority)
    unranked_countries = dt.query(user_criteria)
    country_scores_dict = calculate_economic_performance(gdp_info, cpi_info, interest_info, sdg8_scores)
    for country in unranked_countries:
        output[country] = [country_scores_dict[country], ethical_score(user_criteria, sdg_information)]

    return output

    # sorted_country_scores = sorted(country_scores_dict.items(), key=lambda x: x[1])
    # for country_and_rank in sorted_country_scores:
    #     if country_and_rank[1] in unranked_countries:
    #         ranked_countries.append(country_and_rank[1])
    #
    # return ranked_countries


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
# Doctests for main_func and economic score
# Output ka input: {'country':[*economic score*, *ethical score*]} /or/ {*rank*:['country', *economic score*, *ethical score*]}
