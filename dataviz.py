import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# load in the dataset
df = pd.read_pickle('mhit.pd')

# create custom template off of plotly_dark to match the site
pio.templates["mhit"] = go.layout.Template(dict(layout=go.Layout(
    hoverlabel={
        "bgcolor": "black",
        "bordercolor": "#1ae843",
        "font": {
            "family": "Source Code Pro",
            "color": "#1ae843"
        }
    },
    font={
        "family": "Source Code Pro",
        "color": "#1ae843"
    },
    paper_bgcolor="black",
    plot_bgcolor="black",
    margin=dict(
        pad=20
    ),
    colorway=["#1ae843"]
)))
pio.templates.default = "plotly_dark+mhit"

# create the bar graph
gender = df.gender.value_counts()
fig = px.bar(gender, 
    y=["Male", "Female", "Gender minority"], 
    x=gender.array, 
    title="Responses by Gender", 
    orientation='h', 
    labels={
        "y": "Gender",
        "x": "Responses"
    }
)
fig.write_html("docs/gender.html")

fig = px.bar(df.nEmployees.value_counts().sort_index(),
    title="Responses by Company Size",
    labels={
        "index": "Employees in Company",
        "value": "Responses"
    }
)
fig.update_layout(showlegend=False)
fig.write_html("docs/company_size.html")

import pca
fig = px.scatter(x=pca.discussorX, y=pca.discussorY)
fig.add_trace(
    go.Scatter(
        x=pca.nondiscussorX,
        y=pca.nondiscussorY,
        mode="markers",
        marker=dict(
            color="#e8961a"
        )
    )
)
fig.update_layout(
    showlegend=False,
    xaxis_title="",
    yaxis_title="",
    xaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False
    ),
    title="Principle Component Analysis Plot"
)
fig.write_html("docs/pca.html")

aic = pd.read_csv('aic.csv')
fig = px.bar(aic.sort_values(by="Slope"), 
    x="Question", 
    y="Slope", 
    title="Logistic Regression Model Weights")
fig.write_html("docs/aic.html")

pvals = pd.read_csv('logistic_regression.csv')
fig = px.bar(pvals.sort_values(by='p-value'), 
    x="Question",y="p-value", 
    log_y=True,
    title="P-values for predictor variables"
)
fig.write_html("docs/pval.html")

train = pd.read_csv('best_calc.csv')
fig = px.bar(train,
    title="Accuracy of Model on Training/Validation Datasets",
    y="Dataset",
    x="Prediction Accuracy (%)",
    orientation="h"
)
fig.write_html("docs/training.html")

figs = ["docs/gender.html", "docs/company_size.html", "docs/pca.html", "docs/aic.html", "docs/pval.html", "docs/training.html"]

# kinda hacky, but load the custom font into the generated HTML
for figure in figs:
    with open(figure, "r+") as f:
        l = f.readlines()
        l[1] = '<head><meta charset="utf-8"/><link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,300;0,400;0,600;0,900;1,700&display=swap" rel="stylesheet"></head>'
        f.seek(0)
        f.writelines(l)
