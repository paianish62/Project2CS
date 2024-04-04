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

gdp_test = {"United States": gdp_info["United States"]}
cpi_test = {"United States": cpi_info["United States"]}
sectors_test = sectors_info[sectors_info['Country/Economy'] == 'United States']
interest_test = interest[interest['Country Name'] == 'United States']
region_test = {"United States": region_development["United States"]}
sdg_test = {"United States": sdg_info["United States"]}
