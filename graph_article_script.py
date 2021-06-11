
#################################################################################
## How does the relationship between car weight and horsepower vary by origin? ##
#################################################################################

#################
## iteration 1 ##
#################

import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv("CARS.csv")

fig = go.Figure()

fig.add_trace(go.Scatter(x = df["Horsepower"], y = df["Weight"],
                        mode = "markers"))

fig.show()


#################
## iteration 2 ##
#################

#create a column in the dataframe for the color variable
df["color"] = "#2471A3"

fig = go.Figure()

fig.add_trace(go.Scatter(x = df["Horsepower"], y = df["Weight"],
                        mode = "markers",
                         marker = dict(color = df["color"].tolist()[0]))) #only pass 1 element of the color variable to the color parameter

fig.update_layout(plot_bgcolor = "white",
                 font = dict(color = "#909497"),
                 title = dict(text = "Car Weight Against Horsepower"),
                 xaxis = dict(title = "Horsepower (hp)", linecolor = "#909497"),
                 yaxis = dict(title = "Weight (kgs)", tickformat = ",", linecolor = "#909497"))

fig.show()

#################
## iteration 3 ##
#################

#update the color column so that each origin has a different color
df["Color"] = "#2471A3"
df.loc[df["Origin"] == "Asia", "Color"] = "#BA4A00"
df.loc[df["Origin"] == "USA", "Color"] = "#884EA0"

fig = go.Figure()

#create the for loop to iterate over each origin value 
#this creates separate data layers for each origin location to populate the scatter graph
for area in df["Origin"].unique(): 
    df_plot = df.loc[df["Origin"] == area].copy() 
    
    fig.add_trace(go.Scatter(x = df_plot["Horsepower"], y = df_plot["Weight"],
                            mode = "markers",
                            marker = dict(color = df_plot["Color"].tolist()[0]),
                            name = df_plot["Origin"].tolist()[0] # used to label the legend
                            ))
 
fig.update_layout(plot_bgcolor = "white",
                 font = dict(color = "#909497"),
                 title = dict(text = "Car Weight Against Horsepower"),
                 xaxis = dict(title = "Horsepower (hp)", linecolor = "#909497"),
                 yaxis = dict(title = "Weight (kgs)", tickformat = ",", linecolor = "#909497"))


fig.show()

#################
## iteration 4 ##
#################

from plotly.subplots import make_subplots

#create variables in the data frame for the row and column numbers to be used to generate the subplot
df["row"] = 1
df["col"] = 1
df.loc[df["Origin"] == "Asia", "col"] = 2
df.loc[df["Origin"] == "USA", "col"] = 3

#create the blank graph object with make_subplots(...) instead of go.Figure()
fig = make_subplots(rows = 1, cols = 3, #provide the dimensions of the subplot
                    subplot_titles= ["Europe", "Asia", "USA"]) #give each subplot a title

for area in df["Origin"].unique(): 
    df_plot = df.loc[df["Origin"] == area].copy() 
    
    fig.add_trace(go.Scatter(x = df_plot["Horsepower"], y = df_plot["Weight"],
                            mode = "markers",
                            marker = dict(color = df_plot["Color"].tolist()[0]),
                            name = df_plot["Origin"].tolist()[0]  
                            ), row = df_plot["row"].tolist()[0], col = df_plot["col"].tolist()[0]) #pass the row and column variables to the plot as arguments

fig.update_layout(plot_bgcolor = "white",
                 font = dict(color = "#909497"),
                 title = dict(text = "Car Weight Against Horsepower"))

fig.update_xaxes(title = "Horsepower (hp)", linecolor = "#909497") 
fig.update_yaxes(title = "Weight (kgs)", tickformat = ",", linecolor = "#909497") 


fig.show()


#################
## iteration 5 ##
#################

fig = make_subplots(rows = 1, cols = 3,
                    subplot_titles= ["Europe", "Asia", "USA"],
                    shared_yaxes = True) #only y axes can be shared amongst subplots on this graph because they all have a different x axis

