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

# import from library
import pandas as pd
import os


def main():
    # get folder path
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\AddressCleaning\test_data'


    for file in os.listdir(folder_path):
        if 'Address W Street' in file:
            file_path = os.path.join(folder_path, file)

            # read file
            df = pd.read_excel(file_path)

            # drop column
            df = df.drop(columns='Rollup Summary: First Campaign: Campaign Name')

            # condition to blank row
            delete1 = df['Mailing Street'] == '- - -'
            df.loc[delete1, 'Mailing Street'] = ''

            delete2 = df['Mailing Street'] == '. . .'
            df.loc[delete2, 'Mailing Street'] = ''

            delete3 = df['Mailing Street'] == ',,,'
            df.loc[delete3, 'Mailing Street'] = ''

            delete4 = df['Mailing Street'] == '. .'
            df.loc[delete4, 'Mailing Street'] = ''

            delete5 = df['Mailing Street'] == '.'
            df.loc[delete5, 'Mailing Street'] = ''

            # delete blank row
            filtered_df = df[df['Mailing Street'] != '']

            # create new column
            filtered_df['New State'] = ''
            filtered_df['New Post Code'] = ''
            filtered_df['New Country'] = ''

            # delete based on pattern
            columns_to_clean = ['Mailing City','Mailing State/Province','Mailing Zip/Postal Code','Mailing Country']
            pattern = '[.,;?]'

            filtered_df[columns_to_clean] = filtered_df[columns_to_clean].apply(lambda x: x.replace(pattern, '', regex=True))

            # rearrange column
            rearrange_column = ['Supporter ID', 'Mailing Street', 'Mailing City', 'Mailing State/Province', 
                                'New State', 'Mailing Zip/Postal Code', 'New Post Code', 'Mailing Country', 'New Country']
            
            filtered_df = filtered_df[rearrange_column]

            country_list = country()
            state_list = state()
            city_list = malaysia_city_list()

            city_list = list(map(str.lower, city_list))
            country_list = list(map(str.lower, country_list))

            

            filtered_df['Mailing Street'] = filtered_df['Mailing Street'].str.lower()
            filtered_df['Mailing State/Province'] = filtered_df['Mailing State/Province'].str.lower()

            def extract_state(address):
                for state in state_list:
                    if state in address:
                        return state
                return None
            
            filtered_df['New State'] = filtered_df['Mailing Street'].apply(extract_state)

            def extract_country(address, current_value):
                if pd.isna(address):
                    return current_value

                for country in country_list:
                    if country in address:
                        return country
                
            
            filtered_df['New Country'] = filtered_df['Mailing Street'].apply(extract_country)
            filtered_df['New Country'] = filtered_df.apply(lambda row : extract_country(row['Mailing State/Province'], row['New Country']), axis=1)


            






            
            # save file
            filtered_df.to_excel(os.path.join(folder_path, 'Address W - Test.xlsx'), index=False)

            print('Process complete')


            
            

    

if __name__ == '__main__':
    main()


