import pandas as pd
import numpy as np

data_1 = {
    'id': [1, 2, 3],
    'salary': [100, 200, 300]
}

data_2 = {
    'id': [1],
    'salary': [100]
}

def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    distinct_salaries = employee.salary.drop_duplicates().reset_index(drop=True)
    distinct_salaries = distinct_salaries.sort_values(ascending=False)
    column_name = f"getNthHighestSalary({N})"

    if len(distinct_salaries) < N or N <= 0:
        return pd.DataFrame(data={column_name: np.nan}, index=[1])
    else:
        nth_highest_salary = distinct_salaries.iloc[N-1]
        return pd.DataFrame(data={column_name: nth_highest_salary}, index=[1])
    
df = pd.DataFrame(data_2)

print(nth_highest_salary(df, 2))