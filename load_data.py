import requests
import pandas as pd

API_KEY = "9afd106bb0146138b12fa9e6a1237c94"

countries_of_interest = {
    'United States' : 'US',
    'Canada' : 'CA',
    'Brazil' : 'BR',
    'Mexico' : 'MX',
    'Argentina' : 'AR',
    'Uruguay' : 'UY',
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
sdg_info_file = 'datasets/sdg_info.csv'

gdp_series_ids = {
    'United States': 'RGDPNAUSA666NRUG',
    'Canada': 'RGDPNACAA666NRUG',
    'Brazil': 'RGDPNABRA666NRUG',
    'Mexico': 'RGDPNAMXA666NRUG',
    'Argentina': 'RGDPNAARA666NRUG',
    'Uruguay': 'RGDPNAUYA666NRUG',
    'South Africa': 'RGDPNAZAA666NRUG',
    'Mauritius': 'RGDPNAMUA666NRUG',
    'Botswana': 'RGDPNABWA666NRUG',
    'Australia': 'RGDPNAAUA666NRUG',
    'New Zealand': 'RGDPNANZA666NRUG',
    'Singapore': 'RGDPNASGA666NRUG',
    'China': 'RGDPNACNA666NRUG',
    'India': 'RGDPNAINA666NRUG',
    'Japan': 'RGDPNAJPA666NRUG',
    'Russia': 'RGDPNARUA666NRUG',
    'South Korea': 'RGDPNAKRA666NRUG',
    'Indonesia': 'RGDPNAIDA666NRUG',
    'Saudi Arabia': 'RGDPNASAA666NRUG',
    'Qatar': 'RGDPNAQAA666NRUG',
    'Turkey': 'RGDPNATRA666NRUG',
    'Oman': 'RGDPNAOMA666NRUG',
    'Germany': 'RGDPNADEA666NRUG',
    'United Kingdom': 'RGDPNAGBA666NRUG',
    'France': 'RGDPNAFRA666NRUG',
    'Italy': 'RGDPNAITA666NRUG',
    'Spain': 'RGDPNAESA666NRUG',
    'Netherlands': 'RGDPNANLA666NRUG',
    'Switzerland': 'RGDPNACHA666NRUG',
    'Poland': 'RGDPNAPLA666NRUG'
}

cpi_series_ids = {
    'United States': 'DDOE02USA086NWDB',
    'Canada': 'DDOE02CAA086NWDB',
    'Brazil': 'DDOE02BRA086NWDB',
    'Mexico': 'DDOE02MXA086NWDB',
    'Argentina': 'DDOE02ARA086NWDB',
    'Uruguay': 'DDOE02UYA086NWDB',
    'South Africa': 'DDOE02ZAA086NWDB',
    'Mauritius': 'DDOE02MUA086NWDB',
    'Botswana': 'DDOE02BWA086NWDB',
    'Australia': 'DDOE02AUA086NWDB',
    'New Zealand': 'DDOE02NZA086NWDB',
    'Singapore': 'DDOE02SGA086NWDB',
    'China': 'DDOE02CNA086NWDB',
    'India': 'DDOE02INA086NWDB',
    'Japan': 'DDOE02JPA086NWDB',
    'Russia': 'DDOE02RUA086NWDB',
    'South Korea': 'DDOE02KRA086NWDB',
    'Indonesia': 'DDOE02IDA086NWDB',
    'Saudi Arabia': 'DDOE02SAA086NWDB',
    'Qatar': 'DDOE02QAA086NWDB',
    'Turkey': 'DDOE02TRA086NWDB',
    'Oman': 'DDOE02OMA086NWDB',
    'Germany': 'DDOE02DEA086NWDB',
    'United Kingdom': 'DDOE02GBA086NWDB',
    'France': 'DDOE02FRA086NWDB',
    'Italy': 'DDOE02ITA086NWDB',
    'Spain': 'DDOE02ESA086NWDB',
    'Netherlands': 'DDOE02NLA086NWDB',
    'Switzerland': 'DDOE02CHA086NWDB',
    'Poland': 'DDOE02PLA086NWDB'
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

# {'Decreasing', 'Score moderately improving, insufficient to attain goal', 'On track or maintaining SDG achievement', 'Score stagnating or increasing at less than 50% of required rate', nan}

def extract_sdg_info(csv_file_path, countries_of_interest):
    sdg_data_df = pd.read_csv(csv_file_path)
    sdg_info_dict = {}
    for country in countries_of_interest:
        sdg_info_dict[country] = {}
        temp_df = sdg_data_df.loc[sdg_data_df['country_label'] == country].reset_index()
        for x in range(17):
            trendstr = 'Goal ' + str(x + 1) + ' Trend'
            scorestr = 'Goal ' + str(x + 1) + ' Score'
            trend = temp_df.iloc[0][trendstr]
            score = temp_df.iloc[0][scorestr]
            if trend == 'Decreasing':
                trend = 40
            elif trend == 'Score moderately improving, insufficient to attain goal':
                trend = 80
            elif trend == 'On track or maintaining SDG achievement':
                trend = 100
            elif trend == 'Score stagnating or increasing at less than 50% of required rate':
                trend = 60
            else:
                trend = 20
            try:
                score = int(score)
            except:
                score = -1
            sdg_info_dict[country][x + 1] = [trend, score]
    return sdg_info_dict

region_info_file = 'datasets/country_info.csv'

def extract_region_info(csv_file_path, countries_of_interest):
    region_data_df = pd.read_csv(csv_file_path)
    region_info_dict = {}
    for country in countries_of_interest:
        temp_df = region_data_df.loc[region_data_df['ISO Code (usa-census)'] == countries_of_interest[country]].reset_index()
        print(country)
        develop_status = temp_df.iloc[0]['Developed / Developing Countries (M49)']
        if develop_status == 'Developed':
            develop_status = 1
        else:
            develop_status = 0
        region_info_dict[country] = [temp_df.iloc[0]['Region Name_en (M49)'], develop_status]
    return region_info_dict

# agr > 5, industry > 25, services > 50
# sdg - rank trends from 20 to 100 (multiples of 20) - average trend and current score


'''
NEW DATA BELOW !!!!
'''
# region_development = load_data.extract_region_info(load_data.region_info_file, load_data.countries_of_interest)
# sdg_info = load_data.extract_sdg_info(load_data.sdg_info_file, load_data.countries_of_interest)
