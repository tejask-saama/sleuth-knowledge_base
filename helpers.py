import os
import mysql.connector
import pandas as pd
import json
import prompts
from llm_models import llm
from ydata_profiling import ProfileReport
from dotenv import load_dotenv
import sqlite3

load_dotenv()

def write_to_file(filename, content):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"Output written to {filename}")

# def get_table_names(conn):
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SHOW TABLES")
#         return [table[0] for table in cursor.fetchall()]
#     except mysql.connector.Error as e:
#         print(f"An error occurred: {e}")
#         return []

# def convert_tables_to_dataframe(db_config):
#     try:
#         with mysql.connector.connect(**db_config) as conn:
#             table_names = get_table_names(conn)
#             return {
#                 table: pd.read_sql_query(f"SELECT * FROM {table}", conn)
#                 for table in table_names
#             }
#     except mysql.connector.Error as e:
#         print(f"An error occurred: {e}")
#         return {}



def convert_tables_to_dataframe(db_path):
    conn = None  # Initialize conn to None outside the try block
    try:
        conn = sqlite3.connect(db_path)
        table_names = get_table_names(conn)
        dataframes = {}

        for table_name in table_names:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql_query(query, conn)
                dataframes[table_name] = df
                print(f"Successfully converted '{table_name}' to DataFrame.")
            except Exception as e:
                print(f"Error converting '{table_name}': {e}")

        return dataframes

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

    finally:
        if conn:
            conn.close()

def get_table_names(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return table_names

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None

# Example usage



def generate_profiling_reports(dataframes, database_name):
    profile_reports = {
        table: json.loads(ProfileReport(df, title=f"Profiling Report {table}").to_json())["variables"]
        for table, df in dataframes.items()
    }
    write_to_file(f"profile_reports_{database_name}.json", json.dumps(profile_reports, indent=4))
    return profile_reports

def read_json_as_object(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading JSON: {e}")
        return None

def filter_profile_report(dataframes, database_name):
    profile_report = read_json_as_object(f"profile_reports_{database_name}.json") or generate_profiling_reports(dataframes, database_name)
    important_vars = { 'n_distinct', 'p_distinct', 'is_unique', 'type', 'count', 'chi_squared', 'mean', 'std', 'min', 'max', 'kurtosis', 'skewness', 'range', '25%', '50%', '75%', 'iqr', 'cv', 'histogram' }
    return {
        table: {col: {k: v for k, v in stats.items() if k in important_vars} for col, stats in columns.items()}
        for table, columns in profile_report.items()
    }

def chunk_dictionary(data_dict, chunk_size=5):
    items = list(data_dict.items())
    for i in range(0, len(items), chunk_size):
        # Create a sub-dictionary for the current batch
        yield dict(items[i:i+chunk_size])

def create_summary(batch_dict):
    prompt = prompts.summerization_report_prompt.format(filtered_report_batch=str(list(batch_dict.items())))
    return llm.invoke(prompt).content

def create_table_info(summarized_report, whole_batch):
    prompt = prompts.Table_info_prompt.format(summerized_report=summarized_report, whole_data=str(list(whole_batch.items())))
    return llm.invoke(prompt).content

def create_relationship_report(whole_data, complete_table_info, complete_summarized_report):
    prompt = prompts.relationship_prompt.format(whole_data=whole_data, table_info=complete_table_info, summerized_report_info=complete_summarized_report)
    return llm.invoke(prompt).content

def read_txt_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def sleauth(question):
    database_name = 'insurance_db'
    table_info = read_txt_file(f"{database_name}_table_info.txt")
    relationship_info = read_txt_file(f"{database_name}_relationship_report.txt")
    prompt = prompts.QA_PROMPT.format(table_info=table_info, relation_ship_info=relationship_info)
    return llm.invoke([{"role": "system", "content": prompt}, {"role": "user", "content": question}]).content
