
import pandas as pd
import numpy as np
import datetime
import pickle
import pyLDAvis.gensim

TOPIC_MODELLING_PATH = './data/topicmodels/'

COLS_TO_READ = ['sha', 'title', 'abstract', 'publish_time', 'affiliations_country',
                'location_country', 'risk_factor_topic', 'risk_factor_topic_kw',
                'diagnostic_topic', 'diagnostic_topic_kw',
                'treatment_and_vaccine_topic', 'treatment_and_vaccine_topic_kw',
                'outcome_topic', 'outcome_topic_kw', 'risk_factor_common_name_topic',
                'risk_factor_common_name_topic_kw', 'gender_topic', 'gender_topic_kw',
                'age_topic', 'age_topic_kw', 'disease_comorbidity_topic',
                'disease_comorbidity_topic_kw', 'smoking_topic', 'smoking_topic_kw',
                'exercise_topic', 'exercise_topic_kw', 'occupation_topic',
                'occupation_topic_kw', 'weather_topic', 'weather_topic_kw',
                'diagnostic_common_name_topic', 'diagnostic_common_name_topic_kw',
                'symptom_topic', 'symptom_topic_kw', 'imaging_diagnosis_topic',
                'imaging_diagnosis_topic_kw', 'clinical_diagnosis_topic',
                'clinical_diagnosis_topic_kw', 'genetic_diagnosis_topic',
                'genetic_diagnosis_topic_kw', 'treatment_and_vaccine_common_name_topic',
                'treatment_and_vaccine_common_name_topic_kw',
                'outcome_common_name_topic', 'outcome_common_name_topic_kw',
                'clinical_outcome_topic', 'clinical_outcome_topic_kw']

df = pd.read_csv(TOPIC_MODELLING_PATH+'pcf_topic_data.csv',parse_dates=True,usecols=COLS_TO_READ)

table_cols = ['title', 'abstract', 'publish_time', 
              'affiliations_country', 'location_country']

df['publish_time'] = pd.to_datetime(df['publish_time'])

max_date = pd.to_datetime("today")

df.loc[df['publish_time']>max_date,'publish_time'] = max_date

df['times_str'] = [str(time_point)[:10] for time_point in df['publish_time']]

# print(df['publish_time'].groupby(df["publish_time"].dt.date).count())
# print(df['times_str'].groupby(df["times_str"]).count().index.values)
# print(df['times_str'].groupby(df["times_str"]).count().values)

classes_sub_classes = [col for col in df.columns if 'topic' in col and 'kw' not in col]

def getClassesDescriptionMap(df):

    classes_sub_classes = [col for col in df.columns if 'topic' in col and 'kw' not in col]

    classes_topics_descr = {class_sub_class:{'topic_' + str(topic) : 
                                                {'name':'Topic ' + str(topic+1), 
                                                'times':df.loc[df[class_sub_class]==topic,'times_str'].groupby(df["times_str"]).count().index.values,
                                                'counts':df.loc[df[class_sub_class]==topic,'times_str'].groupby(df["times_str"]).count().values,
                                                'keywords':df.loc[df[class_sub_class]==topic,class_sub_class + '_kw'].unique()[0].split(', ')}
                                            for topic in df[class_sub_class].unique() if topic != -1}
                                for class_sub_class in classes_sub_classes
                            }
    return classes_topics_descr

classes_topics_descr = getClassesDescriptionMap(df)


time_diff = (df['publish_time'].max()-df['publish_time'].min()).days
print(df.shape)
print(time_diff)
print(df['publish_time'].max())


##### incident cases

def preprocCases(df,non_date_cols):
    """Method that returns difference of cases every day and dates."""

    non_date_cols = ['Province/State', 'Country/Region', 'Lat', 'Long']
    date_cols = [col for col in df.columns if col not in non_date_cols]
    dates = pd.to_datetime(date_cols)
    data = pd.Series([0]+list(df[date_cols].sum(axis=0))).diff()[1:]

    return dates,data

df_inc = pd.read_csv('./data/conf_global.csv',parse_dates=True)#,usecols=COLS_TO_READ)
df_death = pd.read_csv('./data/death_global.csv',parse_dates=True)#,usecols=COLS_TO_READ)
df_rec = pd.read_csv('./data/recovered_global.csv',parse_dates=True)#,usecols=COLS_TO_READ)
non_date_cols = ['Province/State', 'Country/Region', 'Lat', 'Long']


location_country = df_inc['Country/Region'].unique()



dates_inc , inc_data = preprocCases(df=df_inc,non_date_cols=non_date_cols)
dates_death , death_data = preprocCases(df=df_death,non_date_cols=non_date_cols)
dates_rec , rec_data = preprocCases(df=df_rec,non_date_cols=non_date_cols)



# print(df_inc.head(3))
# print(df_inc.columns)
# assert(len(inc_data)==len(dates_inc))
# print(inc_data)

# read visualization
# with open(TOPIC_MODELLING_PATH+class_sub_class.replace('_topic','')+'/vis.pickle', 'rb') as mod:
#     vis = pickle.load(mod)