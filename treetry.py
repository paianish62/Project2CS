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
from __future__ import annotations
from typing import Any, Optional, List
import load_data
import pandas as pd

gdp_info = load_data.load_stored_pickle('gdp.pickle')
cpi_info = load_data.load_stored_pickle('cpi.pickle')
sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
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


def classify_long_term_investments(gdp_info: Any) -> tuple[list, list]:
    """
    Classify countries based on their ave rage GDP growth rate from 1980 to 2019.

    Parameters:
    - gdp_info: pandas data frame

    Returns:
    - A list of country codes suitable for long-term investment.
    """

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
            long_term_investment_countries.append(country1)

        if not avg_growth_rate_st < 0:
            short_term_investment_countries.append(country1)

    return (long_term_investment_countries, short_term_investment_countries)


def map_countries_to_sectors(sectors_info, region_development):
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
        if row["Industry % of GDP"] > 25:
            sectors.append('Secondary')

        # Check if the country participates in the agriculture sector and add 'Primary' to the sectors list if true.
        if row['Agriculture % of GDP'] > 3:
            sectors.append('Primary')

        # Check if the country participates in the services sector and add 'Tertiary' to the sectors list if true.
        if row['Services % of GDP'] > 50:
            sectors.append('Tertiary')
        sectors_map[row['Country/Economy']] = sectors
    for cont in region_development:
        if cont not in sectors_map:
            sectors_map[cont] = ['primary', 'secondary', 'tertiary']

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
    min_val = series.min()
    max_val = series.max()

    # Check if the series is constant or all NaN; return the series unchanged or a default value
    if pd.isnull(min_val) or pd.isnull(max_val) or min_val == max_val:
        return series  # or any default value you deem appropriate

    # Perform normalization
    return 100 * (series - min_val) / (max_val - min_val)


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
        # GDP
        # Filter the GDP data for the desired period and calculate the growth rate
        period_gdp_df = gdp_df[(gdp_df['date'] >= 1980) & (gdp_df['date'] <= 2019)].copy()
        period_gdp_df['growth_rate'] = period_gdp_df['value'].pct_change().fillna(0)
        # Normalize the average GDP growth rate across the period for the country (also takes care of negative values)
        normalized_gdp_growth = normalize_series(period_gdp_df['growth_rate'].mean())

        # Inflation
        # Filter the CPI data for the desired period and calculate the growth rate
        period_cpi_df = cpi_info[country]
        period_cpi_df = period_cpi_df[(period_cpi_df['date'] >= 1980) & (period_cpi_df['date'] <= 2019)].copy()
        period_cpi_df['inflation_rate'] = period_cpi_df['value'].pct_change().fillna(0)
        normalized_cpi_inflation = 100 - normalize_series(period_cpi_df['inflation_rate'].mean())

        # Interest rates
        if country in interest_info['Country Name'].values:
            country_interest_df = interest_info[interest_info['Country Name'] == country]
            # Selecting years 1980 to 2019 and dropping NaN values for accurate mean calculation
            interest_rates = country_interest_df.loc[:, '1980':'2019'].dropna(axis=1)
            if not interest_rates.empty:
                average_interest_rate = interest_rates.mean(axis=1).values[0]
                normalized_interest_rate = 100 - normalize_series(average_interest_rate)
            else:
                normalized_interest_rate = 0  # Use 0 or an appropriate default value if no data is available
        else:
            normalized_interest_rate = 0  # Default value if the country is not found in the interest_info
        # SDG
        # Retrieve the SDG 8 score for the country
        sdg8_score = sum(sdg_info[country][8])/2

        # Calculate the combined economic score with assigned weights
        economic_score = (normalized_gdp_growth * 0.4) + \
                         (normalized_cpi_inflation * 0.2) + \
                         (normalized_interest_rate * 0.2) + \
                         (sdg8_score * 0.2)

        economic_performance_scores[country] = economic_score

    return economic_performance_scores


