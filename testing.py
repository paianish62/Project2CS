import load_data
gdp_info = load_data.load_all_series(load_data.API_KEY, load_data.gdp_series_ids)
cpi_info = load_data.load_all_series(load_data.API_KEY, load_data.cpi_series_ids)
sectors_info = load_data.extract_sector_gdp_percentage(load_data.sector_info_file, load_data.countries_of_interest)
interest = load_data.extract_interest_time_series_data(load_data.interest_info_file, load_data.countries_of_interest)


def test_valid_economic_score():
    pass


def test_tree_creation():
    pass


def test_application_output():
    pass
