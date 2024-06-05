import pandas as pd
import os

# dictionary to clean up spelling
state_cleanup = {
    'Johor' : ['johor bahru', 'johor bahru darul takzim', 'johor bharu'],
    'Kelantan' : ['kelatan'],
    'Terengganu' : ['kuala terengganu', 'terengganu', 'terengaganu', 'teregganu', 'terangganu', 'terenganu'],
    'Kuala Lumpur': ['kuala kunpur', 'kuala kumpur', 'kula lumpur', 'kuala lumpu', 'kuala lunpur', 'uala lumpur', 'wp kuala lumpur',
                     'wilayah persekutuan kuala lumpur', 'kuala lumpu', 'kl', 'kluala lumpur'],
    'Negeri Sembilan' : ['negeri seremban'],
    'Pulau Pinang' : ['penang'],
    'Sarawak' : ['sarawaka'],
    'Selangor' : ['sealangor', 'selangor darul ehsan', 'selongor'],
    'Putrajaya' : ['wp putrajaya'],
    'Labuan' : ['wp labuan']
}

# list of state name malaysia state name
malaysia_state = [
    'pulau pinang', 'kedah', 'kelantan', 'terengganu', 'pahang', 'perak', 'selangor', 'kuala lumpur',
    'putrajaya', 'negeri sembilan', 'melaka', 'johor', 'labuan', 'sabah', 'sarawak', 'perlis'
]


# list of country name
country_list = ['brunei', 'malaysia', 'usa']

def main():
    print('Read files')
    # get folder path
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\clean_address_project\data'

    # get file name
    file_name1 = 'All Address Converted.xlsx'
    file_name2 = 'Malaysia Postcode Simplified.xlsx'

    # create file path
    file_path1 = os.path.join(folder_path, file_name1)
    file_path2 = os.path.join(folder_path, file_name2)

    # read file and set data type
    df = pd.read_excel(file_path1, dtype={'Mailing City' : str, 'Mailing State/Province' : str ,'Mailing Zip/Postal Code' : str, 'Mailing Country' : str})
    df1 = pd.read_excel(file_path2, dtype={'Zipcode': str, 'State': str})

    # turn df1 to dictionary
    zipcode_dict = pd.Series(df1['State'].values, index=df1['Zipcode']).to_dict()

    print('Create new columns')
    # create new updated columns
    df['Updated City'] = df['Mailing City']
    df['Updated State'] = df['Mailing State/Province']
    df['Updated Zip'] = df['Mailing Zip/Postal Code']
    df['Updated Country'] = df['Mailing Country']

    print('Rearrange column')
    # rearrange column
    new_column_order = [
        'Supporter ID','Mailing Street','Mailing City','Updated City','Mailing Zip/Postal Code','Updated Zip','Mailing State/Province','Updated State','Mailing Country','Updated Country',
        'Rollup Summary: First Campaign: Campaign Name'
    ]

    df = df[new_column_order]

    # list of columns to clean
    to_clean_columns = ['Updated City','Updated State','Updated Zip','Updated Country']
    mystery_character = '，'

    print('Clean column')
    # clean space, comma, period, mystery character
    df[to_clean_columns] = df[to_clean_columns].apply(lambda x : x.str.replace('.', '').str.replace(',','') if x.dtype == 'object' else x)
    df[to_clean_columns] = df[to_clean_columns].apply(lambda x : x.str.strip() if x.dtype == 'object' else x)
    df[to_clean_columns] = df[to_clean_columns].apply(lambda x : x.str.replace(mystery_character, '') if x.dtype == 'object' else x)
    df[to_clean_columns] = df[to_clean_columns].apply(lambda x : x.str.lower() if x.dtype == 'object' else x)

    print('Fix spelling')
    # clean spelling in state
    def clean_state(row):
        for state, words in state_cleanup.items():
            for word in words:
                if word in row:
                    return state
        return row


    df['Updated State'] = df['Updated State'].fillna('').apply(lambda x : clean_state(x))

    print('Populate wilayah persekutuan from city to state')
    # populate wilayah persekutuan in state with data from mailing city
    mask1 = df['Updated State'] == 'wilayah persekutuan'
    df.loc[mask1, 'Updated State'] = df.loc[mask1, 'Updated City']

    print('Capitalize first alphabet')
    df[to_clean_columns] = df[to_clean_columns].apply(lambda x : x.str.title() if x.dtype == 'object' else x)

    df['Mailing Street'] = df['Mailing Street'].fillna('')

    print('Saving File')
    new_file_path = os.path.join(folder_path, 'result.xlsx')
    df.to_excel(new_file_path, index=False)

    print('File has been saved')


if __name__ == '__main__':
    main()


# populate wpersekutuan in state with data from mailing city
#mask2 = df['MailingState'] == 'wpersekutuan'
#df.loc[mask2, 'MailingState'] = df.loc[mask2, 'MailingCity']

# move country name in state column and delete country name in state column
#mask3 = df['MailingState'].isin(country_list)
#df.loc[mask3, 'MailingCountry'] = df.loc[mask3, 'MailingState']
#df.loc[mask3, 'MailingState'] = ''

# delete malaysian state that in country column
#mask4 = df['MailingCountry'].isin(malaysia_state)
#df.loc[mask4, 'MailingCountry'] = ''

# move state name in city column then delete state name in city column
#mask5 = df['MailingCity'].isin(malaysia_state)
#df.loc[mask5, 'MailingState'] = df.loc[mask5, 'MailingCity']
#df.loc[mask5, 'MailingCity'] = ''

# move country name in city column
#country_in_city = df['MailingCity'].isin(country_list)
#df.loc[country_in_city, 'MailingCountry'] = df.loc[country_in_city, 'MailingCity']
#df.loc[country_in_city, 'MailingCity'] = ''

# move non state name into new column
#df['MailingCity2'] = df['MailingState']
#non_state_name = ~ df['MailingState'].isin(malaysia_state)
#df.loc[non_state_name, 'MailingCity2'] = df.loc[non_state_name, 'MailingState']
#df.loc[non_state_name, 'MailingState'] = ''






#df['MailingState'] = df['MailingPostalCode'].map(zipcode_dict)





