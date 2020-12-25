import plotly.graph_objects as go
from IPython.display import Image
import plotly.io as pio
import base64
import pandas as pd

def ticks_thumbnail(ticks=None, start=None, end=None, width=120, height=30):
    df = ticks.raw_data.iloc[start:end]
    return line_thumbnail(df, x_axis='time', y_axis='close', width=width, height=height)
    # min = df['close'].min()
    # max = df['close'].max()
    # def _color_getter(x):
    #     if x == min:
    #         return "red"
    #     elif x == max:
    #         return "green"
    #     else:
    #         return "yellow"
    
    # def _size_getter(x):
    #     if x == min or x == max:
    #         return 8
    #     else:
    #         return 0

    # layout = go.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b': 0}, xaxis = dict(type="category"))
    # fig = go.Figure(layout=layout, data=[
    #                 go.Scatter(x=df['time'],
    #                            y=df['close'],
    #                            mode='markers+lines',
    #                            marker = dict(size=list(map(_size_getter, df['close'])), color=list(map(_color_getter, df['close']))),
    #                            )
    #                 ]
    #                 )
    # fig.update_layout(xaxis_visible=False, yaxis_visible=False)
    # return Image(pio.to_image(fig, format='png', engine="kaleido", width=width, height=height))

def line_thumbnail(data=None, x_axis=None, y_axis=None, width=120, height=30):
    min = data[y_axis].min()
    max = data[y_axis].max()
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
                    go.Scatter(x=data[x_axis],
                               y=data[y_axis],
                               mode='markers+lines',
                               marker = dict(size=list(map(_size_getter, data[y_axis])), color=list(map(_color_getter, data[y_axis]))),
                               )
                    ]
                    )
    fig.update_layout(xaxis_visible=False, yaxis_visible=False)
    return Image(pio.to_image(fig, format='png', engine="kaleido", width=width, height=height))


def fund_amount_thumbnail(fund=None, start=None, end=None, width=120, height=30):
    history = [d.to_dict() for d in fund.history]
    df = pd.DataFrame(history)
    df = df.iloc[start:end]
    df['amount_trend'] = df['amount'] - df['amount'].min()
    
    min = df['amount_trend'].min()
    max = df['amount_trend'].max()
    def _color_getter(x):
        if x == min:
            return "red"
        elif x == max:
            return "black"
        else:
            return "grey"
    layout = go.Layout(autosize=True, margin={'l': 0, 'r': 0, 't': 0, 'b': 0}, xaxis = dict(type="category"))
    fig = go.Figure(layout=layout, data=[
                    go.Bar(y=df['amount_trend'],
                          marker = dict(color=list(map(_color_getter, df['amount_trend']))))
                    ]
                    )
    fig.update_layout(xaxis_visible=False, yaxis_visible=False)
    return Image(pio.to_image(fig, format='png', engine="kaleido", width=width, height=height))

def image_to_base64(i):
    return base64.b64encode(i)
