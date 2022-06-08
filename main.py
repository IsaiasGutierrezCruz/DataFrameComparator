from DataFrameComparator import DataFrameComparator
import pandas as pd
import numpy as np


def dataframes_creation():
    # first data frame
    first_df = pd.DataFrame(
        {
            "id": [1, 2, 3, 5, 7],
            "Stationary": ["Pens", "Scales",
                           "Pencils", "Geometry Box",
                           "Crayon Set"],
            "Price": [100, 50, 25, 100, 65],
            "Quantity": [10, 5, 5, 2, 1],
            "Dates": ['2012-01-19 03:14:07', '2011-01-12 02:00:07',
                      '2008-09-12 06:30:12', '2009-08-23 08:17:17',
                      '2018-01-20 07:17:19'],
            "ColExtra": [1, 2, 3, 4, 7]
        },
        columns=["id", "Stationary", "Price", "Quantity", "Dates", "ColExtra"],
    )

    # second data frame
    second_df = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 7],
            "Stationary": ["Pens", "Scales",
                           "Pencils", "Geometry Box",
                           "Crayon Set"],
            "Price": [100, 50, 5, 100, 65],
            "Quantity": [10, 5, 5, 3, 1],
            "Dates": ['2012-01-19 03:14:07', '2011-01-12 02:00:07',
                      '2008-10-12 06:30:12', '2009-08-23 08:17:17',
                      '2018-01-20 07:17:19']
        },
        columns=["id", "Stationary", "Price", "Quantity", "Dates"],
    )
    return [first_df, second_df]


if __name__ == '__main__':
    df1, df2 = dataframes_creation()
    comparator = DataFrameComparator(df1, df2, name_col_id='id')
    comparator.check_cols()
    comparator.check_rows(show_unique_ids=True)
    comparator.check_datatypes()
    comparator.output_information()
    """
    print(df1)
    print(comparator.df_ref)
    print(comparator.df_ref.dtypes.index)
    print('--------------')
    print(df2)
    print(comparator.df_proof)
    """
