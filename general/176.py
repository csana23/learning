import pandas as pd
import numpy as np

employee_data_1 = {
    'id': [1, 2, 3, 4, 5],
    'salary': [100, 200, 300, 200, 100]
}

employee_data_2 = {
    "id": [1],
    "salary": [100]
}

employee_df = pd.DataFrame(employee_data_1)

def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    distinct_salaries = employee.salary.drop_duplicates().reset_index(drop=True).sort_values(ascending=True, inplace=True)

    if len(distinct_salaries) < 2:
        return pd.DataFrame(data={"SecondHighestSalary": np.nan}, index=[1])
    else:
        second_highest_salary = distinct_salaries.iloc[1]
        return pd.DataFrame(data={"SecondHighestSalary": second_highest_salary}, index=[1])

print(
    second_highest_salary(employee_df)
)

