import pandas as pd
import glob
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px



def read_strava_data():
    # Relative to this scripts location instead of executing directory
    dirname = os.path.dirname(__file__) 
    path = os.path.join(dirname, 'strava_data')
    all_files = glob.glob(path + "/*.csv")

    dateparse = lambda x: datetime.strptime(x, '%d/%m/%Y,  %H:%M:%S')

    # Read all files in strava_data folder
    li = []
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0, parse_dates=['Date'], date_parser=dateparse, thousands=',')
        li.append(df)

    data = pd.concat(li, axis=0, ignore_index=True)
    data.drop_duplicates(inplace=True)
    data["Distance"] = pd.to_numeric(data["Distance"], downcast="float")
    data = preprocess_chrome_extension(data)
    data.sort_values(by='Date', inplace=True, ascending=True)
    data.reset_index(drop=True, inplace=True)
    return data

def preprocess_chrome_extension(data):
    return data

def get_sum_by_sport(data):
    run_sum = 0
    ride_sum = 0
    swim_sum = 0
    for index, row in data.iterrows():
        if row['Type'] == 'run':
            run_sum += row['Distance']
        elif row['Type'] == 'ride':
            ride_sum += row['Distance']
        elif row['Type'] == 'swim':
            swim_sum += row['Distance']/1000
    return {'run':run_sum, 'ride':ride_sum, 'swim':swim_sum}

def add_cumulative_distance(data):
    # Compute sport-wise cumulative sum.
    # There was perhaps a better way to do this than manually
    run_sum = 0
    ride_sum = 0
    swim_sum = 0
    data['Run Total'] = ""
    data['Swim Total'] = ""
    data['Ride Total'] = ""
    for index, row in data.iterrows():
        if row['Type'] == 'run':
            run_sum += row['Distance']
        elif row['Type'] == 'ride':
            ride_sum += row['Distance']
        elif row['Type'] == 'swim':
            swim_sum += row['Distance']/1000
        
        data.loc[index,'Run Total'] = run_sum
        data.loc[index,'Swim Total'] = swim_sum
        data.loc[index,'Ride Total'] = ride_sum


def add_running_pb(data):
def plot_cumulative_distance(data):


    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Run Total'],
        hoverinfo='x+y',
        mode='lines',
        stackgroup='one', # define stack group
        name='run'
    ))
    fig.add_trace(go.Scatter(
        x=data['Date'], y=data['Ride Total'],
        hoverinfo='x+y',
        mode='lines',
        stackgroup='one',
        name='ride'
    ))

    fig.update_layout(
        title="Total Cumulative Distance",
        xaxis_title="Date",
        yaxis_title="Distance (km)",
        legend_title="Sport"
    )

    fig.write_json('cumulative_distance.json', pretty=True)


def gen_weekly_total_time(data):
    weeks = [g for n, g in data.groupby(pd.Grouper(key='Date',freq='W'))]
    for week in weeks:
        weekly_sum = get_sum_by_sport(week)
def plot_pb_evolution(data):
    data_run = data.loc[data['Type']=='run']

    fig = px.line(data_run, x="Date", y="Pace", color='Name')
    fig.show()

if __name__ == "__main__":
    data = read_strava_data()
    print(data)
    plot_cumulative_distance(data)
    plot_pb_evolution(data)