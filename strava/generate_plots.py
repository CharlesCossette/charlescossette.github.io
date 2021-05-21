import pandas as pd
import glob
import os
from datetime import datetime
import plotly.graph_objects as go


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

def gen_cumulative_distance(data):
   
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


if __name__ == "__main__":
    data = read_strava_data()
    print(data)
    gen_cumulative_distance(data)