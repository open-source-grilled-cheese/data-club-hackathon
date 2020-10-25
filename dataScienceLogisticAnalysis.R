library(MASS)
library(plyr)
library(readr)
library(caTools)

# Reading in data from file
newdata <- read_csv("data/cleaned_mental-health-in-tech-2016.csv")

# Getting only rows of people who are not self-employed
work = newdata[newdata$selfEmployed == F,]

# Changing response variable to binary- combining No and Maybe
work$discussSupervisor <- mapvalues(work$discussSupervisor, from=c("Yes", "No", "Maybe"), to=c(1, 0, 0))

# Creating train and test datasets
set.seed(18414) # set for consistency
smp_siz = floor(0.80*nrow(work))
train_ind = sample(seq_len(nrow(work)),size = smp_siz)
train = work[train_ind,]
test = work[-train_ind,]

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

# ROC curve
library(ROCR)
pred = prediction(model.smaller$fitted.values, as.factor(work$discussSupervisor))
perf = performance(pred, measure = "tpr", x.measure = "fpr")
plot(perf, colorize=T)
abline(a=1, b=-1)
cutoff = 0.5

# Area under curve
auc.tmp = performance(pred, "auc")
auc = as.numeric(auc.tmp@y.values) # Since over 80%, it is a very good model for classification

# Prediction Code
#################################################
# Fitting smaller model with training data
model.smaller = glm(as.factor(discussSupervisor)~techComp + as.factor(leaveDifficulty) + as.factor(discussMentalConseq) + as.factor(discussCoworker) + as.factor(mentalVsPhysical) + as.factor(familyHistory) + as.factor(workRemote) + supervisor + support + onePersonShop, family="binomial", data = train)

# Seeing Predictions of train data
results = model.smaller$fitted.values
for (i in 1:(length(model.smaller$fitted.values))){
  results[i] = (model.smaller$fitted.values[i] >= cutoff)
}

for (i in 1:(length(model.smaller$fitted.values))){
  results[i] = (train$discussSupervisor[i] == results[i])
}
c = count(results)
trainpercent = (c$freq[2]/(c$freq[1] + c$freq[2]))

# Predicting test data
testdf = data.frame(test$techComp, as.factor(test$leaveDifficulty), as.factor(test$discussMentalConseq), as.factor(test$discussCoworker), as.factor(test$mentalVsPhysical), as.factor(test$familyHistory), as.factor(test$workRemote), test$supervisor, test$support, test$onePersonShop, data = test)
colnames(testdf) = c("techComp", "leaveDifficulty", "discussMentalConseq", "discussCoworker", "mentalVsPhysical", "familyHistory", "workRemote", "supervisor", "support", "onePersonShop")
guesses = predict.glm(model.smaller, newdata = testdf)
results = guesses

for (i in 1:(length(guesses))){
  results[i] = (guesses[i] >= cutoff)
}

for (i in 1:(length(guesses))){
  results[i] = (test$discussSupervisor[i] == results[i])
}
c = count(results)
testpercent = (c$freq[2]/(c$freq[1] + c$freq[2]))


