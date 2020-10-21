import cleaningdata
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.decomposition import PCA

df = cleaningdata.df

def remove_self(df):
    """
    Transforms a dataframe by removing all self-employed rows
    """
    fits = df['selfEmployed'] == False
    df_trans = df[fits]

    return df_trans

def filter_categories(df):
    """
    Transforms a dataframe by removing any irrelevant rows
    """
    blacklist_cols = ['selfEmployed', 'whyPhysicalInterview', 'whyMentalInterview', 'yesConditions', 'maybeConditions', 'professionalConditions']
    out = df.drop(columns=blacklist_cols)

    return out

def clean_col(df, col):
    """
    Cleans a given column as necessary
    """
    my_col = df[col]

    try:
        if my_col.dtype == 'boolean':
            my_col.fillna(False, inplace=True)
    except:
        if my_col.dtype == 'bool':
            my_col.fillna(False, inplace=True)

    categorical_responses = {
        "knowOptions": "I am not sure",
        "prevOfferBenefits": "I don't know",
        "prevKnowOptions": "N/A (not currently aware)",
        "prevFormalDiscuss": "None did",
        "prevOfferResources": "None did",
        "prevAnonProtected": "I don't know",
        "prevDiscussMentalConseq": "I don't know",
        "prevDiscussPhysicalConseq": "None of them",
        "prevDiscussCoworker": "No, at none of my previous employers",
        "prevDiscussSupervisor": "I don't know",
        "prevMentalVsPhysical": "I don't know",
        "prevCoworkerNegConseq": "None of them",
        "badWorkplaceResponse": "Maybe/Not sure",
        "badWorkplaceResponseAffect": "Maybe",
        "stateLive": "California",
        "stateWork": "California",
    }

    if col in categorical_responses:
        my_col.fillna(categorical_responses[col], inplace=True)

def embed_categorical(df):
    """
    Transforms a dataframe by embedding each categorical row.
    Removes anything not relevant
    """

    le = preprocessing.LabelEncoder()
    for col in df.columns:
        # if df[col].dtype != 'bool':
            # print(col)
        # print(df[col].dtype)
        print(f'{col}: {df[col].dtype}')


        # my_col = df[col].fillna(method='pad')
        clean_col(df, col)
        df[col] = le.fit_transform(df[col])

    return df

df_trans = remove_self(df)
df_trans = filter_categories(df_trans)
df_trans = embed_categorical(df_trans)

will_discuss = df_trans['discussSupervisor'] == 2
wont_discuss = df_trans['discussSupervisor'] != 2
discussors = df_trans[will_discuss]
non_discussors = df_trans[wont_discuss]

pca = PCA(n_components=2)
pca.fit(df_trans)

discussors = pca.transform(discussors)
non_discussors = pca.transform(non_discussors)

x_d, y_d = list(zip(*discussors))
x_n, y_n = list(zip(*non_discussors))

plt.scatter(x_d, y_d, color='g')
plt.scatter(x_n, y_n, color='r')
plt.show()