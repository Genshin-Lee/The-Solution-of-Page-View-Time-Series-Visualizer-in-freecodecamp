import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv("fcc-forum-pageviews.csv",index_col = "date")

# Clean data
df = df.drop(df[(df["value"] < df["value"].quantile(0.025)) | (df["value"] > df["value"].quantile(0.975))].index)
print(df)
df.index = pd.to_datetime(df.index)

def draw_line_plot():
    # Draw line plot
    fig,ax = plt.subplots(figsize = (20,5))

    ax.plot(df.index,df.values,"r")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")

    ax.set_xticks(["2016-07-01","2017-01-01","2017-07-01","2018-01-01","2018-07-01","2019-01-01","2019-07-01","2020-01-01"])
    ax.set_xticklabels(["2016-07","2017-01","2017-07","2018-01","2018-07","2019-01","2019-07","2020-01"])

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar = df_bar.reset_index()
    df_bar["year"] = df_bar["date"].dt.year
    df_bar["month"] = df_bar["date"].dt.month
    df_bar = df_bar.groupby(["year","month"],as_index = False).mean()
    month_dict = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    df_bar["month"] = df_bar["month"].apply(lambda x:month_dict[x])

    # Draw bar plot
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    fig,ax = plt.subplots(1,1,figsize=(10,10))
    sns.barplot(x = "year", y = "value",hue = "month",data = df_bar,ax = ax,hue_order = month_order)
    ax.set_xlabel("Years")
    ax.set_ylabel("Average Page Views")
    ax.legend(title = "Months",loc = "upper left")

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]
    # Draw box plots (using Seaborn)
    fig,ax = plt.subplots(1,2,figsize=(16,6))

    sns.boxplot(x = "year", y = "value",data = df_box,ax=ax[0],linewidth = 1,fliersize = 1)
    ax[0].set_title("Year-wise Box Plot (Trend)")
    ax[0].set_xlabel("Year")
    ax[0].set_ylabel("Page Views")

    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    sns.boxplot(x = "month", y = "value",order = month_order,data = df_box,ax = ax[1],linewidth = 1,fliersize = 1)
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
