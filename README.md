This code is used to clean address data. These are the overall logic for this process:

1. Remove state name in city and country column and populate in state column. 
2. Remove country name in city and state column and populate in country column.
3. Remove city name in state and country column and populate in city column.
4. Populate state column based on zipcode using a dictionary with state and zipcode data.
5. concatenate existing data in city with city data from other column.
 