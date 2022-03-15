from handlers.dispatcher import *
from csgo import db_to_df

server = Flask(__name__)
app = dash.Dash(server=server)

df = db_to_df()

fig = px.line(df[['id', 'price']], x="id", y="price")


app.layout = html.Div([
    html.H4('Price of cs:go skins'),
    dcc.Graph(figure=fig)

])


if __name__ == '__main__':
    app.run_server(debug=True)
