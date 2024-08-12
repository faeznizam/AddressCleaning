from module.state_zipcode import state_zipcode

zipcode_dict = state_zipcode

def get_state(state_value,zipcode_dict):
    print(f'looking up state for zip code: {state_value}')
    for state, zipcode in zipcode_dict.items():
        if state_value in zipcode:
            print(f'fount state : {state} for zip code: {state_value}')
            return state
    print(f'no state found for zip code : {state_value}')    
    return None

def get_state_from_zipcode_column(df):
    
    df['Mailing Zip/Postal Code'] = df['Mailing Zip/Postal Code'].astype(str).str.strip()
    df['Mailing State/Province'] = df['Mailing Zip/Postal Code'].apply(lambda x: get_state(x, state_zipcode))

    return df