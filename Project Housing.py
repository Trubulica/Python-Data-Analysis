# Import matplotlib, pandas, and plotly
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

#Import data and take a look at it
df1 = pd.read_csv("data/brasil-real-estate-1.csv")
df1.head()

#Drop all rows with NaN values from df1
df1.dropna(inplace=True)

#Use the "lat-lon" column to create two separate columns in df1: "lat" and "lon"
df1[["lat", "lon"]] = df1["lat-lon"].str.split(",", expand=True).astype(float)


#Use the "place_with_parent_names" column to create a "state" column for df1
df1["state"] = df1["place_with_parent_names"].str.split("|", expand=True)[2]
df1["state"]

#Transform the "price_usd" column of df1 so that all values are floating-point numbers instead of strings
df1["price_usd"] =  df1["price_usd"].str.replace("$", "", regex = True).str.replace(",", "", regex = True).astype(float)

#Drop the "lat-lon" and "place_with_parent_names" columns from df1
df1.drop(columns=["lat-lon", "place_with_parent_names"], inplace=True)


#Import the CSV file brasil-real-estate-2.csv into the DataFrame df2
df2 = pd.read_csv("data/brasil-real-estate-2.csv")

#Use the "price_brl" column to create a new column named "price_usd". (when this data was collected 
#in 2015 and 2016, a US dollar cost 3.19 Brazilian reals.)
df2["price_usd"] = df2["price_brl"] / 3.19

#Drop the "price_brl" column from df2, as well as any rows that have NaN values
df2.drop(columns=["price_brl"], inplace=True)
df2.dropna(inplace=True)

#Concatenate df1 and df2 to create a new DataFrame
df = pd.concat([df1, df2])
print("df shape:", df.shape)

#Create a scatter_mapbox showing the location of the properties in df
fig = px.scatter_mapbox(
    df,
    lat="lat",
    lon="lon",
    center={"lat": -14.2, "lon": -51.9},  # Map will be centered on Brazil
    width=600,
    height=600,
    hover_data=["price_usd"],  # Display price when hovering mouse over house
)

fig.update_layout(mapbox_style="open-street-map")

fig.show()

#Create a DataFrame summary_stats with the summary statistics for the "area_m2" and "price_usd" columns
summary_stats = df[["area_m2", "price_usd"]].describe()
summary_stats

#Create a histogram of "price_usd"
plt.hist(df["price_usd"]);
plt.xlabel("Price [USD]");
plt.ylabel("Frequency");
plt.title("Distribution of Home Prices");

plt.savefig("images/price_usd.png", dpi=150)

# Build a box plot of "area_m2" 
plt.boxplot(df["area_m2"]);
plt.xlabel("Area [sq meters]");
plt.title("Distribution of Home Sizes");

plt.savefig("images/size.png", dpi=150)

#Create a Series that shows the mean home price in each region in Brazil, sorted from smallest to largest
mean_price_by_region = df.groupby("region")["price_usd"].mean().sort_values(ascending = True)
mean_price_by_region

#Use mean_price_by_region to create a bar chart
mean_price_by_region.plot(
    kind="bar",
    xlabel="Region",
    ylabel="Mean Price [USD]",
    title="Mean House Price by Region"
);

plt.savefig("images/mean_price_by_region.png", dpi=150)

#Create a DataFrame that contains all the homes from df that are in the "South" region
df_south = df[df["region"] == "South"]

#Create a Series homes_by_state that contains the number of properties in each state in df_south
homes_by_state = df_south["state"].value_counts()
homes_by_state

#Create a scatter plot showing price vs. area for the state in df_south that has the largest number of properties
df_south_rgs = df[df["state"] == "Rio Grande do Sul"]

plt.scatter(x=df_south_rgs["area_m2"], y=df_south_rgs["price_usd"]);
plt.xlabel("Area [sq meters]");
plt.ylabel("Price [USD]");
plt.title("Rio Grande do Sul: Price vs. Area")

plt.savefig("images/price_vs_area.png", dpi=150)


#Create a dictionary south_states_corr, where the keys are the names of the three states in the "South" region of Brazil, 
#and their associated values are the correlation coefficient between "area_m2" and "price_usd" in that state.

x = df_south.groupby("state")["area_m2"].corr(df_south["price_usd"])
south_states_corr = x.to_dict()

south_states_corr