def add_countries_to_tree(dt: Tree, region_development, sectors_info, gdp_info, sdg_information,
                          priority) -> None:
    """
    Iterates over all countries and adds them to the tree based on various criteria including
    development status, region, sector participation, investment term (long/short run), and
    ethical category. The countries are organized within the tree to facilitate queries based
    on these criteria.

    Parameters:
    - dt: An instance of the Tree class where countries will be categorized and added.
    - country_info_df: DataFrame with columns for country name, emerging/developed status, and region.
    - sectors_info: DataFrame with information on the sectors (Primary, Secondary, Tertiary) each
    country participates in.
    - gdp_info: DataFrame with GDP growth rate information used for classifying countries into
     long/short investment terms.
    - sdg: List containing Sustainable Development Goals (SDG) scores for countries.
    - priority: List indicating the priority areas for ethical scoring, used to categorize countries ethically.
    - trends_rank: Dictionary mapping SDG scores to their improvement trends, used in ethical scoring.

    This function does not return anything but updates the tree in place by adding countries according
    to the specified criteria.
    """
    # Classify countries based on their investment potential (long-term vs short-term)
    long_term_countries, short_term_countries = classify_long_term_investments(gdp_info)
    # Map each country to the sectors it participates in
    sectors_map = map_countries_to_sectors(sectors_info, region_development)

    # Iterate over each country in the country information DataFrame
    for cont in region_development:
        country = cont

        # Development status (emerging/developed)'
        development_status = 'developed' if region_development[cont][1] == 1 else 'emerging'

        region = region_development[country][0]  # Geographical region

        # Determine the ethical category based on scoring
        ethical_category = 'good' if ethical_score(priority, sdg_information[country]) >= 50 else 'bad'

        # Determine the investment term based on classification
        investment_term = []
        if country in long_term_countries:
            investment_term.append('long run')
        if country in short_term_countries:
            investment_term.append('short run')

        # Retrieve the list of sectors the country is involved in
        country_sectors = sectors_map[country]

        # Add the country to the tree under each sector it participates in
        for sector in country_sectors:
            if 'long run' in investment_term:
                dt.add_country([(region.lower()), development_status.lower(), 'long run', sector.lower(),
                                ethical_category.lower()], country)
            if 'short run' in investment_term:
                dt.add_country([(region.lower()), development_status.lower(), 'short run', sector.lower(),
                                ethical_category.lower()], country)


def search_country(user_criteria, tree, lis, num) -> list:
    options = [["good", "bad"], ["emerging", "developing"], ["primary", "secondary", "tertiary"],
               ["long run", "short run"], ["europe", "asia", "oceania", "americas", "africa"]]
    if lis or num == 5:
        return lis
    else:
        crit = user_criteria[-1 - num]
        lis_temp = []
        for option in options:
            if crit in option:
                temp_option = option.copy()
                temp_option.remove(crit)
                for c in option:
                    user_criteria_temp = user_criteria.copy()
                    user_criteria_temp.remove(crit)
                    user_criteria_temp.insert(len(user_criteria_temp) - num, c)
                    lis_temp.extend(tree.query(user_criteria_temp))
        return search_country(user_criteria, tree, lis_temp, num + 1)


def main_func(country_info_df, sectors_info, gdp_info, sdg_information, priority, user_criteria,
              cpi_info, interest_info) -> list[dict[str| Any, list[int]] | int]:
    """
    Main function which creates tree and returns ranked list of countries to user
    """
    output = {}
    dt = Tree()
    add_countries_to_tree(dt, country_info_df, sectors_info, gdp_info, sdg_information, priority)
    criteria = user_criteria + ['good']
    unranked_countries = dt.query(criteria)
    country_scores_dict = calculate_economic_performance(gdp_info, cpi_info, interest_info, sdg_information)
    recurse = 0
    if not unranked_countries:
        new_country_list = search_country(criteria, dt, [], 0)
        # new_country_list = []
        if not new_country_list:
            top_5_countries = sorted(country_scores_dict.items(), key=lambda x: x[1], reverse=True)[:5]
            output = {}
            recurse = 2
            for cont in top_5_countries:
                output[cont[0]] = [country_scores_dict[cont[0]], ethical_score(priority,sdg_information[cont[0]])]
        else:
            new_country_list = set(new_country_list)
            new_country_list = list(new_country_list)
            recurse = 1
            for country in new_country_list:
                output[country] = [country_scores_dict[country], ethical_score(priority, sdg_information[country])]
    else:
        for country in unranked_countries:
            output[country] = [country_scores_dict[country], ethical_score(priority, sdg_information[country])]
    return [output, recurse]

if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120
    })


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': [],
        'allowed-io': [],
        'max-line-length': 120
    })
