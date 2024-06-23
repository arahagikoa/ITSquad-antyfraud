import os
import pandas as pd


class Reader:
    def __init__(self, filename) -> None:
        self.filename = filename

    def read_file_and_save(self, out_path, expected_columns) -> str:
        try:
            df = pd.read_csv(self.filename, delimiter=';')
            print("File loaded successfully.")
        except FileNotFoundError:
            print(f"File not found: {self.filename}")
            return
        except pd.errors.EmptyDataError:
            print("No data found in the file.")
            return
        except pd.errors.ParserError:
            print("Error parsing the file.")
            return

        
        #print("DataFrame loaded:")
        #print(df.head())

        
        #print("Column names:")
        #print(df.columns.tolist())

        
        


        #missing_columns = [col for col in expected_columns if col not in df.columns]
        #if missing_columns:
        #    print(f"Missing columns: {missing_columns}")
        #    return
        


        columns_data = df[expected_columns]
        try:
            with open(out_path, 'w') as file:
                
                for index, row in columns_data.iterrows():
                    
                    values = ', '.join(map(lambda x: f"'{x}'" if isinstance(x, str) else str(x), row.values))
                    file.write(f"({values}),\n")
            print(f"Data successfully saved to {out_path}")
        except IOError:
            print(f"Error saving data to {out_path}")
        
        
        #print(columns_data)

    def create_batch_insert_statement(self, file_path, table_name, columns):
        values_list = []

        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    cleaned_line = line.strip().rstrip(',')
                    if cleaned_line:
                        values_list.append(cleaned_line)

            values_str = ', '.join(values_list)
            sql_statement = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {values_str};"
            return sql_statement
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return ""
        except IOError:
            print(f"Error reading file: {file_path}")
            return ""
        

