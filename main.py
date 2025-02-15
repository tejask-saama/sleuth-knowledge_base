import os
from datetime import datetime
from dotenv import load_dotenv

from helpers import (
    convert_tables_to_dataframe,
    filter_profile_report,
    chunk_dictionary,
    create_summery,
    create_table_info,
    create_relationship_report,
    read_txt_file,
    write_to_file
)

load_dotenv()

db_config = {
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': os.getenv("DB_DATABASE", "")
}


def process_batches(profile_batches, whole_batches):
    summarized_reports, knowledge_base_outputs = [], []
    
    for i, (profile_batch, whole_batch) in enumerate(zip(profile_batches, whole_batches)):
        summarized_report = create_summery(profile_batch)
        summarized_reports.append(summarized_report)
        print(f"Batch {i+1}: Summarized Report Generated.")

        prompt2_output = create_table_info(summarized_report, whole_batch)
        knowledge_base_outputs.append(prompt2_output)
        print(f"Batch {i+1}: Combined Data Processed.")
    
    return "\n\n".join(summarized_reports), "\n\n".join(knowledge_base_outputs)

def main():
    start_time = datetime.now()
    print(db_config)
    
    if not db_config['database']:
        print("Database not specified. Exiting.")
        return
    
    database_name = db_config['database']
    dataframes = convert_tables_to_dataframe(db_config)
    filtered_report = filter_profile_report(dataframes, database_name)
    whole_data = {key: df.head(50) for key, df in dataframes.items()}

    profile_batches = list(chunk_dictionary(filtered_report, chunk_size=5))
    whole_batches = list(chunk_dictionary(whole_data, chunk_size=5))

    summarized_report, knowledge_base = process_batches(profile_batches, whole_batches)
    
    write_to_file(f"{database_name}_summarized_report.txt", summarized_report)
    write_to_file(f"{database_name}_table_info.txt", knowledge_base)
    
    complete_table_info = read_txt_file(f"{database_name}_table_info.txt")
    complete_summarized_report = read_txt_file(f"{database_name}_summarized_report.txt")
    relationship_report = create_relationship_report(whole_data, complete_table_info, complete_summarized_report)
    
    write_to_file(f"{database_name}_relationship_report.txt", relationship_report)
    
    print("Total time taken for all processes:", datetime.now() - start_time)

if __name__ == "__main__":
    main()
