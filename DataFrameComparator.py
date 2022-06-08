import pandas as pd
import numpy as np
from io import open


class DataFrameComparator:
    __file = '# '
    df_ref = None
    df_proof = None
    name_col_id = None

    def __init__(self, df_ref, df_proof, name_col_id, table_name='Report'):
        # Set all column names to lowercase and keep the dataframes
        df_ref.columns = map(str.lower, df_ref.columns)
        df_proof.columns = map(str.lower, df_proof.columns)
        self.df_ref = df_ref
        self.df_proof = df_proof

        self.name_col_id = name_col_id
        self.__file += f'{table_name}\n'
        self.table_name = table_name

    def check_cols(self):
        description_cols = '## Description of columns\n \n'
        # check the number of columns
        if self.df_ref.shape[1] == self.df_proof.shape[1]:
            description_cols += 'The dataframes have the same number of columns.\n \n'
        else:
            description_cols += 'The dataframes have different number of columns.\n \n'

        description_cols += f'- Columns number of Reference DataFrame: {self.df_ref.shape[1]} ' \
                            f'\n- Columns number of Proof DataFrame: {self.df_proof.shape[1]}\n \n \n'

        # Get common columns
        common_cols = list(set(self.df_ref).intersection(set(self.df_proof)))
        description_cols += f'\t- Columns in common: {list(sorted(common_cols))}\n'
        # Get columns differences
        df_ref_unique_cols = set(self.df_ref) - set(self.df_proof)
        df_proof_unique_cols = set(self.df_proof) - set(self.df_ref)

        description_cols += f'\t- Columns only in Reference DataFrame: {list(sorted(df_ref_unique_cols))}\n'
        description_cols += f'\t- Columns only in Proof DataFrame: {list(sorted(df_proof_unique_cols))}\n'

        # Only consider common columns in the following proofs
        self.df_ref = self.df_ref[common_cols]
        self.df_proof = self.df_proof[common_cols]

        print(description_cols)
        self.__file += description_cols

    def check_rows(self, show_unique_ids=False):
        # check the number of rows
        description_rows = '## Description of rows\n'
        if self.df_ref.shape[0] == self.df_proof.shape[0]:
            description_rows += 'The dataframes have the same number of rows.\n\n'
        else:
            description_rows += 'The dataframes have different number of rows.\n\n'

        description_rows += f'- Rows number of Reference DataFrame: {self.df_ref.shape[0]} ' \
                            f'\n- Rows number of Proof DataFrame: {self.df_proof.shape[0]}\n \n \n'

        # evaluate the and select the shared values of id
        if self.name_col_id:
            # Get common ids
            common_ids = set(self.df_ref[self.name_col_id]) & set(self.df_proof[self.name_col_id])
            description_rows += f'\t- IDs in common: {len(common_ids)}\n'

            # Get rows differences
            unique_ids_df_ref = set(self.df_ref[self.name_col_id]) - set(self.df_proof[self.name_col_id])
            unique_ids_df_proof = set(self.df_proof[self.name_col_id]) - set(self.df_ref[self.name_col_id])

            description_rows += f'\t- Number of IDs only in Reference DataFrame: {len(unique_ids_df_ref)}\n'
            description_rows += f'\t- Number of IDs only in Proof DataFrame: {len(unique_ids_df_proof)}\n'

            # export unique ids
            if show_unique_ids:
                description_rows += f'### IDs only in Reference DataFrame: \n```{unique_ids_df_ref}```\n'
                description_rows += f'### IDs only in Proof DataFrame: \n ```{unique_ids_df_proof}```\n'

            # Only consider common ids
            self.df_ref = self.df_ref.loc[self.df_ref[self.name_col_id].isin(common_ids)]
            self.df_ref.sort_values(self.name_col_id, inplace=True, ignore_index=True)

            self.df_proof = self.df_proof.loc[self.df_proof[self.name_col_id].isin(common_ids)]
            self.df_proof.sort_values(self.name_col_id, inplace=True, ignore_index=True)

        # TODO: add the option where there are not a explicit column id

        print(description_rows)
        self.__file += description_rows

    def check_datatypes(self):
        # TODO: Evaluate the condition of having the same column names and the same dimensions
        description_datatypes = '## Description of datatypes\n'
        # get the column names with differences in the datatypes
        cols_with_different_datatypes = (self.df_ref.dtypes == self.df_proof.dtypes)[
            (self.df_ref.dtypes == self.df_proof.dtypes) == False].index.tolist()

        description_datatypes += f'\t- Number of columns with differences in ' \
                                 f'the datatypes: {len(cols_with_different_datatypes)}\n'

        if len(cols_with_different_datatypes) != 0:
            description_datatypes += f'Columns with differences in the datatypes: {cols_with_different_datatypes}\n'

        print(description_datatypes)
        self.__file += description_datatypes

    def check_differences_in_colum_dates(self):
        description_diff_colum_dates = '## Description of differences in column dates\n'
        # Find datetime columns
        date_differences = dict()
        object_cols = (self.df_ref[self.df_ref.columns].dtypes == 'object') & \
                      (self.df_proof[self.df_proof.columns].dtypes == 'object')
        object_cols = object_cols[object_cols].index.tolist()

        # evaluate differences in the column dates and convert to the correct format each column
        for col in set(self.df_ref.columns) & set(object_cols):
            if col == self.name_col_id:
                continue
            try:
                df_ref_date_col = pd.to_datetime(self.df_ref[col], format='%Y-%m-%d')
                df_proof_date_col = pd.to_datetime(self.df_proof[col], format='%Y-%m-%d')
            except Exception as ex:
                pass
            else:
                # check differences in the columns with dates
                date_differences[col] = (self.df_proof[col].fillna(np.Inf) != self.df_ref[col].fillna(np.Inf)).sum()
                # Save data as datetime
                self.df_ref[col] = df_ref_date_col
                self.df_proof[col] = df_proof_date_col

        description_diff_colum_dates += f'Differences in column dates:' \
                                        f'\n{pd.DataFrame.from_dict(date_differences, orient="index").to_html()}\n'

        print(description_diff_colum_dates)
        self.__file += description_diff_colum_dates

    def check_differences_in_columns(self, export_differences=False):
        description_diff_columns = '\n## Description of differences in all columns\n'
        # Contrast all elements
        # Fill with unambigous value while contrasting to ignore missing values since NA != NA
        differences = self.df_proof.fillna(np.Inf) != self.df_ref.fillna(np.Inf)

        # Identify columns and rows with differences
        cols_w_diffs = differences.any(axis=0)
        cols_w_diffs = cols_w_diffs[cols_w_diffs].index.tolist()
        rows_w_diffs = differences.any(axis=1)

        cols_diffs_n = differences.sum()[cols_w_diffs].to_dict()

        # Report differences
        if differences.sum().sum():
            description_diff_columns += '\tColumns with differences:\n'
            for col, n in cols_diffs_n.items():
                if (n / np.max([self.df_ref[col].count(), self.df_proof[col].count()])) > 0.2:
                    description_diff_columns += f'\t- {col}: {n} *\n'
                else:
                    description_diff_columns += f'\t- {col}: {n}\n'

            # TODO: Evaluate the existence of self.name_col_id
            if export_differences:
                # Identify specific differences
                df_proof_diffs = self.df_proof.loc[rows_w_diffs, [self.name_col_id] + cols_w_diffs]
                df_ref_diffs = self.df_ref.loc[rows_w_diffs, [self.name_col_id] + cols_w_diffs]

                df_proof_diffs.set_index(self.name_col_id, inplace=True)
                df_ref_diffs.set_index(self.name_col_id, inplace=True)

                # Remove similarities to only export differences
                for col in cols_w_diffs:
                    similarities = df_proof_diffs[col] == df_ref_diffs[col]
                    df_ref_diffs.loc[similarities, col] = np.nan
                    df_proof_diffs.loc[similarities, col] = np.nan

                # Summarise differences in one dataframe
                df_diffs = df_ref_diffs.join(df_proof_diffs, self.name_col_id, lsuffix='_ref', rsuffix='_proof')
                df_diffs = df_diffs.reindex(sorted(df_diffs.columns), axis=1)

                print('\tExporting differences to csv')

                df_diffs.to_csv(f'differences_{self.table_name}.csv')

        else:
            description_diff_columns += '\tNo differences found on common ids and columns'

        print(description_diff_columns)
        self.__file += description_diff_columns

    def output_information(self):
        file = open('description.md', 'w')
        file.write(self.__file)
        file.close()
