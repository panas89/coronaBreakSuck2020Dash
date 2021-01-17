import os
import yaml
import pandas as pd
import numpy as np

# ######################################################################################################################
DASH_DIR = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))
TOPIC_DIR = os.path.join(DASH_DIR, 'data/topicmodeling') 
NRE_DIR = os.path.join(DASH_DIR, 'data/nre') 
COVID_DIR = os.path.join(DASH_DIR, 'data/covid') 

INCIDENTS_PATH = os.path.join(COVID_DIR, 'conf_global.csv')
DEATHS_PATH = os.path.join(COVID_DIR, 'death_global.csv')
RECOVERED_PATH = os.path.join(COVID_DIR, 'recovered_global.csv')

COLS_TO_READ = ['sha', 'title', 'abstract', 'publish_time', 'affiliations_country',  # 'doi',
                'location_country', 'risk_factor_topic', 'risk_factor_topic_kw',
                'treatment_and_vaccine_topic', 'treatment_and_vaccine_topic_kw',
                'treatment_and_vaccine_common_name_topic_kw']

TABLE_COLS = ['title', 'abstract', 'publish_time',
              'affiliations_country']  # , 'location_country']#,'doi']

CLASSES_SUBCLASSES = [col for col in COLS_TO_READ if 'topic' in col and 'kw' not in col]

MAX_DATE = pd.to_datetime("today")
MAX_WEEK = MAX_DATE.isocalendar()[1]

# ----------------------------------------------------------------------------------------------------------------------
def load_topic_modeling_data(file_path, cols_to_read, max_date) -> pd.DataFrame:

    # Load data
    df = pd.read_csv(file_path, parse_dates=[ 'publish_time'], usecols=cols_to_read)

    # Create DOI col
    # df['doi'] = ['https://doi.org/'+str(doi) for doi in df['doi'] if doi!=np.nan]

    # Create date col
    df['date'] = [date.strftime('%m-%d-%Y') for date in df['publish_time']]

    # Fix unknown/wrong publication datetimes to today
    df.loc[df['publish_time'] > max_date, 'publish_time'] = max_date

    return df

# ######################################################################################################################
# Load Topic Modeling Data
dataset2df = {}
for path in os.listdir(TOPIC_DIR):
    # create file_path
    full_path = os.path.join(TOPIC_DIR, path)

    # create dataset name
    raw_name = path.split('.')[0]  # remove .csv
    name = " ".join(raw_name.split('_')).title()
    # load dataset and store to dict
    try:
        dataset2df[name] = load_topic_modeling_data(full_path, COLS_TO_READ, MAX_DATE)
        print('GOOD', full_path)
    except Exception as e:
        print('BAD', full_path, '\n', e)

# Create dataset name,file_path dict for Topic Modeling
topic_dataset_name2path = {}
for path in os.listdir(TOPIC_DIR):

    # create file_path
    full_path = os.path.join(TOPIC_DIR, path)

    # create dataset name
    raw_name = path.split('.')[0]  # remove .csv
    name = " ".join(raw_name.split('_')).title()
    
    topic_dataset_name2path[name] = full_path

# Load Forecasting Data
df_inc = pd.read_csv(INCIDENTS_PATH, parse_dates=True)
df_death = pd.read_csv(DEATHS_PATH, parse_dates=True)
df_rec = pd.read_csv(RECOVERED_PATH, parse_dates=True)

# Global Definitions
DATASET_NAMES = list(dataset2df.keys())
LOCATIONS_COUNTRIES = df_inc['Country/Region'].unique()

# ################################################################################################## 
# # Relation table data
# RELATION_PATH = './data/relations/classified_dims_Publications_hi_90_95_covid_relation.csv'
# RELATION_TABLE_COLS = ['title','publish_time','relations']

# # load relation data
# df_relations = pd.read_csv(RELATION_PATH)

# ################################################################################################## 

# Load NRE data
nre_dataset_name2path = {}
for path in os.listdir(NRE_DIR):
    # create file_path
    full_path = os.path.join(NRE_DIR, path)

    # create dataset name
    raw_name = path.split('.')[0]  # remove .csv
    name = " ".join(raw_name.split('_')).title()
    
    nre_dataset_name2path[name] = full_path

print(nre_dataset_name2path)
# filenames = glob.glob("data/relations/*.csv")
# meaningfull_filenames = [
#     "Top 5-10\% High impact papers",
#     # "Semantic scholar COVID-19 papers",
#     # "COVID-19 Clinical Trials",
#     "Top 5\% High impact papers",
# ]


# Create data dictionary from yaml  
yaml_path = os.path.join(DASH_DIR, "assets/Davids_interest_meshed.yaml")
with open(yaml_path) as f:
    data_yml = yaml.load(f, Loader=yaml.FullLoader)

# Reorganize the information
class_subclass2kws = dict(
    (c, data_yml[c][f"{c}_common_name"]["kw"]) 
    for c in data_yml.keys() if c != "disease_name"
)