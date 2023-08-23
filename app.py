from collections import Counter
from flask import Flask, request, jsonify
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)

# PostgreSQL connection settings
DB_URL = "postgresql://username:password@db_host:5432/db_name"
csv_dir = './data'  # Assuming you mount your data directory to /data in Docker


# A special function to process and clean the csv files and make it ready for further use.
def csv_formatter(filename: str):
    df = pd.read_csv(os.path.join(csv_dir, filename), sep='\t')
    df = df.replace(',', ' ', regex=True)
    df.columns = df.columns.str.rstrip(',')
    return df


# Define the ETL process and retrun a dataframe with the end result
def etl_process():
    # Load CSV files
    users_df = csv_formatter('users.csv')
    experiments_df = csv_formatter('user_experiments.csv')
    compounds_df = csv_formatter('compounds.csv')

    # Total experiments per user
    user_experiment_counts = experiments_df['user_id'].value_counts().to_dict()

    # Average experiments amount per user
    avg_experiments_per_user = experiments_df.groupby('user_id').size().mean()

    # User's most commonly experimented compound
    compound_counts = Counter()
    for compounds in experiments_df['experiment_compound_ids']:
        compound_counts.update(compounds.split(';'))
    most_common_compound_id = compound_counts.most_common(1)[0][0]
    most_common_compound = compounds_df[compounds_df['compound_id'] == most_common_compound_id]['compound_name'].values[0]

    processed_data = pd.DataFrame({
        'user_id': users_df['user_id'],
        'total_experiments': users_df['user_id'].map(user_experiment_counts),
        'average_experiments': avg_experiments_per_user,
        'most_common_compound': most_common_compound
    })
    
    return processed_data


# A function to upload processed data to PostgreSQL
def post_data():
    data = etl_process()
    engine = create_engine(DB_URL)
    data.to_sql('processed_data', engine, if_exists='replace', index=False)


# A basic homepage
@app.route("/", methods=['GET']) 
def index():
    return jsonify('Hello! This is the home page. Visit show_data to view the processed data'), 200


#to see the processed data in JSON format
@app.route("/show_data", methods=['GET']) 
def etl():
    result_df = etl_process()
    result = result_df.to_dict(orient='records')
    return jsonify(result), 200


#to upload data to database
@app.route('/trigger_etl', methods=['POST'])
def trigger_etl():  
    post_data()
    return {"message": "ETL process started"}, 200


if __name__ == '__main__':
    app.run(debug=True)
