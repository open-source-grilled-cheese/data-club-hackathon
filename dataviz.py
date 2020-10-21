import pandas as pd
# import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_pickle('mhit.pd')
gender = df.gender.value_counts()

fig = px.bar(gender, y=["Male", "Female", "Gender\nminority"], x=gender.array, title="Responses by Gender", template="plotly_dark", orientation='h', labels={
    "y": "Gender",
    "x": "Responses"
})
fig.update_layout(hoverlabel={
    "bgcolor": "black",
    "bordercolor": "black",
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
plot_bgcolor="black"
)
fig.update_traces(marker_color="#e8961a")
# fig.show()
fig.write_html("docs/plotly.html")

# kinda hacky, but load the custom font into our generated HTML
with open("docs/plotly.html", "r+") as f:
    l = f.readlines()
    l[1] = '<head><meta charset="utf-8" /><link href="https://fonts.googleapis.com/css2?family=Source+Code+Pro:ital,wght@0,300;0,400;0,600;0,900;1,700&display=swap" rel="stylesheet"></head>'
    f.seek(0)
    f.writelines(l)
