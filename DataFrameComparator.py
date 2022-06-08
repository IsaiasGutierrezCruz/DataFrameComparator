import pandas as pd


class DataFrameComparator:
    __verbose = None  # make a description of the differences between both dataframes
    __num_rows_df_ref = None
    __num_cols_df_ref = None
    __col_types_df_ref = None
    __df_ref = None
    # data from

    def __init__(self, df_ref, df_proof):
        # get the number of rows
        self.__num_rows_df_ref = df_ref.shape[0]
        self.num_cols_df_ref = df_ref.shape[1]
        # self.__col_types_df1 = df_reference.

    def check_row_number(self, df_to_compare):
        if self.__num_rows_df_ref == df_to_compare.shape[0]:
            print('Both dataframes have the same number of rows. \n')
        else:
            print('Both dataframes have different number of rows')

    def check_col_number(self, df_to_compare):
        if self.__num_cols_df_ref == df_to_compare.shape[1]:
            print('Both dataframes have the same number of columns. \n')
