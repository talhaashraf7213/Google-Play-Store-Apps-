import streamlit as st
import pandas as pd
import numpy as np

# Visualization Libraries
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import re
from datetime import datetime
st.set_page_config(layout="wide")
sns.set(font_scale=2)


df=pd.read_csv(r'.\data\Google-Playstore.csv')
# df=df[0:500]


st.title('Google Play Store Apps')

# df.head()
st.write(df.head())
st.write("Total number of Rows And columns ", df.shape)


# st.write(""" # DATA TRANSFORMATION """)

temp_size=[]
for x in df.Size:
    if  pd.isna(x):
        temp_size.append(np.nan)
    elif 'G' in x:
        temp_size.append(float(re.sub('G','',x))*1000)
    elif  'M' in x:
        temp_size.append(float(re.sub('M|,','',x)))
    elif 'K' in x or 'k' in x:
        temp_size.append(float(re.sub('K|k|,','',x))/1000.0)
    else:
        temp_size.append(0)
    
df.Size = temp_size

Released = []
for x in df.Released:
    if  pd.isna(x):
        Released.append(np.nan)
    else:
        Released.append(datetime.strptime(x, '%b %d, %Y'))
    
df.Released = Released

df["Last Updated"]=pd.to_datetime(df["Last Updated"])


st.write(""" # EDA """)

st.write(f"Number of apps that is not rated: {(df[df.Rating==0].shape[0]/df.shape[0])*100:.2f}%\n")


col1, col2 = st.columns(2)

with col1:
    fig = plt.figure(figsize=(20, 10))
    
    st.markdown("#### Rating with Boxplot Graph ")
    ax = sns.boxplot(data=df[df.Rating>0], x="Rating")
    st.pyplot(fig)
with col2:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Rating with Histogram Graph ")
    ax=sns.histplot(data=df[df.Rating > 0], x = "Rating",kde=True,binwidth=0.5)
    st.pyplot(fig)



col1, col2 = st.columns(2)

