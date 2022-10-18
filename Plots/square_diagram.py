from bokeh.plotting import figure, output_file, show
from bokeh.models import Range1d, Label
#from bokeh.io import export_svg

tau = '\u03C4'
# output to static HTML file
output_file("square.html")

p = figure(width=400, height=400)
p.x_range = Range1d(0, 10)
p.y_range = Range1d(0, 10)
p.outline_line_color = None
p.xgrid.grid_line_color = None
p.ygrid.grid_line_color = None

# add a square renderer with a size, color, and alpha
polyg_opt = dict(alpha=0.3)
p.multi_polygons(xs=[[[[2.1, 9.9, 9.9, 2.1]]]],
                 ys=[[[[9.9, 9.9, 2.1, 2.1]]]], color='green', **polyg_opt)
p.multi_polygons(xs=[[[[0.1, 1.9, 1.9, 5.4, 5.4, 0.1]]]],
                 ys=[[[[5.4, 5.4, 1.9, 1.9, 0.1, 0.1]]]], color='blue', **polyg_opt)
p.multi_polygons(xs=[[[[0.1, 0.1, 1.9, 1.9], [5.6, 5.6, 9.9, 9.9]]]],
                 ys=[[[[5.6, 9.9, 9.9, 5.6], [0.1, 1.9, 1.9, 0.1]]]], color='red', **polyg_opt)

label_opt = dict(x_units='data', y_units='data', text_font_size='10pt', render_mode='canvas')

stats_ditau = {'ditau': Label(x=7., y=9.3, text=tau+tau+': XXXXX', text_color='green', **label_opt),
               'met':   Label(x=7., y=8.9, text='met: XXXXX', text_color='blue', **label_opt),
               'tau':   Label(x=7., y=8.5, text=tau+': XXXXX', text_color='red', **label_opt) }
for elem in stats_ditau.values():
    p.add_layout(elem)

stats_met = {'ditau': Label(x=2.5, y=1.2, text=tau+tau+': XXXXX', text_color='green', **label_opt),
             'met':   Label(x=2.5, y=0.8, text='met: XXXXX', text_color='blue', **label_opt),
             'tau':   Label(x=2.5, y=0.4, text=tau+': XXXXX', text_color='red', **label_opt) }
for elem in stats_met.values():
    p.add_layout(elem)

stats_tau = {'ditau': Label(x=7.0, y=1.2, text=tau+tau+': XXXXX', text_color='green', **label_opt),
             'met':   Label(x=7.0, y=0.8, text='met: XXXXX', text_color='blue', **label_opt),
             'tau':   Label(x=7.0, y=0.4, text=tau+': XXXXX', text_color='red', **label_opt) }
for elem in stats_tau.values():
    p.add_layout(elem)

line_opt = dict(color='black', line_dash='dashed', line_width=2)
p.line(x=[2.0, 2.0], y=[0.0, 10.0], **line_opt)
p.line(x=[0.0, 10.0], y=[2.0, 2.0], **line_opt)

p.xaxis.ticker = [2.0, 5.5]
p.xaxis.major_label_overrides = {2: '40', 5.5: '200'}
p.xaxis.axis_label = 'dau1_pT [GeV]'

p.yaxis.ticker = [2.0, 5.5]
p.yaxis.major_label_overrides = {2: '40', 5.5: '200'}
p.yaxis.axis_label = 'dau2_pT [GeV]'

p.output_backend = "svg"
show(p)
