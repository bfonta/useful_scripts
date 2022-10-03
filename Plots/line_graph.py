import bokeh                
from bokeh.plotting import figure, show

x = [600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 3000]
y1 = [4.26, 7.026, 9.92, 12.60, 17.49, 45.66, 0.0, 69.53, 0.0, 0.0]

p = figure(title='MET Trigger inclusion',
           plot_width=800, plot_height=400,
           x_axis_label='x', y_axis_label='y')
p.line(x, y1, color="blue", line_width=2) #legend_label="Temp."
p.xaxis.axis_label = 'mHH [GeV]'
p.yaxis.axis_label = '(MET with cut + Baseline) / Baseline [%]'
show(p)
