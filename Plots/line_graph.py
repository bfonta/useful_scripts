import bokeh                
from bokeh.plotting import figure, show
from bokeh.io import export_svg

x = [600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 3000]
y_etau = {180: [4.06, 5.38, 6.88, 8.23, 9.89, 12.26, 12.25, 13.9, 12.16, 15.33],
          200: [2.67, 4.47, 5.74, 7.32,  9.08,  11.53, 11.7,  13.6,  11.45, 15.21],
          220: [1.94, 3.47, 4.92, 6.32, 8.07, 10.69, 11.18, 13.1, 10.9, 15.21]}
y_mutau  = {180: [2.78, 3.22, 3.75, 4.08, 4.31, 4.53,  5.41,  4.9,  5.37,  9.11],
            200: [2.13, 2.74, 3.3,  3.81,  3.98,  4.48,  5.36,  4.75,  5.11,  9.11],
            220: [1.62, 2.22, 2.88, 3.57, 3.53,  4.30,  5.22, 4.55, 5.07, 8.72]}
y_tautau = {180: [6.39, 9.08, 11.84, 14.78, 19.94, 48.62, 59.1, 70.4, 74.39, 88.48],
            200: [4.37, 7.03, 9.93, 12.66, 17.49, 45.66, 56.85, 69.06, 73.31, 88.16],
            220: [2.98, 5.13, 7.54, 10.28, 15.26, 42.24, 54.28, 67.42, 72.27, 87.87]}

p = figure(title='MET Trigger inclusion (cuts at 180, 200 and 220 GeV)',
           plot_width=800, plot_height=400,
           x_axis_label='x', y_axis_label='y')

opt_points = dict(size=8)
opt_line = dict(width=1.5, line_dash='dashed')
alphas_cuts = {200: 1, 180: 0.5, 220: 0.5}

for k,v in alphas_cuts.items():
    p.circle(x, y_tautau[k], color='green', legend_label='tautau', fill_alpha=v, **opt_points)
    p.circle(x, y_etau[k], color='blue', legend_label='etau', fill_alpha=v, **opt_points)
    p.circle(x, y_mutau[k], color='red', legend_label='mutau', fill_alpha=v, **opt_points)
    if k == 200:
        p.line(x, y_tautau[k], color='green', line_alpha=v, **opt_line)
        p.line(x, y_etau[k], color='blue', line_alpha=v, **opt_line)
        p.line(x, y_mutau[k], color='red', line_alpha=v, **opt_line)
    

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
p.yaxis.axis_label = '(MET trigger with cut + Baseline) / Baseline [%]'

p.output_backend = 'svg'
export_svg(p, filename='line_graph.svg')
show(p)
