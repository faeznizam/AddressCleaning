import pandas as pd
import numpy as np
import os




def main():

    folder_path = r'C:\Users\mfmohammad\OneDrive - UNICEF\Documents\Codes\AddressCleaning\test_data'

    file_list = ['To clean - all address - finished - city.csv', 'To clean - all address - finished - country.csv', 'To clean - all address - finished - postcode.csv', 
                 'To clean - all address - finished - state.csv']

    for file in file_list:
        file_path = os.path.join(folder_path, file)

        # read
        df = pd.read_csv(file_path, encoding='latin1')

        # split
        rows_per_file = 100000

        num_files = (len(df) + rows_per_file - 1) // rows_per_file

        for i, chunk in enumerate(np.array_split(df, num_files)):
            chunk.to_csv(os.path.join(folder_path,f'{file[:-4]}_{i+1}.csv'), index=False)

       

if __name__ == '__main__':
    main()