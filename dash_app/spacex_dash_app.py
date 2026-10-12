# Plotly Dash app: SpaceX launch records dashboard
# Run:  python spacex_dash_app.py   then open http://127.0.0.1:8050
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

URL = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(URL)
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

app = dash.Dash(__name__)

site_options = [{"label": "All Sites", "value": "ALL"}] + [
    {"label": s, "value": s} for s in spacex_df["Launch Site"].unique()
]

app.layout = html.Div(children=[
    html.H1("SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 40}),
    dcc.Dropdown(id="site-dropdown", options=site_options, value="ALL",
                 placeholder="Select a Launch Site here", searchable=True),
    html.Br(),
    html.Div(dcc.Graph(id="success-pie-chart")),
    html.Br(),
    html.P("Payload range (kg):"),
    dcc.RangeSlider(id="payload-slider", min=0, max=10000, step=1000,
                    marks={0: "0", 2500: "2500", 5000: "5000", 7500: "7500", 10000: "10000"},
                    value=[min_payload, max_payload]),
    html.Div(dcc.Graph(id="success-payload-scatter-chart")),
])


@app.callback(Output("success-pie-chart", "figure"), Input("site-dropdown", "value"))
def get_pie_chart(entered_site):
    if entered_site == "ALL":
        return px.pie(spacex_df, values="class", names="Launch Site",
                      title="Total Successful Launches by Site")
    site_df = spacex_df[spacex_df["Launch Site"] == entered_site]
    counts = site_df["class"].value_counts().reset_index()
    counts.columns = ["class", "count"]
    return px.pie(counts, values="count", names="class",
                  title="Total Launches for site " + entered_site)


@app.callback(Output("success-payload-scatter-chart", "figure"),
              [Input("site-dropdown", "value"), Input("payload-slider", "value")])
def get_scatter_chart(entered_site, payload_range):
    low, high = payload_range
    df = spacex_df[(spacex_df["Payload Mass (kg)"] >= low) & (spacex_df["Payload Mass (kg)"] <= high)]
    if entered_site != "ALL":
        df = df[df["Launch Site"] == entered_site]
    return px.scatter(df, x="Payload Mass (kg)", y="class", color="Booster Version Category",
                      title="Correlation between payload and success")


if __name__ == "__main__":
    app.run(debug=True)
