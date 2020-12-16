import plotly.graph_objects as go
from IPython.display import Image
import plotly.io as pio
import base64


def ticks_thumbnail(ticks=None, start=None, end=None, width=120, height=30):
    df = ticks.raw_data.iloc[start:end]

    min = df['close'].min()
    max = df['close'].max()
    def _color_getter(x):
        if x == min:
            return "red"
        elif x == max:
            return "green"
        else:
            return "yellow"
    
    def _size_getter(x):
        if x == min or x == max:
            return 8
        else:
            return 0

    layout = go.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b': 0}, xaxis = dict(type="category"))
    fig = go.Figure(layout=layout, data=[
                    go.Scatter(x=df['time'],
                               y=df['close'],
                               mode='markers+lines',
                               marker = dict(size=list(map(_size_getter, df['close'])), color=list(map(_color_getter, df['close']))),
                               )
                    ]
                    )
    # remove missing timestamps from visualization
    # fig.update_xaxes(
    #     rangebreaks=[dict(values=dt_breaks)]  # hide timestamps with no values
    # )
    fig.update_layout(xaxis_visible=False, yaxis_visible=False)
    return Image(pio.to_image(fig, format='png', engine="kaleido", width=width, height=height))


def image_to_base64(i):
    return base64.b64encode(i)
