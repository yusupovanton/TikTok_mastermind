from handlers.dispatcher import *
from csgo import db_to_df

server = Flask(__name__)
app = dash.Dash(server=server)

df = db_to_df()

duplicates_series = df.pivot_table(columns=['name'], aggfunc='size')
duplicates_df = pd.DataFrame({'name': duplicates_series.index, 'count': duplicates_series.values})
duplicates_fig = px.bar(duplicates_df, x='name', y='count')

app.layout = html.Div([

    html.H4('Price of cs:go skins'),
    dcc.Graph(id="Graph"),
    dcc.Dropdown(id='Dropdown', options=[{'label': i, 'value': i} for i in df.name.unique()]),
    dcc.Graph(figure=duplicates_fig, id='Total Skins')
])


@app.callback(
    Output('Graph', 'figure'),
    Input('Dropdown', 'value'))
def update_output(selected_value):

    filtered_df = df[df['name'] == selected_value]
    fig = px.scatter(filtered_df[['float', 'price']], x="float", y="price")
    fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
