import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go

# load in the dataset
df = pd.read_pickle('mhit.pd')
gender = df.gender.value_counts()

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
    margin={
        "pad": 20
    },
    colorway=["#1ae843"]
)))
pio.templates.default = "plotly_dark+mhit"

# create the bar graph
fig = px.bar(gender, 
    y=["Male", "Female", "Gender\nminority"], 
    x=gender.array, 
    title="Responses by Gender", 
    orientation='h', 
    labels={
        "y": "Gender",
        "x": "Responses"
    }
)

# save the figure to an html doc
fig.write_html("docs/plotly.html")

# kinda hacky, but load the custom font into the generated HTML
with open("docs/plotly.html", "r+") as f:
    l = f.readlines()
    l[1] = '<head><meta charset="utf-8" /><link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,300;0,400;0,600;0,900;1,700&display=swap" rel="stylesheet"></head>'
    f.seek(0)
    f.writelines(l)
