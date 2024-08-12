from module import get_state_from_city, get_country_from_city, get_state_from_zipcode

import os
import pandas as pd

def main():
    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\AddressCleaning\test_data'

    for filename in os.listdir(folder_path):
        if 'Address Without State' in filename:

            print(f'Processing file: {filename}')
            file_path = os.path.join(folder_path, filename)


            # read
            df = pd.read_excel(file_path, dtype={'Mailing Zip/Postal Code' : str})

            print("Before processing:")
            print(df.head())

            # process
            df = get_state_from_city.get_state_from_city_column(df)
            df = get_country_from_city.get_country_from_city_column(df)
            df = get_state_from_zipcode.get_state_from_zipcode_column(df)

            print("After processing:")
            print(df.head())
            
            # save
            df.to_excel(os.path.join(folder_path, 'Address Without State - Edited.xlsx'), index=False)

            print('Done')
    
if __name__ == '__main__':
    main()
