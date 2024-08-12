"""
1. Use street, city, state, country to determine the country = malaysia
2. Based on mailing street, pull out zipcode.
3. Based on mailing street, pull out state. 
4. Validate zipcode.
5. Populate State.

"""
# import form local module
from city_list import malaysia_city_list
from county_list import country
from state_list import state
from zipcode_list import zipcode

# import from library
import pandas as pd
import warnings
import logging
import os
import re

# Configure the logging
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Set the format for log messages
    handlers=[
        logging.FileHandler("app.log"),  # Log messages to a file
        logging.StreamHandler()  # Log messages to the console
    ])

# Example usage
logger = logging.getLogger(__name__)

def main():

    # Ignore warnings for stylesheets
    warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl.styles.stylesheet')


    logging.info('Get folder path')
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\AddressCleaning\test_data'


    for file in os.listdir(folder_path):
        if 'Address W Street' in file:
            file_path = os.path.join(folder_path, file)

            logging.info('Read file')
            df = pd.read_excel(file_path)

            logging.info('Drop column')
            df = df.drop(columns='Rollup Summary: First Campaign: Campaign Name')

            # condition to blank cell
            delete1 = df['Mailing Street'] == '- - -'
            df.loc[delete1, 'Mailing Street'] = ''

            delete2 = df['Mailing Street'] == '. . .'
            df.loc[delete2, 'Mailing Street'] = ''

            delete3 = df['Mailing Street'] == ', , ,'
            df.loc[delete3, 'Mailing Street'] = ''

            delete4 = df['Mailing Street'] == '. .'
            df.loc[delete4, 'Mailing Street'] = ''

            delete5 = df['Mailing Street'] == '.'
            df.loc[delete5, 'Mailing Street'] = ''

            logging.info('Create new column')
            df['New State'] = ''
            df['New Post Code'] = ''
            df['New Country'] = ''

            # delete based on pattern
            columns_to_clean = ['Mailing City','Mailing State/Province','Mailing Zip/Postal Code','Mailing Country']
            pattern = '[.,;?]'

            df[columns_to_clean] = df[columns_to_clean].apply(lambda x: x.replace(pattern, '', regex=True))

            logging.info('Clean Mailing Street')
            df['Mailing Street'] = df['Mailing Street'].str.replace(',,', ', ')
            df['Mailing Street'] = df['Mailing Street'].str.replace(',,,', ', ')

            logging.info('Rearrange Column')
            rearrange_column = ['Supporter ID', 'Mailing Street', 'Mailing City', 'Mailing State/Province', 
                                'New State', 'Mailing Zip/Postal Code', 'New Post Code', 'Mailing Country', 'New Country']
            
            df = df[rearrange_column]


            logging.info('Extract value from mailing street.')
            country_list = country()
            state_list = state()
            city_list = malaysia_city_list()
            zipcode_list = zipcode()

            city_list = list(map(str.lower, city_list))
            country_list = list(map(str.lower, country_list))

            

            df['Mailing Street'] = df['Mailing Street'].str.lower()
            df['Mailing State/Province'] = df['Mailing State/Province'].str.lower()

            def extract_state(address, current_value):
                for state in state_list:
                    if state in address:
                        return state
                return current_value  # Return the current value if no state is found in the address

            # Apply the function to each row
            df['New State'] = df.apply(lambda row: extract_state(row['Mailing Street'], row['New State']), axis=1)

            def extract_country(address, current_value):
                for country in country_list:
                    if country in address:
                        return country
                return current_value
                
            
            df['New Country'] = df.apply(lambda row: extract_country(row['Mailing Street'], row['New Country']), axis=1)

            postcode_pattern = r'\b\d{5}\b'

            def extract_valid_postcode(address):
                postcodes = re.findall(postcode_pattern, address)
                for postcode in postcodes:
                    if postcode in zipcode_list:
                        return postcode
                return None
            
            df['New Post Code'] = df['Mailing Street'].apply(extract_valid_postcode)

            def postcode_validation(x):
                if x in zipcode_list:
                    return 'Valid'
                else:
                    return 'Invalid'
                
            df['Postcode Validation'] = df['New Post Code'].apply(lambda x : postcode_validation(x))










            logging.info('Capitalize first alphabet')
            columns_to_capitalize = ['New State','New Post Code','New Country','Mailing Street']
            df[columns_to_capitalize] = df[columns_to_capitalize].apply(lambda x : x.str.title())
        
            # save file
            df.to_excel(os.path.join(folder_path, 'Address W - Test.xlsx'), index=False)

            logging.info('Process Complete')


            
            

    

if __name__ == '__main__':
    main()


