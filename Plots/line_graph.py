import bokeh                
from bokeh.plotting import figure, show

x = [600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 3000]
y_etau   = [2.67, 4.47, 5.74, 7.32,  9.08,  11.53, 11.7,  13.6,  11.45, 15.21]
y_mutau  = [2.13, 2.74, 3.3,  3.81,  3.98,  4.48,  5.36,  4.75,  5.11,  9.11]
y_tautau = [4.37, 7.03, 9.93, 12.66, 17.49, 45.66, 56.85, 69.06, 73.31, 88.16]

p = figure(title='MET Trigger inclusion',
           plot_width=800, plot_height=400,
           x_axis_label='x', y_axis_label='y')

opt_points = dict(size=8)
opt_line = dict(width=1.5, line_dash='dashed')

p.circle(x, y_etau, color="blue", legend_label="etau", **opt_points)
p.circle(x, y_mutau, color="red", legend_label="mutau", **opt_points)
p.circle(x, y_tautau, color="green", legend_label="tautau", **opt_points)
p.line(x, y_etau, color="blue", legend_label="etau", **opt_line)
p.line(x, y_mutau, color="red", legend_label="mutau", **opt_line)
p.line(x, y_tautau, color="green", legend_label="tautau", **opt_line)

xticks = x[:]
p.xaxis[0].ticker = xticks
p.xgrid[0].ticker = xticks
p.xgrid.grid_line_alpha = 0.2
p.xgrid.grid_line_color = 'black'

yticks = [x for x in range(10,100,10)]
p.yaxis[0].ticker = yticks
p.ygrid[0].ticker = yticks
p.ygrid.grid_line_alpha = 0.2
p.ygrid.grid_line_color = 'black'

p.legend.location = 'top_left'
p.xaxis.axis_label = 'mHH [GeV]'
p.yaxis.axis_label = '(MET with 200 GeV cut + Baseline) / Baseline [%]'

show(p)
