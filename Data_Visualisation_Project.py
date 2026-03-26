import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st 
import seaborn as sns
import plotly.express as px

st.set_page_config(
    page_title= "Analysis of Uber and Lyft Data",
    layout="centered",
    initial_sidebar_state="expanded"
)

st.title("Comparative Analysis of Lyft to Uber")

@st.cache_data
def load_data():
    df1 = pd.read_parquet("ride_share_1.parquet", engine="pyarrow")
    df2 = pd.read_parquet("ride_share_2.parquet", engine="pyarrow")
    df = pd.concat([df1, df2], ignore_index=True)

    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df["humidity"] = pd.to_numeric(df["humidity"], errors="coerce")
    df["windSpeed"] = pd.to_numeric(df["windSpeed"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")
    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    
    df = df.dropna(subset=["price", "humidity", "windSpeed"])
    
    df = df[(df["price"] > 0) & (df["price"] < 200.00)]
    df = df[(df["humidity"] > 0) & (df["humidity"] < 1)]
    df = df[(df["windSpeed"] > 0) & (df["windSpeed"] < 15)]
    
    df = df.rename(columns={"longitude": "lon", "latitude": "lat"})
    
    return df
    
df = load_data()

st.sidebar.title("Navigation")

options = st.sidebar.radio("Pages", options=["Information Page","Uber and Lyft Pickup Locations","Uber and Lyft Price Comparison","Price to Ride Comparison", 
                                             "Interactive Scatter Plot","Heatmap for Correlation between Metrics", "Rides Per Time Period"])

def Main():
    st.header("Uber and Lyft Rides in Boston")
    st.write("This project aims to explore an competitve analysis between Uber and Lyft through data visualisation. In the United States of America, both these companies are conglomerates in the transportation industry.")
    st.write("__Data Source:__")
    st.write("https://www.kaggle.com/datasets/brllrb/uber-and-lyft-dataset-boston-ma")
    st.write("__Scenario:__")
    st.write("I am a data science consultant, hired by Lyft to do a competitive analysis using visual techniques, interpreting the results, and providing insights.")
    st.write("__Questions:__")
    st.write("__1.__ At which locations are the rides most popular?")
    st.write("__2.__ What is the difference between prices offered by Uber and Lyft?")
    st.write("__3.__ How much money is spent on Uber and Lyft rides?")
    st.write("__4.__ Which metric influences the price of rides the most?")

# Define a function def Main():, its needed to add the information page 
# Used the streamlit function, st.write(), to add strings to the page

def Locations():
    st.header("Latitude and Longtitude of Uber and Lyft Pickups")
    data = df[['lat','lon']]
    st.map(data)
    st.subheader("__Data Interpretation__")
    st.markdown("According to the diagram demand for ride-share vehicles were around the bay area, "
    "and in the city of Boston, MA. Therefore, to compete with Uber," \
    " Lyft should reduce the amount of vehicles near towns, such as, Braintree, and allocate their resources near the city. the financial district and china town ")
    st.markdown("This answers the first questions, in which, areas in the city, such as, the financial district, are pickup locations, rather than towns.")

# Define a function def Locations():, its needed to add the map diagram to its page
# I needed only the columns lon and lat form the dataset, so defined data = [["lat", "lon"]].
# Then just used the streamlit function, st.map, to map the longitude and latitude on the dashboard. 


def Price():
    st.header("Ride Dependency on Price")
    fig_2 = px.box(df, x="name", y = "price", color = "cab_type", labels = dict(x = "Car Selection", y = "Prices"))
    fig_2.update_layout(title = "Prices of different Car Models")
    st.plotly_chart(fig_2)
    st.subheader("__Data Interpretation__")
    st.markdown("This plot was essential in identifying Lyft's most expensive car models, and how much the price varied when compared to it Uber." \
    " For example, the most common model and most luxurious model for of both companies should be considered for analysis." \
    "The median cost to ride in a Lyft was 9 dollars and to ride in a UberX 10 dollar." \
    "Furthermore, the median for their basic models was skewed in the middle, which indicate fairness," \
    "even with distance and the surge multipliers influencing prices (Correlation Heatmap).")
    st.markdown("Comparing, their most luxurious products, Lyft Lux and Uber Black, the results remain similar to the common model in terms of price and skewness." \
    " Lastly, it must be said that on average Lyft's prices are a higher than Ubers, looking at the box and whisker and its outliers, which answers the second question of this report.")

# Define a function def Price():, its needed to add the box and whisker plot to its page
# I used plotly.express to create my box and whisker plot with the function .box(). 
# This uses the original data frame values (df), where x was the different car models and y was the price to take a ride in each model.
# I used labels = dict(), to give my x and y axes label names 
# Finally, the .plotly_chart function was called to plot the diagram. 

def Ride():
    st.header("Ride Dependency on Price")
    fig_2, ax = plt.subplots()
    sns.histplot(df["price"], bins=30, ax = ax, alpha = 0.3, kde = True, fill = True, color = "red")
    ax.set_xlabel("Price")
    ax.set_ylabel("Number of Rides")
    ax.set_title("Variation in Rides that depend on Prices")
    st.pyplot(fig_2)
    st.subheader("__Data Interpretation__")
    st.markdown("The Histogram was essential for the marketing department at Lyft to understand and evaluate cutomer trends. " \
    " According to the graph, most customers book a ride share for prices between 10 and 15 dollars." \
    " This results in can be interpreted as customer book read shares for short distances and quick trips. " \
    "This is logical because for longer distances, potential customers would book other means of transport, such as, rental cars, buses, trains, etc. This answers the third quesiton in which lower amounts of money is spent on ride share trips. ")

# Define a function def Ride():, its needed to add the histogram to its page
# I used the ppt used in class, both seaborn and matplotlib, to create this histogram.
# Used the function from seaborn, sns.histplot() to create the histogram
# This uses the original data frame values (df), and the column price for the x axis. 
# I wanted thirty different bar/bins to make the values stand out more, and made kde = True, to outline the histogram.
# However, both were the same colour of red, so, I decided to use alpha = 0.3, to make the bins more transparent. 
# Next, to plot I used st.pyplot() to plot the diagram. 

def Scat():
    x_axis_val = st.selectbox("Select X-Axis Value", options = df.columns)
    y_axis_val = st.selectbox("Select Y-Axis Value", options = df.columns)

    plot = px.scatter(df, x = x_axis_val, y = y_axis_val, opacity= 0.5)
    plot.update_xaxes(showgrid = False)
    plot.update_yaxes(showgrid = False)
    st.plotly_chart(plot)
    st.subheader("__Data Interpretation__")
    st.markdown("The interactive scatter plot results can show the predicted trends for vehicle travels that travel further distances and the price changes. " \
    " It can even show how temperature effects the pricing of rides, and when there are higher temperatures in Boston the rides get cheaper, because customers, do not want to leave their houses. " \
    "This is relevant information to all stakeholder's mentioned, as it effects the strategic decisions on pricing, promotion, and availability of Lyft vehicles.")

# Define a function def Scat():, its needed to add the Scatter plot to its page
# I used the youtube video: https://www.youtube.com/watch?v=3f-j-PZ5N8A, to create this scatter plot
# Used the function from streamlit, .selectbox() to give an option to choose from
# I wanted the user to choose from all the available columns from the dataset,so I made options = df.columns.
# I used plotly.express to create my scatter plot with the function .scatter(). 
# This uses the original data frame values (df), and the x and y axes, are equal to the defined x and y columns selected by the user.
# opacity = 0.5, was used to make the points on the plot more visable, since most data points were overlapping. 
# I used .update_xaxes, and .update_yaxes, to remove the gridlines, and make the diagram more visable.
# Finally, the .plotly_chart function was called to plot the diagram. 


def Heat(): 
    st.header("Heatmap for Correlation between Metrics")
    data_3 = ["price","distance","surge_multiplier","temperature","humidity", "windSpeed"]
    correlation = df[data_3].corr() 
    fig_3 = px.imshow(correlation, labels = dict(x = "Metrics", y = "Metrics", color = "Correlation"), text_auto = True, color_continuous_scale="rdbu")
    fig_3.update_layout(title = "Correlation of Metrics")  
    st.plotly_chart(fig_3)
    st.subheader("__Data Interpretation__")
    st.markdown("An heatmap for correlation is important because it gives the correlation value between various metrics and uses colour to indicate its relationship. " \
    " Instead of analysis the correlation of each scatter plot, the heatmap directly give the values.")
    st.markdown("An example can be taken for distance and surge multiplier, in which, if distance of the journey is high the price of the ride will be multiplied by 2.6%. " \
    " So, all these difference metrics influence the final price of the ride provided by the application of Lyft and Uber.")
    st.markdown("This diagram, answers the fourth question, and indicates that distance and the surge multiplier would have the biggest impact on the price of rides.")

# Define a function def Heat():, its needed to add the Heatmap to its page
# use the function from streamlit, .header() to create a header for this page.
# Needed only the metrics, therefore, defined data_3 as all the columns I needed from the dataset.
# Then I only wanted to compared the correlation of the metrics to each other, so I used the .corr() function, and got the columns from the data frame. 
# I used plotly.express to create my heatmap diagram with the function .imshow(), I used this youtube video to help with its creation: https://www.youtube.com/watch?v=6S-4CCm9xm0
# This uses the new dataset, correlation, gives the x and y axes, its labels, and gives a legend according to the correlation (color = "Correlation")
# text_auto = True, was used to give each square on the heatmap a value, andc color_continuous_scale = "rdbu", was used to change the colour of the heatmap
# Finally, I used .update_layout, to give the graph a title, and .plotly_chart to plot the diagram. 

def Time():
    x_axis_val = st.selectbox("Select X-Axis Value", options = ["hour","day"])
    rides_per_time_period = df.groupby([x_axis_val, "cab_type"]).size().reset_index(name="rides") 
    plot = px.line(rides_per_time_period, x = x_axis_val, y = "rides", color="cab_type", markers=True)  
    plot.update_xaxes(showgrid = False)
    plot.update_yaxes(showgrid = False)
    st.plotly_chart(plot)
    st.subheader("__Data Interpretation__")
    st.markdown("When looking at the graph, it can be said that Uber is always more booked than Lyft at all times of the day. " \
    "Furthermore, both companies are booked more during the mid-night hours. This is probably influenced by the younger demographic who go to bars and clubs, and cannot drive after, therefore booking a ride share. ")

# Define a function def Time():, its needed to add the Line Graph to its page.
# create a box option, so that the user can change from hour to day. Defined x-axis value to streamlit function “.selectbox”, with options = “hour” and “day”.
# group my data using “.groupby()”, by the column selected. The .size() was used to count the rows for a specific time and company (Uber or Lyft).
# use reset.index() to convert it back to the Data Frame and gave the results the name “rides”. 
# used ploty express to create the line graph (px.line).
# rides_per_time_period would be the dataset (hour, cab_type, rides).
# x axis would be “hour” or “day”.
# y-axis would be the number of rides.
# graph more visually appealing color = cab_type, so that the rides for Uber are Lyft were different and easily recognisable.
# markers = True, so on the graph you can see the number of rides at a particular time. 
# showgrid = False, to remove the gridlines, and updated that to the plot.
 # streamlit function st.plotly_chart(plot) to plot the Line Graph.


if options == "Uber and Lyft Pickup Locations":
    Locations()
elif options == "Uber and Lyft Price Comparison":
    Price()
elif options == "Information Page":
    Main()
elif options == "Price to Ride Comparison":
    Ride()
elif options == "Interactive Scatter Plot":
    Scat()
elif options == "Heatmap for Correlation between Metrics":
    Heat()
elif options == "Rides Per Time Period":
    Time()

# used to else if loops to call the functions created above, and display them on their respective pages
# the pages names where given when I create the sidebar, and if options equal the title of the page call the function