for area in df["Origin"].unique(): 
    df_plot = df.loc[df["Origin"] == area].copy()
    
    fig.add_trace(go.Scatter(x = df_plot["Horsepower"], y = df_plot["Weight"],
                            mode = "markers",
                            marker = dict(color = df_plot["Color"].tolist()[0]),
                            ), row = df_plot["row"].tolist()[0], col = df_plot["col"].tolist()[0])
 
fig.update_layout(plot_bgcolor = "white",
                 font = dict(color = "#909497"),
                 title = dict(text = "Car Horsepower Against Weight"),
                 showlegend = False)

#fix the x axes range because shared_xaxes can't be used
fig.update_xaxes(linecolor = "white", range = [0, 510], tickvals = [0, 100, 200, 300, 400, 500]) 
fig.update_yaxes(tickformat = ",", linecolor = "white") 

#use the add_annotations() command to generate both the x-axis and y-axis titles instead of update_axes(title = ...) and update_yaxes(title = ...)

#x axis title
fig.add_annotation(text = "Horsepower (hp)",
                    xref = "paper",
                    yref = "paper",
                    x = 0.5,
                    y = -0.1,
                    showarrow = False)

#y axis title
fig.add_annotation(text = "Weight (kgs)",
                    xref = "paper",
                    yref = "paper",
                    x = -0.08,
                    y = 0.5,
                    showarrow = False,
                    textangle = -90)

fig.show()

#################
## iteration 6 ##
#################

import statsmodels
import numpy as np

#create the table that will hold the annotation text
for car_type in df['Type'].unique():
    df[str(car_type)] = (df['Type'] == car_type).astype(int)

#calculate average weight and horsepower for each origin and proportion of Sports Cars, SUVs and Trucks
df_annotations = df.groupby(["Origin"]).agg(Mean_Weight = ("Weight", "mean"),
                                            Mean_Horsepower = ("Horsepower", "mean"),
                                            Car_Count = ("Origin", "count"),
                                            Sports_Car_Prop = ("Sports", "sum"),
                                            SUV_Prop = ("SUV", "sum"),
                                            Truck_Prop = ("Truck", "sum")).reset_index()

df_annotations["Sports_Car_Prop"] = df_annotations["Sports_Car_Prop"] / df_annotations["Car_Count"]
df_annotations["SUV_Prop"] = df_annotations["SUV_Prop"] / df_annotations["Car_Count"]
df_annotations["Truck_Prop"] = df_annotations["Truck_Prop"] / df_annotations["Car_Count"]

#calculate the line of gradient of the line of best fit for each origin
GRADIENT_EUROPE = np.polyfit(df.loc[df["Origin"] == "Europe", "Horsepower"], df.loc[df["Origin"] == "Europe", "Weight"], 1)[0]
GRADIENT_ASIA = np.polyfit(df.loc[df["Origin"] == "Asia", "Horsepower"], df.loc[df["Origin"] == "Asia", "Weight"], 1)[0]
GRADIENT_USA = np.polyfit(df.loc[df["Origin"] == "USA", "Horsepower"], df.loc[df["Origin"] == "USA", "Weight"], 1)[0]

#create the text that will appear above each subplot
TEXT_EUROPE = 'On average European cars have the most power at <br><span style="color:#2471A3">{:.0f}hp</span> and the best weight to horsepower ratio, where <br>a 1 unit increase in hp will have a <span style="color:#2471A3">{:.1f}kg</span> rise in weight. <br>This is driven by a high mix of sports cars at <span style="color:#2471A3">{:.0%}</span>.'\
                            .format(df_annotations.loc[df_annotations["Origin"] == "Europe", "Mean_Horsepower"].tolist()[0], \
                                    GRADIENT_EUROPE, \
                                    df_annotations.loc[df_annotations["Origin"] == "Europe", "Sports_Car_Prop"].tolist()[0])

