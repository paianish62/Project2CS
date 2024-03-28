import requests
import pandas as pd

API_KEY = "9afd106bb0146138b12fa9e6a1237c94"

countries_of_interest = {
    'United States' : 'US',
    'Canada' : 'CA',
    'Brazil' : 'BR',
    'Mexico' : 'MX',
    'Argentina' : 'AR',
    'Uraguay' : 'UY',
    'South Africa' : 'ZA',
    'Mauritius' : 'MU',
    'Botswana' : 'BW',
    'Australia' : 'AU',
    'New Zealand' : 'NZ',
    'Singapore' : 'SG',
    'China' : 'CN',
    'India' : 'IN',
    'Japan' : 'JP',
    'Russia' : 'RU',
    'South Korea' : 'KR',
    'Indonesia' : 'ID',
    'Saudi Arabia' : 'SA',
    'Qatar' : 'QA',
    'Turkey' : 'TR',
    'Oman' : 'OM',
    'Germany' : 'DE',
    'United Kingdom' : 'GB',
    'France' : 'FR',
    'Italy' : 'IT',
    'Spain' : 'ES',
    'Netherlands' : 'NL',
    'Switzerland' : 'CH',
    'Poland' : 'PL'
    }

sector_info_file = 'datasets/gdp_info.csv'
interest_info_file = 'datasets/interest_info.csv'

gdp_series_ids = {
    'USA': 'RGDPNAUSA666NRUG',
    'CAN': 'RGDPNACAA666NRUG',
    'BRA': 'RGDPNABRA666NRUG',
    'MEX': 'RGDPNAMXA666NRUG',
    'ARG': 'RGDPNAARA666NRUG',
    'URY': 'RGDPNAUYA666NRUG',
    'ZAF': 'RGDPNAZAA666NRUG',
    'MUS': 'RGDPNAMUA666NRUG',
    'BWA': 'RGDPNABWA666NRUG',
    'AUS': 'RGDPNAAUA666NRUG',
    'NZL': 'RGDPNANZA666NRUG',
    'SGP': 'RGDPNASGA666NRUG',
    'CHN': 'RGDPNACNA666NRUG',
    'IND': 'RGDPNAINA666NRUG',
    'JPN': 'RGDPNAJPA666NRUG',
    'RUS': 'RGDPNARUA666NRUG',
    'KOR': 'RGDPNAKRA666NRUG',
    'IDN': 'RGDPNAIDA666NRUG',
    'SAU': 'RGDPNASAA666NRUG',
    'QAT': 'RGDPNAQAA666NRUG',
    'TUR': 'RGDPNATRA666NRUG',
    'OMN': 'RGDPNAOMA666NRUG',
    'DEU': 'RGDPNADEA666NRUG',
    'GBR': 'RGDPNAGBA666NRUG',
    'FRA': 'RGDPNAFRA666NRUG',
    'ITA': 'RGDPNAITA666NRUG',
    'ESP': 'RGDPNAESA666NRUG',
    'NLD': 'RGDPNANLA666NRUG',
    'CHE': 'RGDPNACHA666NRUG',
    'POL': 'RGDPNAPLA666NRUG'
}

cpi_series_ids = {
    'USA': 'DDOE02USA086NWDB',
    'CAN': 'DDOE02CAA086NWDB',
    'BRA': 'DDOE02BRA086NWDB',
    'MEX': 'DDOE02MXA086NWDB',
    'ARG': 'DDOE02ARA086NWDB',
    'URY': 'DDOE02UYA086NWDB',
    'ZAF': 'DDOE02ZAA086NWDB',
    'MUS': 'DDOE02MUA086NWDB',
    'BWA': 'DDOE02BWA086NWDB',
    'AUS': 'DDOE02AUA086NWDB',
    'NZL': 'DDOE02NZA086NWDB',
    'SGP': 'DDOE02SGA086NWDB',
    'CHN': 'DDOE02CNA086NWDB',
    'IND': 'DDOE02INA086NWDB',
    'JPN': 'DDOE02JPA086NWDB',
    'RUS': 'DDOE02RUA086NWDB',
    'KOR': 'DDOE02KRA086NWDB',
    'IDN': 'DDOE02IDA086NWDB',
    'SAU': 'DDOE02SAA086NWDB',
    'QAT': 'DDOE02QAA086NWDB',
    'TUR': 'DDOE02TRA086NWDB',
    'OMN': 'DDOE02OMA086NWDB',
    'DEU': 'DDOE02DEA086NWDB',
    'GBR': 'DDOE02GBA086NWDB',
    'FRA': 'DDOE02FRA086NWDB',
    'ITA': 'DDOE02ITA086NWDB',
    'ESP': 'DDOE02ESA086NWDB',
    'NLD': 'DDOE02NLA086NWDB',
    'CHE': 'DDOE02CHA086NWDB',
    'POL': 'DDOE02PLA086NWDB'
}

def extract_year(year_string):
    return int(year_string[:4])

def extract_val(val_string):
    return float(val_string)

def fetch_fred_series(api_key, series_id):
    base_url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json"
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()['observations']
        country_df = pd.DataFrame(data)[['date', 'value']]
        country_df['date'] = country_df['date'].apply(extract_year)
        country_df['value'] = country_df['value'].apply(extract_val)
        return country_df
    else:
        print(f"Failed to fetch data for series {series_id}. Status code: {response.status_code}")
        return pd.DataFrame()

def load_all_series(api_key, series_ids):
    all_series_data = {}
    for country_code, series_id in series_ids.items():
        df = fetch_fred_series(api_key, series_id)
        all_series_data[country_code] = df
    return all_series_data

def extract_sector_gdp_percentage(csv_file_path, countries_of_interest):
    economic_data_df = pd.read_csv(csv_file_path)
    filtered_df = economic_data_df[economic_data_df['Country/Economy'].isin(countries_of_interest)]
    agriculture_percentage = filtered_df['Agriculture % of GDP'].apply(extract_val)
    industry_percentage = filtered_df['Industry % of GDP'].apply(extract_val)
    services_percentage = filtered_df['Services % of GDP'].apply(extract_val)
    sector_gdp_percentage_df = pd.DataFrame({
        'Country/Economy': filtered_df['Country/Economy'],
        'Agriculture % of GDP': agriculture_percentage,
        'Industry % of GDP': industry_percentage,
        'Services % of GDP': services_percentage
    })
    return sector_gdp_percentage_df.reset_index()

def extract_interest_time_series_data(csv_file_path, countries_of_interest, start_year=None, end_year=None):
    data_df = pd.read_csv(csv_file_path)
    
    filtered_df = data_df[data_df['Country Name'].isin(countries_of_interest)]
    print(filtered_df)
    # If year range is specified, filter the columns as well
    filtered_df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, inplace=True)
    if start_year and end_year:
        year_columns = [str(year) for year in range(start_year, end_year + 1)]
        columns_of_interest = ['Country Name'] + year_columns
        filtered_df = filtered_df[columns_of_interest]
    return filtered_df.reset_index()


print(extract_sector_gdp_percentage(sector_info_file, countries_of_interest))

# agr > 5, industry > 25, services > 50
# sdg - rank trends from 20 to 100 (multiples of 20) - average trend and current score