with col1:
    pie_data = df.Category.value_counts()
    graph_data = pie_data[:14]
    graph_data["Others"] = pie_data[15:].sum()
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### The first 15 Category App")
    ax = plt.pie(graph_data.values, labels=graph_data.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
with col2:
    paid_free_data = {
    "Paid": df.Price[df.Price > 0].count(),
    "Free": df.Price[df.Price == 0].count()
}
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Free & Paid App ")
    ax = plt.pie(paid_free_data.values(), labels=paid_free_data.keys(), autopct='%1.2f%%')
    st.pyplot(fig)


col1, col2 = st.columns(2)
with col1:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Prices of Paid App")
    ax = sns.histplot(data=df[df.Price > 0], x = "Price",kde=True,binwidth=5)
    st.pyplot(fig)
with col2:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Size of App")
    ax = sns.histplot(data=df,x="Size",kde=True,binwidth=20)
    st.pyplot(fig)


col1, col2, col3 = st.columns(3)

with col1:
    ad_supported=df["Ad Supported"].value_counts()
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### AD Supported App ")
    ax = plt.pie(ad_supported.values, labels=ad_supported.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
with col2:
    app_purchase = df["In App Purchases"].value_counts()
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Purchase Option in App")
    ax = plt.pie(app_purchase.values, labels=app_purchase.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
with col3:
    android_version = df["Minimum Android"].value_counts()
    graph_data = android_version[:9]
    graph_data["Others"] = android_version[10:].sum()
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Top 10 Minimum Android version ")
    ax = plt.pie(graph_data.values, labels=graph_data.keys(), autopct='%1.2f%%')
    st.pyplot(fig)


st.write("""Facebook's rating on Google Play Store dropped from 4.0 to 2.6 as a result of a boycott of the social media platform, which was sparked by Facebook's removal of posts that protested against Israeli military action against Palestinians.""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("#### Top 10 most expensive App ")
    sorted_df = df.sort_values(by=['Price'], ascending=False)
    sorted_df[["App Name","Category","Rating","Maximum Installs","Price"]][0:10]
with col2:
    st.markdown("#### Top 10 Maximum Installs App Table ")
    sorted_Install= df.sort_values(by=['Maximum Installs'], ascending=False)
    sorted_Install[["App Name","Category","Rating","Price","Maximum Installs"]][0:10]


col1, col2 = st.columns(2)
with col1:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### The most Rated top 10 Category")
    a = df.groupby(["Category"])["Rating"].count().sort_values(ascending=False)[:10]
    ax = sns.barplot(x=a.keys(), y=a.values)
    ax.tick_params(axis='x', labelrotation = 45)
    ax = plt.ylabel('Ratings (count)')
    st.pyplot(fig)
with col2:
    topTenDeveloperID= df["Developer Id"].value_counts()[0:10]
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Top 10 Developer")
    ax = sns.barplot(x=topTenDeveloperID.keys() , y=topTenDeveloperID.values)
    ax.tick_params(axis='x', labelrotation = 45)
    st.pyplot(fig)


topTenCategoriesNames=df["Category"].value_counts()[0:10].keys()
a = df[df.Category.isin(topTenCategoriesNames)]
a = a[a.Price>0]
fig = plt.figure(figsize=(50, 15))
st.markdown("#### Top 10 category with price")
ax = sns.boxplot(data=a, x="Category", y="Price")
ax.set_yscale('log',base=10)
ax.set_ylim(0.1,1000)
ax.set_ylabel('Price(log)')
ax.tick_params(axis='x', labelrotation = 45)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
st.pyplot(fig)


a = df[df.Category.isin(topTenCategoriesNames)]
a = a[a.Rating>0]
fig = plt.figure(figsize=(50, 15))
st.markdown("#### Top 10 category with Rating")
ax = sns.boxplot(data=a, x="Category", y="Rating")
ax.tick_params(axis='x', labelrotation = 45)
st.pyplot(fig)

a = df[df.Category.isin(topTenCategoriesNames)]
a = a[a.Size>=1]
fig = plt.figure(figsize=(50, 15))
st.markdown("#### Top 10 category with Size")
ax = sns.boxplot(data=a, x="Category", y="Size")
ax.set_yscale('log',base=10)
ax.set_ylabel('Size(MB)')
ax.set_ylim(0.1,1500.0)
ax.tick_params(axis='x', labelrotation = 45)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
st.pyplot(fig)


col1, col2 = st.columns(2)

with col1:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Price, Rating with Size")
    ax = sns.scatterplot( data=df, x="Price", y="Rating", size=df["Size"],)
    st.pyplot(fig)   
with col2:
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Price, Rating with Max-Installs")
    ax = sns.scatterplot( data=df, x="Price", y="Maximum Installs", size=df["Rating"],) 
    ax.set_yscale('log',base=10)
    st.pyplot(fig)
 

app = {
    "Abondened":(df[df["Last Updated"]<"2019"]).shape[0] ,
    "Non-Abondened":(df[df["Last Updated"]>="2019"]).shape[0] 
}


st.markdown("#### Abondened & Non-Abondened App before 2019")
col1, col2, col3  = st.columns([1,3,1])
with col2:
    fig = plt.figure(figsize=(70, 30), dpi=1200)
    ax = plt.pie(app.values(), labels=app.keys(), autopct='%1.2f%%')
    st.pyplot(fig)



col1, col2 = st.columns(2)
with col1:
    ratingFilteredDf = df[df.Rating > 0]
    app_Rating = {
    "Abondened":["Abondoned" if x else "Non-Abondoned" for x  in ratingFilteredDf["Last Updated"]<="2019"],
    "Abondened_Rating":ratingFilteredDf["Rating"]
    }
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Rating of Abondened & Non-Abondoned App ")
    ax = sns.boxplot(data=app_Rating, x="Abondened_Rating",  y="Abondened" )
    st.pyplot(fig)
   
with col2:
    PriceFilteredDf = df[df.Price>0]
    app_price = {
        "Abondened":["Abondoned" if x else "Non-Abondoned" for x  in PriceFilteredDf["Last Updated"]<="2019"],
        "Abondened_Price":PriceFilteredDf["Price"]
    }
    fig = plt.figure(figsize=(20, 10))
    st.markdown("#### Price of Abondened & Non-Abondoned App ")
    ax = sns.boxplot(data=app_price, x="Abondened_Price",  y="Abondened" )
    ax.set_xscale('log',base=10)
    st.pyplot(fig)



col1, col2, col3 = st.columns(3)

with col1:
    abondened = df[df["Last Updated"]<"2019"]
    abondened_paid_free = {
    "Paid": abondened.Price[abondened.Price > 0].count(),
    "Free": abondened.Price[abondened.Price == 0].count()
    }
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Free & Paid in Abondened App ")
    ax = plt.pie(abondened_paid_free.values(), labels=abondened_paid_free.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
   
with col2:
    abondened = df[df["Last Updated"]<"2019"]
    abondened_ad_supported = {
        "Yes": abondened["Ad Supported"][abondened["Ad Supported"] == True].count(),
        "No" : abondened["Ad Supported"][abondened["Ad Supported"] == False].count()  
    }
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Ad Supported in Abondened App ")
    ax = plt.pie(abondened_ad_supported.values(), labels=abondened_ad_supported.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
    
with col3:
    abondened = df[df["Last Updated"]<"2019"]
    abondened_editor_choice = {
     "Yes": abondened["Editors Choice"][abondened["Editors Choice"] == True].count(),
     "No" : abondened["Editors Choice"][abondened["Editors Choice"] == False].count()  
    }
    fig = plt.figure(figsize=(50, 15))
    st.markdown("#### Editors Choice in Abondened App ")
    ax = plt.pie(abondened_editor_choice.values(), labels=abondened_editor_choice.keys(), autopct='%1.2f%%')
    st.pyplot(fig)
    st.write(f"Only {abondened_editor_choice['Yes']} are Editor's choice out of {abondened_editor_choice['No']+abondened_editor_choice['Yes']} abondend apps.")


st.markdown("#### Editors Choice in Abondened App ")
Editors_Choice=abondened[abondened["Editors Choice"]]
Editors_Choice[["App Name","Category","Rating","Price","Last Updated"]][0:10]


