import psycopg2
import os
from dotenv import load_dotenv
from reader import Reader



load_dotenv()


class Manager:
    def __init__(self) -> None:
        self.host = os.getenv('HOST')
        self.db_name = os.getenv('DB_NAME')
        self.port = os.getenv('PORT')
        self.login = os.getenv('LOGIN')
        self.password = os.getenv('PASSWORD')
        self.conn = None
        self.cursor=None




    def get_conn(self)->None:
        try:
            self.conn = psycopg2.connect(database=self.db_name,
                                    host=self.host,
                                    user=self.login,
                                    password=self.password,
                                    port=self.port)


            print("Connection successful")
            self.cursor = self.conn.cursor()

            self.cursor.execute("SELECT * FROM _user")
            rows = self.cursor.fetchall() 

            
            for row in rows:
                print(row)

        except Exception as error:
            print(f"Error: {error}")

            
    def insert_into(self, query):
        try:
            self.cursor.execute(query)
        except Exception as error:
            print(f"Error: {error}")

        self.close_conn


    def close_conn(self)->None:
        if self.conn:
            self.cursor.close()
            self.conn.close()



mng = Manager()
#mng.get_conn()
#mng.close_conn()


#csv_file = "./pron_gya_csv.csv"

csv_file = "E:\\Projekty\\for_work\\ai-solution\\ITSquad-antyfraud\\excel\\final.csv"


user_columns = ['user_id', 'username', 'firstname', 'lastname', 'email', 'password', 'user_role_id']
incident_columns = ['incident_id', 'incident_number', 'incydent_type', 'occurance_date', 'submission_date', 'incydent_status_id', 'user_id', 'last_modified']
incident_history_columns = ['id', 'action', 'object_id', 'incident_id']
party_columns = ['party_id', 'first_name_party', 'middle_name_party', 'surname_party', 'tax_id','adress_party', 'phone_number_party', 'email_party']
party_attribute_columns = ['id_attribute', 'value', 'party_id_attribute', 'party_extension_id']
party_extension_columns =['id_extension', 'name']
party_extension_mapping_columns = ['party_extension_id', 'active_flag']
user_role_columns = ['user_role_id', 'user_role']
incident_status_columns = ['incydent_status_id', 'status_description']

asset_name_columns = ['name_asset']
asset_attribute_columns = ['asset_id_attribute', 'system_asset_extension_id', 'asset_attribute_value']
system_asset_extension_columns = ['system_asset_extension_name']


reader = Reader(csv_file)
#reader.read_file_and_save("./txt_data_to_db/user_role.txt", user_role_columns)
#reader.read_file_and_save("./txt_data_to_db/user_.txt", user_columns)
#reader.read_file_and_save("./txt_data_to_db/incident.txt", incident_columns)
reader.read_file_and_save("./txt_data_to_db/incident_status.txt", incident_status_columns)
#reader.read_file_and_save("./txt_data_to_db/party.txt", party_columns)
#reader.read_file_and_save("./txt_data_to_db/party_attribute.txt", party_attribute_columns)
#reader.read_file_and_save("./txt_data_to_db/party_extension.txt", party_extension_columns)
#reader.read_file_and_save("./txt_data_to_db/party_extension_mapping.txt", party_extension_mapping_columns)

'''
reader.read_file_and_save("./user_.txt", user_columns)
reader.read_file_and_save("./incident.txt", incident_columns)
reader.read_file_and_save("./incident_history.txt", incident_history_columns)
reader.read_file_and_save("./party.txt", party_columns)
reader.read_file_and_save("./party_attribute.txt", party_attribute_columns)
reader.read_file_and_save("./party_extension.txt", party_extension_columns)
reader.read_file_and_save("./party_extension_mapping.txt", party_extension_mapping_columns)
'''
'''
reader.read_file_and_save("./asset.txt", asset_name_columns)
reader.read_file_and_save("./asset_attribute.txt", asset_attribute_columns)
reader.read_file_and_save("./system_asset_extension.txt", system_asset_extension_columns)
'''
query_file = "./query_file.txt"

#user_role_query = reader.create_batch_insert_statement("./txt_data_to_db/user_role.txt", 'user_role', user_role_columns)
#user_query = reader.create_batch_insert_statement("./txt_data_to_db/user_.txt", 'user_', user_columns)
#incident_query = reader.create_batch_insert_statement("./txt_data_to_db/incident.txt", 'incident', incident_columns)
incident_query = reader.create_batch_insert_statement("./txt_data_to_db/incident_status.txt", 'incident', incident_status_columns)
#incident_history_query = reader.create_batch_insert_statement("./incident_history.txt", 'incident_history', incident_history_columns)
#party_query = reader.create_batch_insert_statement("./txt_data_to_db/party.txt", 'party', party_columns)
#party_attribute_query = reader.create_batch_insert_statement("./txt_data_to_db/party_attribute.txt", 'party_attribute', party_attribute_columns)
#party_extension_query = reader.create_batch_insert_statement("./txt_data_to_db/party_extension.txt", 'party_extension', party_extension_columns)
#party_extension_mapping_query = reader.create_batch_insert_statement("./txt_data_to_db/party_extension_mapping.txt", 'party_extension_mapping', party_extension_mapping_columns)



#print(party_query)

#print(user_query)
#print(incident_query)
# print(incident_history_query)
#print(party_query)
#print(party_attribute_query)
#print(party_extension_mapping_query)
#print(party_extension_mapping_query)


#asset_query = reader.create_batch_insert_statement("./asset.txt", "asset", asset_name_columns)
#asset_attribute_query =reader.create_batch_insert_statement("./asset_attribute.txt", "asset_attribute", asset_attribute_columns)
#system_asset_extension_query =reader.create_batch_insert_statement("./system_asset_extension.txt", "system_asset_extension", system_asset_extension_columns)

'''
with open(query_file, 'w') as f:
    f.write(user_query + "\n")
    f.write(incident_query+ "\n")
    f.write(incident_history_query+ "\n")
    f.write(party_query+ "\n")
    f.write(party_attribute_query+ "\n")
    f.write(party_extension_mapping_query+ "\n")
    f.write(party_extension_mapping_query+ "\n")
    f.write(asset_query+ "\n")
    f.write(asset_attribute_query+ "\n")
    f.write(system_asset_extension_query+ "\n")
    '''