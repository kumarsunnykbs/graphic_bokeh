from bokeh.layouts import gridplot
from bokeh.models import BooleanFilter, CDSView, ColumnDataSource
from bokeh.plotting import figure, show

source = ColumnDataSource(data=dict(x=[1, 2, 3, 4, 5], y=[1, 2, 3, 4, 5]))
booleans = [True if y_val > 2 else False for y_val in source.data['y']]
view = CDSView(filter=BooleanFilter(booleans))

tools = ["box_select", "hover", "reset"]
p = figure(height=300, width=300, tools=tools)
p.circle(x="x", y="y", size=10, hover_color="red", source=source)

p_filtered = figure(height=300, width=300, tools=tools,
                    x_range=p.x_range, y_range=p.y_range)
p_filtered.circle(x="x", y="y", size=10, hover_color="red", source=source, view=view)

show(gridplot([[p, p_filtered]]))
