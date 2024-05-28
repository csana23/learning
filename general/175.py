import pandas as pd

person_data = {
    'personId': [1, 2],
    'lastName': ['Wang', 'Alice'],
    'firstName': ['Allen', 'Bob']
}

person_df = pd.DataFrame(person_data)

address_data = {
    'addressId': [1, 2],
    'personId': [2, 3],
    'city': ['New York City', 'Leetcode'],
    'state': ['New York', 'California']
}

address_df = pd.DataFrame(address_data)

output_columns = ["firstName", "lastName", "city", "state"]

def combine_two_tables(person: pd.DataFrame, address: pd.DataFrame) -> pd.DataFrame:
    result_df = pd.merge(left=person, right=address, how="left", left_on='personId', right_on="personId")

    return result_df[output_columns]

print(
    combine_two_tables(person_df, address_df)
)