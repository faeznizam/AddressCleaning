from module.state_list import state



def get_state_from_city_column(df):

    df['Mailing City'] = df['Mailing City'].str.lower()

    malaysian_state = state()

    df['Mailing State/Province'] = df['Mailing City'].apply(lambda x: x if x in malaysian_state else '')
    df['Mailing City'] = df['Mailing City'].apply(lambda x: '' if x in malaysian_state else x)

    df['Mailing City'] = df['Mailing City'].str.title()
    df['Mailing State/Province'] = df['Mailing State/Province'].str.title()
    

    return df
    


           


   


