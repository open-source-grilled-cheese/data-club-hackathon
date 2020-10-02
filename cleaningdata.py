import numpy as np
import pandas as pd

# Load in File
filename = "mental-heath-in-tech-2016.csv"
df = pd.read_csv(filename)

# Make column names easier to work with
df.columns = ['selfEmployed', 'nEmployees', 'techComp', 'techRole', 'offerBenefits', 'knowOptions', 'formalDiscuss', 'offerResources', 'anonProtected', 'leaveDifficulty', 'discussMentalConseq', 'discussPhysicalConseq', 'discussCoworker', 'discussSupervisor', 'mentalVsPhysical', 'coworkerNegConseq', 'medCoverage', 'knowResources', 'revealClient', 'revealClientConseq', 'revealCoworker', 'revealCoworkerConseq', 'prodAffect', 'prodAffectPercent', 'prevEmployers', 'prevOfferBenefits', 'prevKnowOptions', 'prevFormalDiscuss', 'prevOfferResources', 'prevAnonProtected', 'prevDiscussMentalConseq', 'prevDiscussPhysicalConseq', 'prevDiscussCoworker', 'prevDiscussSupervisor', 'prevMentalVsPhysical', 'prevCoworkerNegConseq', 'physicalInterview', 'whyPhysicalInterview', 'mentalInterview', 'whyMentalInterview', 'hurtCareer', 'viewNegatively', 'shareFriendsFamily', 'badWorkplaceResponse', 'badWorkplaceResponseAffect', 'familyHistory', 'mentalPast', 'mentalCurrent', 'yesConditions', 'maybeConditions', 'professionalDiagnose', 'professionalConditions', 'soughtTreatment', 'interferesTreated', 'interferesNotTreated', 'age', 'gender', 'countryLive', 'stateLive', 'countryWork', 'stateWork', 'workPosition', 'workRemote']

# Change column data types
# Bools
for col in ['selfEmployed', 'prevEmployers', 'soughtTreatment']:
    df[col] = df[col].astype(bool)

# Booleans (Allows for null values, unlike bool)
for col in ['techComp', 'techRole', 'medCoverage']:
    df[col] = df[col].astype("boolean")

# Unordered Categorical
for col in ['offerBenefits', 'knowOptions', 'formalDiscuss', 'offerResources', 'anonProtected', 'leaveDifficulty', 'discussMentalConseq', 'discussPhysicalConseq', 'discussCoworker', 'discussSupervisor', 'mentalVsPhysical', 'coworkerNegConseq', 'knowResources', 'revealClient', 'revealClientConseq', 'revealCoworker', 'revealCoworkerConseq', 'prodAffect', 'prevOfferBenefits', 'prevKnowOptions', 'prevFormalDiscuss', 'prevOfferResources', 'prevAnonProtected', 'prevDiscussMentalConseq', 'prevDiscussPhysicalConseq', 'prevDiscussCoworker', 'prevDiscussSupervisor', 'prevMentalVsPhysical', 'prevCoworkerNegConseq', 'physicalInterview', 'mentalInterview', 'hurtCareer', 'viewNegatively', 'shareFriendsFamily', 'badWorkplaceResponse', 'badWorkplaceResponseAffect', 'familyHistory', 'mentalPast', 'mentalCurrent', 'yesConditions', 'maybeConditions', 'professionalDiagnose', 'professionalConditions', 'interferesTreated', 'interferesNotTreated', 'gender', 'countryLive', 'stateLive', 'countryWork', 'stateWork', 'workPosition', 'workRemote']:
    df[col] = df[col].astype('category')

# Ordered Categorical
nEmployeesCat = pd.api.types.CategoricalDtype(categories=['1-5', '6-25', '26-100', '100-500', '500-1000', 'More than 1000'], ordered=True)
df['nEmployees'] = df['nEmployees'].astype(nEmployeesCat)

prodAffectPercentCat = pd.api.types.CategoricalDtype(categories=['1-25%', '26-50%', '51-75%', '76-100%'], ordered=True)
df['prodAffectPercent'] = df['prodAffectPercent'].astype(prodAffectPercentCat)

## possible ordered: leaveDifficulty
## needs to be fixed: gender
def translate_gender(gender_val):
    """
    Translates a gender to "Male", "Female", or "Other"
    """
    # Base case
    if type(gender_val) is not str:
        return 'Other'

    # Clean the value
    gender_val = ''.join([i for i in gender_val if i.isalpha() or i.isspace()]).lower().strip()
    
    # Decision tree
    if 'woman' in gender_val:
        if 'trans' in gender_val or 'queer' in gender_val:
            return 'Other'
        return 'Female'
    elif 'fem' in gender_val:
        other_ident = ['rough', 'bodied', 'multi', 'fluid','other']
        if any(i in gender_val for i in other_ident):
            return 'Other'
        return 'Female'
    elif 'dude' in gender_val:
        return 'Male'
    elif 'ma' in gender_val:
        other_ident = ['nb', 'trans', 'hu','queer']
        if any(i in gender_val for i in other_ident):
            return 'Other'
        return 'Female'
    elif gender_val in ['f', 'fm', 'afab']:
        return 'Female'
    elif gender_val in ['m']:
        return 'Male'
    else:
        return 'Other'
    
        
# Transform genders
df['gender'] = df['gender'].map(translate_gender, na_action=None).fillna('Other')

# Creating a Bool column if a person is each work position
# Categories for work positions
workPos = {'Back-end Developer':'backend', 'Front-end Developer':'frontend', 'Supervisor/Team Lead':'supervisor', 'DevOps/SysAdmin':'devOps', 'Other':'other', 'Support':'support', 'One-person shop':'onePersonShop', 'Designer':'designer', 'Dev Evangelist/Advocate':'advocate', 'Executive Leadership':'execLeader', 'Sales':'sales', 'HR':'hr'}

# creates column
for col in workPos.values():
    df[col] = False

for i, entry in enumerate(df['workPosition']): # for each person
    for position in workPos.keys(): # for each possible position
        if position in entry:
            df.at[i, workPos[position]] = True
        else:
            df.at[i, workPos[position]] = False

#Creating a bool column if a person has each condition for each method of diagnosis
# Categories for mental conditions
mentalCond = {'Mood Disorder (Depression, Bipolar Disorder, etc)':'mood', 'Anxiety Disorder (Generalized, Social, Phobia, etc)':'anxiety', 'Attention Deficit Hyperactivity Disorder':'adhd', 'Post-traumatic Stress Disorder':'ptsd', 'Obsessive-Compulsive Disorder':'ocd', 'Personality Disorder (Borderline, Antisocial, Paranoid, etc)':'personality', 'Stress Response Syndromes':'srs', 'Substance Use Disorder':'substance', 'Eating Disorder (Anorexia, Bulimia, etc)':'eating', 'Addictive Disorder':'addictive', 'Psychotic Disorder (Schizophrenia, Schizoaffective, etc)':'psychotic', 'Dissociative Disorder':'disassociative', 'Other':'other'}

diagnoses = {'yesConditions':'Yes', 'maybeConditions':'Maybe', 'professionalConditions':'Profess'}

# Creates columns
for d in diagnoses.values():
    for col in mentalCond.values():
        df[col + d] = False

for d in diagnoses.keys(): # For each type of diagnoses
    for i, entry in enumerate(df[d]): # For each person
        for condition in mentalCond.keys(): # For each condition
            if entry != entry: # Checks if NaN (leaves it false)
                continue
            if condition in entry:
                df.at[i, mentalCond[condition]+diagnoses[d]] = True
            else:
                df.at[i, mentalCond[condition]+diagnoses[d]] = False

