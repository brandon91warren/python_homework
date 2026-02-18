import pandas as pd
import plotly.express as px
import plotly.data as pldata

df = pldata.wind(return_type="pandas")

print(df.head(10))
print(df.tail(10))

df["strength"] = df["strength"].astype(str).str.replace(r"[^0-9.\-]", "", regex=True)
df["strength"] = pd.to_numeric(df["strength"], errors="coerce")

df = df.dropna(subset=["strength", "frequency", "direction"])

fig = px.scatter(
    df,
    x="strength",
    y="frequency",
    color="direction",
    title="Wind Strength vs Frequency by Direction"
)

fig.write_html("wind.html")
loaded_fig = px.scatter(df, x="strength", y="frequency", color="direction")
loaded_fig.write_html("wind.html", auto_open=True)