TEXT_ASIA = 'On average Asian cars have the lowest power at <br><span style="color:#BA4A00">{:.0f}hp</span> and are the lightest at <span style="color:#BA4A00">{:,.0f}kgs</span>. However, <br>they have a high weight to horsepower ratio <br>where a 1 unit increase in hp will have a <span style="color:#BA4A00">{:.1f}kg</span> <br>rise in weight.'\
                            .format(df_annotations.loc[df_annotations["Origin"] == "Asia", "Mean_Horsepower"].tolist()[0], \
                                    df_annotations.loc[df_annotations["Origin"] == "Asia", "Mean_Weight"].tolist()[0], \
                                    GRADIENT_ASIA)

TEXT_USA = 'On average USA cars are the heaviest at <span style="color:#884EA0">{:,.0f}kgs</span> and <br>have a high weight to horsepower ratio, where a 1 unit <br>increase in hp will have a <span style="color:#884EA0">{:.1f}kg</span> rise in weight. This is <br>driven by a high mix of SUVs and Trucks at <span style="color:#884EA0">{:.0%}</span>.'\
                            .format(df_annotations.loc[df_annotations["Origin"] == "USA", "Mean_Weight"].tolist()[0], \
                                    GRADIENT_USA, \
                                    df_annotations.loc[df_annotations["Origin"] == "USA", "SUV_Prop"].tolist()[0] + df_annotations.loc[df_annotations["Origin"] == "USA", "Truck_Prop"].tolist()[0])

df_annotations["Text"] = TEXT_EUROPE
df_annotations.loc[df_annotations["Origin"] == "Asia", "Text"] = TEXT_ASIA
df_annotations.loc[df_annotations["Origin"] == "USA", "Text"] = TEXT_USA

#create row and column variables so that each category's text can be displayed on the correct subplot
df_annotations["xref"] = "x1"
df_annotations["yref"] = "y1"
df_annotations.loc[df_annotations["Origin"] == "Asia", "xref"] = "x2"
df_annotations.loc[df_annotations["Origin"] == "Asia", "yref"] = "y2"
df_annotations.loc[df_annotations["Origin"] == "USA", "xref"] = "x3"
df_annotations.loc[df_annotations["Origin"] == "USA", "yref"] = "y3"

#create row and column variables so that each category's line of best fit can be displayed on the correct subplot
df["xref"] = "x1"
df["yref"] = "y1"
df.loc[df["Origin"] == "Asia", "xref"] = "x2"
df.loc[df["Origin"] == "Asia", "yref"] = "y2"
df.loc[df["Origin"] == "USA", "xref"] = "x3"
df.loc[df["Origin"] == "USA", "yref"] = "y3"

#create a dataframe of the subplot titles to be looped over with the add_annotation command
df_subplot_titles = pd.DataFrame({"Origin": ["Europe", "Asia", "USA"],
                                    "xref": ["x1", "x2", "x3"],
                                    "yref": ["y1", "y2", "y3"]})

fig = make_subplots(rows = 1, cols = 3,
                    shared_yaxes = True)

