from module.county_list import country

def get_country_from_city_column(df):

    country_list = country()

    df['Mailing Country'] = df['Mailing City'].apply(lambda x: x if x in country_list else '')
    df['Mailing City'] = df['Mailing City'].apply(lambda x: '' if x in country_list else x)
    
    return df