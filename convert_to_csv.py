import pandas as pd
import os



folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\clean_address_project\data'


startwith_zero_filepath = os.path.join(folder_path, 'To clean - postal code starts with 0.xlsx' )


startwith_zero_df = pd.read_excel(startwith_zero_filepath, dtype={
        'Supporter ID' : str, 
        'Mailing Street' : str, 
        'Mailing City' : str, 
        'Mailing Zip/Postal Code' : str, 
        'Mailing State/Province' : str, 
        'Mailing Country' : str, 
        'Rollup Summary: First Campaign: Campaign Name': str
    })




new_file_name = 'To clean - postal code starts with 0.csv'
new_file_path = os.path.join(folder_path, new_file_name)
startwith_zero_df.to_csv(new_file_path, index=False)

print('file has been download')