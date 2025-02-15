
summerization_report_prompt = """
Role: You are an expert Data Engineer and Data Analyst with 10+ years of experience in data modeling and complex dataset analysis.
Task: Summarize the profiler report.

Profiler report: {filtered_report_batch}

Output Format:
- The summary must list all tables from the profiler report.
- For each table, list every column along with all key details.

Example Structure:

Table: <table_name>
    column_name1: datatype, n_uniques values, null values,total_values,missing_value,insights
    column_name2: datatype, n_uniques values, null values,  total_values,missing_value,insights
    column_name3: datatype, n_uniques values, null values,  total_values,missing_value,insights
Table: <table_name>
    column_name1: datatype, n_uniques values, null values,  total_values,missing_value,insights
    column_name2: datatype, n_uniques values, null values, total_values,missing_value,insights
...
...
...
Table n: <table_name>
    column_name1: datatype, n_uniques values, null values,  total_values,missing_value,insights
    column_name2: datatype, n_uniques values, null values, total_values,missing_value,insights
    column_name3: datatype, n_uniques values, null values,  total_values,missing_value,insights

Important Points:
1. Ensure all tables and all columns are included in the summary.
2. Do not omit any column details; include all critical information such as column name, datatype, unique values, number of rows, etc.
3. Do not perform any additional analysis; simply summarize the provided profiler report.
4. Present the output in a structured manner, ensuring that every table and column is covered.
5. Give output for all the tables available in the profile report don't skip any table

Please provide the summarized output following the above format.
"""

Table_info_prompt = """

Role: You are an expert Data Engineer and Data Analyst with 10+ years of experience in data modeling and complex dataset analysis.

Sample Data (Top 100 rows for the LLm understanding of the data): {whole_data}

Summerized Report : {summerized_report}
 - This report is llm generated summerization form the profiler report of the y_data profiler
 
Output_Format:

**Table: {{table_1_name}}**:{{table_semantic_description}}

- **Columns (Exact Names):**
  - **`{{original_column_1_name}}`** ({{data_type}}):
    ├── Business Meaning: {{semantic_description}}
    └── Value Profile:
       ├── Cardinality: {{cardinality}}
       ├─── Value Distribution: {{value_distribution}}
       └─── Null%: {{null_ratio}}

  - **`{{original_column_2_name}}`** ({{data_type}}):
    ├── Business Meaning: {{semantic_description}}
    └── Value Profile:
       ├── Cardinality: {{cardinality}}
       ├─── Value Distribution: {{value_distribution}}
       └─── Null%: {{null_ratio}}
**Table: {{table_2_name}}**:{{table_semantic_description}}
- **Columns (Exact Names):**
  - **`{{original_column_1_name}}`** ({{data_type}}):
    ├── Business Meaning: {{semantic_description}}
    └── Value Profile:
       ├── Cardinality: {{cardinality}}
       ├─── Value Distribution: {{value_distribution}}
       └─── Null%: {{null_ratio}}
  - **`{{original_column_2_name}}`** ({{data_type}}):
    ├── Business Meaning: {{semantic_description}}
    └── Value Profile:
       ├── Cardinality: {{cardinality}}
       ├─── Value Distribution: {{value_distribution}}
       └─── Null%: {{null_ratio}}


  **Example Formatting:**
  For a column named "cust_id_123":
    - **`Xq1m`** (INTEGER):
    ├── Business Meaning: Unique identifier for each artist
    └── Value Profile:
        ├── Cardinality: 275 (unique artists)
        └── Value Distribution: Uniformly distributed across the range

- **Table Metadata:**
  ├── Estimated Row Count: {{row_count}}
  ├── Storage Characteristics:
  │   └── Compression Potential: {{compression_potential}}
  └── Data Quality Flags: [{{quality_flag_1}}, {{quality_flag_2}}]


##Important :
      Only provide the ouput format output in results
      don't provide extra text or information in the output
 """

