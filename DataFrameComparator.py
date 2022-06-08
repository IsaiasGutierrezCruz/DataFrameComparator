import pandas as pd
from io import open


class DataFrameComparator:
    __file = '# '
    df_ref = None
    df_proof = None
    name_col_id = None

    def __init__(self, df_ref, df_proof, name_col_id=None, table_name='Report'):
        # Set all column names to lowercase and keep the dataframes
        df_ref.columns = map(str.lower, df_ref.columns)
        df_proof.columns = map(str.lower, df_proof.columns)
        self.df_ref = df_ref
        self.df_proof = df_proof

        self.name_col_id = name_col_id
        self.__file += f'{table_name}\n'

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

    def output_information(self):
        file = open('description.md', 'w')
        file.write(self.__file)
        file.close()
