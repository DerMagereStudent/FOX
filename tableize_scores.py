import os
import csv
import pandas as pd

# Function to parse the CSV file and extract scores
def parse_results_file(file_path):
    roc_auc, f1_score = None, None
    with open(file_path, 'r') as f:
        reader = csv.reader(f, delimiter=';')
        for row in reader:
            if row and row[0] == 'ROC_AUC_SCORE weighted':
                roc_auc = round(float(row[1]), 3)
            elif row and row[0] == 'F1_SCORE weighted':
                f1_score = round(float(row[1]), 3)
    return roc_auc, f1_score

# Function to process all files in a folder
def process_results_folder(folder_path):
    roc_auc_table = {}
    f1_score_table = {}

    for file_name in os.listdir(folder_path):
        if file_name.endswith('_results.csv'):
            # Extract dataset and member function from file name
            base_name = file_name[:-12]  # Remove '_results.csv'
            dataset_name, member_function = base_name.rsplit('_', 1)

            # Parse the file to get scores
            file_path = os.path.join(folder_path, file_name)
            roc_auc, f1_score = parse_results_file(file_path)

            # Populate the tables
            if dataset_name not in roc_auc_table:
                roc_auc_table[dataset_name] = {}
                f1_score_table[dataset_name] = {}

            roc_auc_table[dataset_name][member_function] = roc_auc
            f1_score_table[dataset_name][member_function] = f1_score

    return roc_auc_table, f1_score_table

# Function to determine the best function for each dataset
def add_best_column(score_table):
    best_column = {}
    for dataset, scores in score_table.items():
        if scores:
            # Filter out None values
            valid_scores = {key: value for key, value in scores.items() if value is not None}
            if valid_scores:  # Ensure there are valid scores
                best_function = max(valid_scores, key=valid_scores.get)
                best_column[dataset] = best_function
            else:
                best_column[dataset] = None  # No valid scores
    return best_column

# Function to convert tables to dataframes and save as CSV
def save_tables_as_csv(roc_auc_table, f1_score_table, output_folder):
    # Convert to DataFrame
    roc_auc_df = pd.DataFrame(roc_auc_table).transpose()
    f1_score_df = pd.DataFrame(f1_score_table).transpose()

    # Add "best" column to DataFrames
    roc_auc_df['best'] = pd.Series(add_best_column(roc_auc_table))
    f1_score_df['best'] = pd.Series(add_best_column(f1_score_table))

    # Save to CSV
    roc_auc_df.to_csv(os.path.join(output_folder, 'roc_auc_scores.csv'))
    f1_score_df.to_csv(os.path.join(output_folder, 'f1_scores.csv'))

# Main execution
def main():
    input_folder = './results/'  # Replace with your folder path
    output_folder = './scores/'  # Replace with your folder path

    roc_auc_table, f1_score_table = process_results_folder(input_folder)
    save_tables_as_csv(roc_auc_table, f1_score_table, output_folder)

if __name__ == "__main__":
    main()
