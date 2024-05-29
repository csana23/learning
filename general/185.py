import pandas as pd
import numpy as np

employee_data = {
    'id': [1, 2, 3, 4, 5, 6, 7],
    'name': ['Joe', 'Henry', 'Sam', 'Max', 'Janet', 'Randy', 'Will'],
    'salary': [85000, 80000, 60000, 90000, 69000, 85000, 70000],
    'departmentId': [1, 2, 2, 1, 1, 1, 1]
}

department_data = {
    'id': [1, 2],
    'name': ['IT', 'Sales']
}

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    # get top 3 unique salaries by department
    salaries = employee.groupby('departmentId')['salary'].unique().apply(lambda x: np.sort(x)[-3:])

    df = pd.merge(left=employee, right=salaries, how="inner", on="departmentId")

    df["is_top_3"] = df.apply(lambda row: "yes" if row["salary_x"] in row["salary_y"] else "no", axis=1)

    result = pd.merge(left=df, right=department, how="inner", left_on="departmentId", right_on="id")

    result = result.loc[result.is_top_3 == "yes"]

    drop_cols = ["id_x", "departmentId", "salary_y", "is_top_3", "id_y"]
    result = result.drop(drop_cols, axis=1)

    result = result.rename(columns={"name_x": "Employee", "name_y": "Department", "salary_x": "Salary"})

    return result
    

employee_df = pd.DataFrame(employee_data)

department_df = pd.DataFrame(department_data)

print(top_three_salaries(employee_df, department_df))