for area in df["Origin"].unique(): 
    df_plot = df.loc[df["Origin"] == area].copy()
    df_plot2 = df.loc[df["Origin"] != area].copy() # create a second df_plot so that the remaining data points from the sample can be displayed on each subplot 
    m,b = np.polyfit(df_plot["Horsepower"], df_plot["Weight"], 1) #create the gradient and intercept for line of best fit
    bestfit_y = (df_plot["Horsepower"] * m + b) #create the line of best fit
    
    fig.add_trace(go.Scatter(x = df_plot["Horsepower"], y = df_plot["Weight"],
                            mode = "markers",
                            marker = dict(color = df_plot["Color"].tolist()[0]),
                            name = df_plot["Origin"].tolist()[0],
                            customdata = np.dstack((df_plot["Make"], df_plot["Model"]))[0], #use customdata to include information in the hover label that isn't already included in the graph object
                            hovertemplate = 
                            "Car: %{customdata[0]}<br>" +
                            "Model: %{customdata[1]}<br>" +
                            "Weight: %{y}kgs<br>" +
                            "Horsepower: %{x}hp<extra></extra>"
                            ), row = df_plot["row"].tolist()[0], col = df_plot["col"].tolist()[0])

    #add a new trace to overlay the remaining data points
    fig.add_trace(go.Scatter(x = df_plot2["Horsepower"], y = df_plot2["Weight"],
                            marker = dict(color = "#909497"),
                            opacity = 0.3,
                            mode = "markers",
                            hoverinfo = "skip"), row = df_plot["row"].tolist()[0], col = df_plot["col"].tolist()[0])
    
    #add a new trace to show the line of best fit
    fig.add_trace(go.Scattergl(x = df_plot["Horsepower"], y = bestfit_y,
                            line = dict(color = df_plot["Color"].tolist()[0]),
                            hoverinfo = "skip"), 
                            row = df_plot["row"].tolist()[0], col = df_plot["col"].tolist()[0])


fig.update_layout(plot_bgcolor = "white",
                 font = dict(color = "#909497", size = 10),
                 showlegend = False)

fig.update_xaxes(linecolor = "white", range = [0, 510], tickvals = [0, 100, 200, 300, 400, 500]) 
fig.update_yaxes(tickformat = ",", linecolor = "white", range = [1000, 8500]) 


#x axis title
fig.add_annotation(text = "Horsepower (hp)",
                    xref = "paper",
                    yref = "paper",
                    x = 0.5,
                    y = -0.1,
                    showarrow = False,
                    font = dict(size = 12))

#y axis title
fig.add_annotation(text = "Weight (kgs)",
                    xref = "paper",
                    yref = "paper",
                    x = -0.08,
                    y = 0.5,
                    showarrow = False,
                    textangle = -90,
                    font = dict(size = 12))

#graph title annotation
fig.add_annotation(text = "Car Weight Against Horsepower by Origin",
                    xref = "paper",
                    yref = "paper",
                    x = -0.08,
                    y = 1.10,
                    showarrow = False,
                    xanchor = "left",
                    font = dict(color = "#404647", size = 16))

#sub-title annotation
for area in df_subplot_titles["Origin"].unique():
    df_sub = df_subplot_titles.loc[df_subplot_titles["Origin"] == area].copy()
    fig.add_annotation(text = df_sub["Origin"].tolist()[0],
                        xref = df_sub["xref"].tolist()[0],
                        yref = "paper",
                        x = 20,
                        y = 1.02,
                        showarrow = False,
                        xanchor = "left",
                        font = dict(size = 14, color = "#404647"))

#loop over each subplot to add in the commentary 
for area in df_annotations["Origin"].unique():
    df_text = df_annotations.loc[df_annotations["Origin"] == area].copy()
    fig.add_annotation(text = df_text["Text"].tolist()[0],
                        xref = df_text["xref"].tolist()[0],
                        yref = df_text["yref"].tolist()[0],
                        x = 20,
                        y = 8180,
                        showarrow = False,
                        font = dict(size = 10),
                        xanchor = "left",
                        align = "left",
                        yanchor = "top")

#create author of the graph
fig.add_annotation(text = "Author: Tom Price",
                    xref = "paper",
                    yref = "paper",
                    x = 1.005,
                    y = -0.145,
                    showarrow = False,
                    font = dict(size = 12),
                    align = "right",
                    xanchor = "right")

#create the data source of the graph
fig.add_annotation(text = "Data Source: kaggle.com",
                    xref = "paper",
                    yref = "paper",
                    x = -0.005,
                    y = -0.145,
                    showarrow = False,
                    font = dict(size = 12),
                    align = "left",
                    xanchor = "left")


fig.show()



