import plotly as py
import plotly.graph_objs as go


# bar plot
def barplot(l, s):
    trace0 = go.Scatter(
        x=l,
        y=s,
        mode='lines+markers')
    data = [trace0]
    div = py.offline.plot(data, output_type='div')
    return div

def compare_bar(x, y1, y2):
    trace1 = go.Bar(
        x=x,
        y=y1,
        name=y1.name
    )
    trace2 = go.Bar(
        x=x,
        y=y2,
        name=y2.name
    )
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='group'
    )

    fig = go.Figure(data=data, layout=layout)
    div = py.offline.plot(fig, output_type='div')

    return div


# Histogram
def histo(l):
    trace0 = go.Histogram(
        x=l,
    )
    data = [trace0]
    div = py.offline.plot(data, output_type='div')
    return div


def pie(l, s):
    labels = l
    values = s
    trace = go.Pie(labels=labels, values=values)

    div = py.offline.plot([trace], output_type='div')
    return div


def compare_pie(l, s, e):
    title = "Comparaison entre " + s.name + " et " + e.name
    fig = {
        "data": [
            {
                "values": s,
                "labels": l,
                "domain": {"x": [0, .48]},
                "name": s.name,
                "hoverinfo": "label+percent+name",
                "hole": .4,
                "type": "pie"
            },
            {
                "values": e,
                "labels": l,
                "text": e,
                "textposition": "inside",
                "domain": {"x": [.52, 1]},
                "name": e.name,
                "hoverinfo": "label+percent+name",
                "hole": .4,
                "type": "pie"
            }],
        "layout": {
            "title": title,
            "annotations": [
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": s.name,
                    "x": 0.20,
                    "y": 0.5
                },
                {
                    "font": {
                        "size": 12
                    },
                    "showarrow": False,
                    "text": e.name,
                    "x": 0.8,
                    "y": 0.5
                }
            ]
        }
    }
    div = py.offline.plot(fig, output_type='div')
    return div


# Horizontal Histogram
def hor_histo(l):
    trace0 = go.Histogram(
        y=l,
    )
    data = [trace0]
    py.offline.plot(data, output_type='div')




# Overlaid Histogram
def over_histo(l, s):
    trace1 = go.Histogram(
        x=l,
        opacity=0.65,
        name='Incidents 85_99')
    trace2 = go.Histogram(
        x=s,
        opacity=0.65,
        name='Incidents 00_14')
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='overlay')
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, output_type='div')


# Stacke Histogram
def stack_histo(l, s):
    trace1 = go.Histogram(
        x=l,
        opacity=0.65,
        name='Incidents 85_99')
    trace2 = go.Histogram(
        x=s,
        opacity=0.65,
        name='Incidents 00_14')
    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack')
    fig = go.Figure(data=data, layout=layout)
    py.offline.plot(fig, output_type='div')
