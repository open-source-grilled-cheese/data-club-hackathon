library(MASS)
library(plyr)
library(readr)

# Reading in data from file
newdata <- read_csv("newdata.csv")

# Getting only rows of people who are not self-employed
work = newdata[newdata$selfEmployed == F,]

# Changing response variable to binary- combining No and Maybe (can change)
work$discussSupervisor <- mapvalues(work$discussSupervisor, from=c("Yes", "No", "Maybe"), to=c(0, 1, 1))

# Creating and viewing massive model
model.regress = glm(as.factor(discussSupervisor)~as.factor(nEmployees) + techComp + as.factor(offerBenefits) + as.factor(formalDiscuss) + as.factor(offerResources) + as.factor(anonProtected) + as.factor(leaveDifficulty) + as.factor(discussMentalConseq) + as.factor(discussPhysicalConseq) + as.factor(discussCoworker) + as.factor(mentalVsPhysical) + as.factor(coworkerNegConseq) + as.factor(familyHistory) + as.factor(mentalPast) + as.factor(mentalCurrent) + as.factor(professionalDiagnose) + soughtTreatment + age + as.factor(gender) + as.factor(countryLive) + as.factor(workRemote) + backend + frontend + supervisor + devOps + other + support + onePersonShop + designer + advocate + execLeader + sales + hr, family="binomial", data = work)
summary(model.regress)

# Testing to find unnecessary variables
stepAIC(model.regress, direction = "backward")

# Creating and viewing new model, given by stepAIC
model.smaller = glm(as.factor(discussSupervisor)~techComp + as.factor(leaveDifficulty) + as.factor(discussMentalConseq) + as.factor(discussCoworker) + as.factor(mentalVsPhysical) + as.factor(familyHistory) + as.factor(workRemote) + supervisor + support + onePersonShop, family="binomial", data = work)
summary(model.smaller)

# Finding p-val: Since p-val is very small, shows that smaller model has some utility
cs = 1514.5-885.73
df = 1145-1126
pval = pchisq(cs, df, lower.tail=F)
pval

# Comparing smaller model with larger model
cs = 885.73 - 811.05
df = 1126 - 1049
pval = pchisq(cs, df, lower.tail = F)
pval # since p-val is high (> 0.05), we should use the smaller model

# Hoslem test- since p-value is high, shows that the model actually fits well
library(ResourceSelection)
hoslem.test(model.smaller$y, fitted(model.smaller))
