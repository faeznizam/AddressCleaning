import pandas as pd
import logging
import os
import re
from state_zipcode import zipcode
import numpy as np

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# create dictionary with set to make searching faster
state_cleanup = {
    'johor': set([
        'johor bahru', 'johor bahru darul takzim', 'johor bharu'
        ]),
    'kelantan': set([
        'kelatan'
        ]),
    'terengganu': set([
        'kuala terengganu', 'terengganu', 'terengaganu', 'teregganu', 'terangganu', 'terenganu'
        ]),
    'kuala lumpur': set([
        'kuala kunpur', 'kuala kumpur', 'kula lumpur', 'kuala lumpu', 'kuala lunpur', 'uala lumpur', 'wp kuala lumpur',
        'wilayah persekutuan kuala lumpur', 'kuala lumpu', 'kl', 'kluala lumpur', 'kluala lumpur'
        ]),
    'negeri sembilan': set([
        'negeri seremban','nsembilan'
        ]),
    'penang': set([
        'pinang', 'pulang pinang', 'ppinang', 'pulau pinang'
        ]),
    'sarawak': set([
        'sarawaka'
        ]),
    'selangor': set([
        'sealangor', 'selangor darul ehsan', 'selongor', 'cyberjaya / selangor','selnagor'
        ]),
    'putrajaya': set([
        'wp putrajaya', 'wpputrajaya'
        ]),
    'labuan': set([
        'wp labuan', 'wplabuan'
        ]),
    'pahang' : set([
        'kuantan pahang', 'pahanag'
        ])
}

# list of country name
country_list = ['brunei', 'malaysia', 'usa', 'singapore']

# list of state name malaysia state name
malaysia_state = [
    'penang', 'kedah', 'kelantan', 'terengganu', 'pahang', 'perak', 'selangor', 'kuala lumpur',
    'putrajaya', 'negeri sembilan', 'melaka', 'johor', 'labuan', 'sabah', 'sarawak', 'perlis'
]

