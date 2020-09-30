import numpy as np
import pandas as pd

# Load in File
filename = "mentalhealth.csv"
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
## needs to be fixed: yesConditions, maybeConditions, professionalConditions, gender, workPosition
