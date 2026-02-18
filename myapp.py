from dash import Dash, dcc, html, Input, Output
import plotly.express as px

df = px.data.gapminder()
countries = df["country"].drop_duplicates().sort_values()

app = Dash(__name__)
server = app.server

app.layout = html.Div([
    dcc.Dropdown(
        id="country-dropdown",
        options=[{"label": c, "value": c} for c in countries],
        value="Canada",
        clearable=False
    ),
    dcc.Graph(id="gdp-growth")
])

@app.callback(
    Output("gdp-growth", "figure"),
    Input("country-dropdown", "value")
)
def update_graph(country_name):
    filtered = df[df["country"] == country_name]
    fig = px.line(
        filtered,
        x="year",
        y="gdpPercap",
        title=f"GDP Per Capita Over Time: {country_name}"
    )
    return fig

if __name__ == "__main__":
    app.run(debug=True)
