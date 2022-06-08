from DataFrameComparator import DataFrameComparator
import pandas as pd
import numpy as np


def dataframes_creation():
    # first data frame
    first_df = pd.DataFrame(
        {
            "Stationary": ["Pens", "Scales",
                           "Pencils", "Geometry Box",
                           "Crayon Set"],
            "Price": [100, 50, 25, 100, 65],
            "Quantity": [10, 5, 5, 2, 1]
        },
        columns=["Stationary", "Price", "Quantity"],
    )

    # second data frame
    second_df = first_df.copy()
    # loc specifies the location,
    # here 0th index of Price Column
    second_df.loc[0, 'Price'] = 150
    second_df.loc[1, 'Price'] = 70
    second_df.loc[2, 'Price'] = 30
    second_df.loc[0, 'Quantity'] = 15
    second_df.loc[1, 'Quantity'] = 7
    second_df.loc[2, 'Quantity'] = 6

    return [first_df, second_df]


if __name__ == '__main__':
    df1, df2 = dataframes_creation()
    comparator = DataFrameComparator(df1)
    comparator.
    comparator.check_row_number(df2)
    #print(df1)
    #print(df2)
    #DataFrameReference()