def main():
    logger.info('Starting the address cleaning script')

    # get file paths
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\AddressCleaning\test_data'
    all_address_filepath = os.path.join(folder_path, 'To clean - all address.csv')
    startwith_zero_filepath = os.path.join(folder_path, 'To clean - postal code starts with 0.xlsx' )

    logger.debug('Reading files')
    column_names = [
        'Supporter ID', 'Mailing Street', 'Mailing City', 'Mailing Zip/Postal Code', 
        'Mailing State/Province', 'Mailing Country', 'Rollup Summary: First Campaign: Campaign Name'
        ]
    all_address_df = pd.read_csv(all_address_filepath, encoding='latin1', dtype={col:str for col in column_names})
    startwith_zero_df = pd.read_excel(startwith_zero_filepath, dtype={col:str for col in column_names})

    logger.debug('Create comparison column')
    all_address_df['Updated City'] = all_address_df['Mailing City']
    all_address_df['Updated State'] = all_address_df['Mailing State/Province']
    all_address_df['Updated Zip'] = all_address_df['Mailing Zip/Postal Code']
    all_address_df['Updated Country'] = all_address_df['Mailing Country']
    startwith_zero_df['Updated City'] = startwith_zero_df['Mailing City']
    startwith_zero_df['Updated State'] = startwith_zero_df['Mailing State/Province']
    startwith_zero_df['Updated Zip'] = startwith_zero_df['Mailing Zip/Postal Code']
    startwith_zero_df['Updated Country'] = startwith_zero_df['Mailing Country']

    logger.debug('Rearrage column')
    new_column_order = [
        'Supporter ID','Mailing Street','Mailing City','Updated City','Mailing Zip/Postal Code','Updated Zip','Mailing State/Province','Updated State','Mailing Country','Updated Country',
        'Rollup Summary: First Campaign: Campaign Name'
    ]

    all_address_df = all_address_df[new_column_order]
    startwith_zero_df = startwith_zero_df[new_column_order]

    # clean comma and period
    logger.debug('Clean special character')
    columns_to_clean = ['Updated City','Updated State','Updated Zip','Updated Country']

    all_address_df[columns_to_clean] = all_address_df[columns_to_clean].apply(lambda x: x.str.lower())
    startwith_zero_df[columns_to_clean] = startwith_zero_df[columns_to_clean].apply(lambda x: x.str.lower())   
    
    # Define the pattern to match
    pattern = '[.,;?]'

    # Apply regex replacement
    all_address_df[columns_to_clean] = all_address_df[columns_to_clean].apply(lambda x: x.str.lower().replace(pattern, '', regex=True))
    startwith_zero_df[columns_to_clean] = startwith_zero_df[columns_to_clean].apply(lambda x: x.str.lower().replace(pattern, '', regex=True))

    logger.debug('Fix spelling')
    # fix spelling 
    def clean_state(row):
        
        for state, words in state_cleanup.items():
            if any(word in row for word in words):
                return state
        return row

    all_address_df['Updated State'] = all_address_df['Updated State'].fillna('').apply(clean_state)
    startwith_zero_df['Updated State'] = startwith_zero_df['Updated State'].fillna('').apply(clean_state)

    def clean_city(row):
        
        for city, words in state_cleanup.items():
            if any(word in row for word in words):
                return city
        return row

    all_address_df['Updated City'] = all_address_df['Updated City'].fillna('').apply(clean_city)
    startwith_zero_df['Updated City'] = startwith_zero_df['Updated City'].fillna('').apply(clean_city)
    
    logger.debug('Populate data from other column')
    # transfer data from another column based on word. 
    # replace wilayah persekutuan with data from mailing city
    def populate_data_from_other_column(df):
        condition1 = df['Updated State'] == 'wilayah persekutuan'
        df.loc[condition1, 'Updated State'] = df.loc[condition1, 'Updated City']

        condition2 = df['Updated State'] == 'wpersekutuan'
        df.loc[condition2, 'Updated State'] = df.loc[condition2, 'Updated City']

        # remove country name in state and delete
        condition3 = df['Updated State'].isin(country_list)
        df.loc[condition3, 'Updated Country'] = df.loc[condition3, 'Updated State']
        df.loc[condition3, 'Updated State'] = ''

        # delete state from country column
        condition4 = df['Updated Country'].isin(malaysia_state)
        df.loc[condition4, 'Updated Country'] = ''

        # move state name in city column then delete state name in city column
        condition5 = df['Updated City'].isin(malaysia_state)
        df.loc[condition5, 'Updated State'] = df.loc[condition5, 'Updated City']
        df.loc[condition5, 'Updated City'] = ''

        # move country name in city column
        condition6 = df['Updated City'].isin(country_list)
        df.loc[condition6, 'Updated Country'] = df.loc[condition6, 'Updated City']
        df.loc[condition6, 'Updated City'] = ''

        # if data in state column is in list. populate malaysia in country. 
        condition7 = df['Updated State'].isin(malaysia_state)
        df.loc[condition7, 'Updated Country'] = 'Malaysia'
        
        # move non state data in state data to new column
        df['Updated City 2'] = df['Updated State']
        condition8 = ~ df['Updated State'].isin(malaysia_state)
        df.loc[condition7, 'Updated City 2'] = ''
        df.loc[condition8, 'Updated State'] = ''

        # delete others in updated city 2
        condition9 = df['Updated City 2'] == 'others'
        df.loc[condition9, 'Updated City 2'] = ''

        # populate updated city with data from updated city 2 if blank
        condition10 = df['Updated City'] == ''
        df.loc[condition10, 'Updated City'] = df.loc[condition10, 'Updated City 2']
        df.loc[condition10, 'Updated City 2'] = ''

        # get state from Mailing street
        pattern = '|'.join(map(re.escape, malaysia_state))
        df['Mailing Street Test'] = df['Mailing Street'].str.lower()
        condition11 = df['Updated State'] == ''
        df.loc[condition11, 'Updated State'] = df.loc[condition11, 'Mailing Street Test'].str.extract(f'({pattern})', expand=False) 
        df.drop(columns=['Mailing Street Test'], inplace=True)

        # if state blank, run code to find the zipcode in the dictionary. 
        def update_state(df, state_zipcode):
            
            # Ensure the columns exist in the DataFrame
            if 'Updated State' in df.columns and 'Updated Zip' in df.columns:
                # Ensure the blank entries are empty strings
                df['Updated State'] = df['Updated State'].fillna('')
                # Update the blank 'Updated State' entries based on the 'Updated Zip' and the dictionary
                df['Updated State'] = np.where(df['Updated State'] == '', df['Updated Zip'].map(lambda x: next((k for k, v in zipcode.items() if x in v), '')), df['Updated State'])
            else:
                raise KeyError("The DataFrame must contain 'Updated State' and 'Updated Zip' columns")
    
            #df['Updated State'] = np.where(df['Updated State'] == '', df['Updated Zip'].map(lambda x: next((k for k, v in state_zipcode.items() if x in v), '')), df['Updated State'])
        
            return df

        # Apply the function to update blank 'State' entries
        df = update_state(df, zipcode)
        
        return df
    
    all_address_df = populate_data_from_other_column(all_address_df)
    startwith_zero_df = populate_data_from_other_column(startwith_zero_df)
    
    # capitalize spelling
    all_address_df[columns_to_clean] = all_address_df[columns_to_clean].apply(lambda x : x.str.title())
    startwith_zero_df[columns_to_clean] = startwith_zero_df[columns_to_clean].apply(lambda x : x.str.title())

    def merge_city_column(row):
        # concat data from updated city 2 and updated city if there is data. 

        if row['Updated City 2'] != '':
            return row['Updated City'] + ", " + row['Updated City 2']
        else:
            return row['Updated City']

    all_address_df['Updated City'] = all_address_df.apply(merge_city_column, axis=1)
    startwith_zero_df['Updated City'] = startwith_zero_df.apply(merge_city_column, axis=1)


    all_address_df2 = all_address_df.drop(['Mailing City', 'Mailing State/Province', 'Mailing Zip/Postal Code', 'Mailing Country'], axis=1)
    startwith_zero_df2 = startwith_zero_df.drop(['Mailing City', 'Mailing State/Province', 'Mailing Zip/Postal Code', 'Mailing Country'], axis=1)
    
    logger.debug('Saving cleaned data to file')
    all_address_df.to_csv(os.path.join(folder_path, 'To clean - all address - result.csv'), index=False)
    startwith_zero_df.to_excel(os.path.join(folder_path, 'To clean - postal code starts with 0 - result.xlsx'), index=False)
    all_address_df2.to_csv(os.path.join(folder_path, 'To clean - all address - finished.csv'), index=False)
    startwith_zero_df2.to_excel(os.path.join(folder_path, 'To clean - postal code starts with 0 - finished.xlsx'), index=False)

    logger.info('Process completed.')


if __name__ == '__main__':
    main()