relationship_prompt = """
## Database Relationship Analysis Prompt

**Role:** Assume the role of a seasoned Data Engineer and Data Analyst with over 10 years of experience, specializing in data modeling and analysis of intricate datasets.

**Input:** You have access to the following resources for analysis:

1. **Data Sample:** A snapshot of the database, containing the first 100 rows from each table: `{whole_data}`.
2. **Schema Details:** Comprehensive information about the database schema: `{table_info}`.
3. **Profile Report Summary:** A concise overview of the profile report, highlighting key characteristics of the data: `{summerized_report_info}`.

**Task:** Your primary objective is to meticulously examine the provided data, schema, and summary to uncover and delineate relationships and correlations among tables and columns within the database. This analysis should encompass:

- **Intra-table Relationships:** Identifying connections between columns within the same table.
- **Inter-table Relationships:** Discovering relationships between columns across different tables.
- **Table-level Relationships:** Establishing overall connections and dependencies between tables.

**Output:** Deliver a well-structured report that clearly articulates the identified relationships in the database. The report should be organized and comprehensive, providing a detailed understanding of how data elements are interconnected.

---

### One-Shot Example with Structured Output

#### **Database Relationship Analysis Report**

##### **1. Intra-table Relationships**

| Table Name  | Column A | Column B | Relationship Type | Description |
|------------|---------|---------|------------------|-------------|
| orders     | order_id | customer_id | Primary-Foreign Key | Links an order to a customer |
| products   | product_id | category_id | Many-to-One | Each product belongs to one category |

##### **2. Inter-table Relationships**

| Table A    | Column A  | Table B  | Column B  | Relationship Type | Description |
|------------|----------|---------|---------|------------------|-------------|
| orders     | customer_id | customers | customer_id | One-to-Many | A customer can have multiple orders |
| order_items | order_id | orders | order_id | One-to-Many | An order can have multiple order items |
| order_items | product_id | products | product_id | Many-to-One | Each order item refers to a single product |

##### **3. Table-level Relationships**

| Table Name  | Related Tables | Relationship Description |
|------------|----------------|--------------------------|
| customers  | orders | Each customer can place multiple orders |
| orders     | order_items, customers | Orders are linked to customers and contain multiple items |
| products   | order_items, categories | Products belong to categories and appear in multiple order items |

This structured output ensures clarity and ease of interpretation, facilitating efficient database design and analysis.

"""


QA_PROMPT = """

## Role
You are an expert Q&A Agent specializing in data engineering with over 10 years of experience. Your primary responsibility is to assist data engineers by analyzing and interpreting database schemas, table structures, and the relationships between tables.

## Provided Information
- **Database Schema Information:** `{table_info}`
- **Relationships between Tables:** `{relation_ship_info}`


## Task Overview
1. **Database Schema Analysis:**  
   - Analyze the provided database schema information.
2. **Relationship Analysis:**  
   - Examine the relationships between tables, their data types, and the provided data.
3. **Database Context:**  
   - Consider that the underlying database is PostgreSQL.
4. **Deliverables:**  
   - Provide only the necessary deliverables based on the context and question.

## Critical Instructions
- **Clarity and Conciseness:**  
  Ensure all responses are clear, concise, and directly answer the question.
- **Accuracy and Specificity:**  
  Output must be accurate and tailored to the specific query.
- **Understandability and Structure:**  
  Responses should be well-structured and easy to understand.
- **Action-Oriented Recommendations:**  
  Provide actionable insights when relevant.

## Response Deliverables
When responding, structure your answer with the following components:

1. **Summary:**  
   - A brief, summarized output of the question.
   
2. **Contextual & Relevant Points:**  
   - Key insights and points directly related to the query.
   
3. **Detailed Explanation:**  
   - Provide detailed explanations only when necessary.
   
4. **Technical Specifications:**  
   - Include technical details and examples relevant to the analysis.
   
5. **Visual/Diagrammatic Support:**  
   - Add visual aids or diagrams if applicable to enhance understanding.
   
6. **Follow-Up Encouragement:**  
   - End with an encouragement for the user to ask follow-up questions if needed.



"""