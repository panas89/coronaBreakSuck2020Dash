import pandas as pd
import numpy as np

# ######################################################################################################################
TOPIC_MODELING_PATH = './data/topicmodels/pcf_topic_data.csv'
INCIDENTS_PATH = './data/conf_global.csv'
DEATHS_PATH = './data/death_global.csv'
RECOVERED_PATH = './data/recovered_global.csv'

COLS_TO_READ = ['sha', 'title', 'abstract', 'publish_time', 'affiliations_country',#'doi',
                'location_country', 'risk_factor_topic', 'risk_factor_topic_kw',
                # 'diagnostic_topic', 'diagnostic_topic_kw',
                'treatment_and_vaccine_topic', 'treatment_and_vaccine_topic_kw',
                # 'kidney_disease_topic', 'kidney_disease_topic_kw',
                # 'outcome_topic', 'outcome_topic_kw', 'risk_factor_common_name_topic',
                # 'risk_factor_common_name_topic_kw', 'gender_topic', 'gender_topic_kw',
                # 'age_topic', 'age_topic_kw', 'disease_comorbidity_topic',
                # 'disease_comorbidity_topic_kw', 'smoking_topic', 'smoking_topic_kw',
                # 'exercise_topic', 'exercise_topic_kw',
                # # 'occupation_topic','occupation_topic_kw', 
                # 'weather_topic', 'weather_topic_kw',
                # 'diagnostic_common_name_topic', 'diagnostic_common_name_topic_kw',
                # 'symptom_topic', 'symptom_topic_kw', 'imaging_diagnosis_topic',
                # 'imaging_diagnosis_topic_kw', 'clinical_diagnosis_topic',
                # 'clinical_diagnosis_topic_kw', 'genetic_diagnosis_topic',
                # 'genetic_diagnosis_topic_kw', 'treatment_and_vaccine_common_name_topic',
                'treatment_and_vaccine_common_name_topic_kw']
                # 'outcome_common_name_topic', 'outcome_common_name_topic_kw',
                # 'clinical_outcome_topic', 'clinical_outcome_topic_kw']

TABLE_COLS = ['title', 'abstract', 'publish_time', 
              'affiliations_country', 'location_country']#,'doi']

CLASSES_SUBCLASSES = [col for col in COLS_TO_READ if 'topic' in col and 'kw' not in col]

MAX_DATE = pd.to_datetime("today")
MAX_WEEK = MAX_DATE.isocalendar()[1]

COLORS = ['#4285F4',
          "#DB4437",
          "#F4B400",
          "#0F9D58",
          "#666666",
          "#FF00BF",
          "#e6ab02"]

# ----------------------------------------------------------------------------------------------------------------------
def load_topic_modeling_data(file_path, cols_to_read, max_date) -> pd.DataFrame:

    # Load data
    df = pd.read_csv(file_path, parse_dates=['publish_time'], usecols=COLS_TO_READ)

    # Create DOI col
    # df['doi'] = ['https://doi.org/'+str(doi) for doi in df['doi'] if doi!=np.nan]

    # Create date col 
    df['date'] = [date.strftime('%m-%d-%Y') for date in df['publish_time']]

    # Fix unknown/wrong publication datetimes to today   
    df.loc[df['publish_time'] > max_date, 'publish_time'] = max_date

    return df 

# ######################################################################################################################

# Load Data
df = load_topic_modeling_data(file_path=TOPIC_MODELING_PATH, cols_to_read=COLS_TO_READ, max_date=MAX_DATE)
df_inc = pd.read_csv(INCIDENTS_PATH, parse_dates=True) 
df_death = pd.read_csv(DEATHS_PATH, parse_dates=True) 
df_rec = pd.read_csv(RECOVERED_PATH, parse_dates=True) 


# Global Definitions
LOCATIONS_COUNTRIES = df_inc['Country/Region'].unique()
TIME_DIFF = (df['publish_time'].max()-df['publish_time'].min()).days
