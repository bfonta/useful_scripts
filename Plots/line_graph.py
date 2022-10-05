import bokeh                
from bokeh.plotting import figure, show

x = [600, 700, 800, 900, 1000, 1250, 1500, 1750, 2000, 3000]
y1 = [4.26, 7.026, 9.92, 12.60, 17.49, 45.66, 0.0, 69.53, 0.0, 0.0]

y_etau_220   = [1.94, 3.47, 4.92, 6.32, 8.07, 10.69, 11.18, 13.1, 10.9, 15.21]
y_mutau_220  = [1.62, 2.22, 2.88, 3.57, 3.53,  4.30,  5.22, 4.55, 5.07, 8.72]
y_tautau_220 = [2.98, 5.13, 7.54, 10.28, 15.26, 42.24, 54.28, 67.42, 72.27, 87.87]

y_etau_180   = [4.06, 5.38, 6.88, 8.23, 9.89, 12.26, 12.25, 13.9, 12.16, 15.33]
y_mutau_180  = [2.78, 3.22, 3.75, 4.08, 4.31, 4.53,  5.41,  4.9,  5.37,  9.11]
y_tautau_180 = [6.39, 9.08, 11.84, 14.78, 19.94, 48.62, 59.1, 70.4, 74.39, 88.48]

p = figure(title='MET Trigger inclusion',
           plot_width=800, plot_height=400,
           x_axis_label='x', y_axis_label='y')
p.line(x, y1, color="blue", line_width=2) #legend_label="Temp."
p.xaxis.axis_label = 'mHH [GeV]'
p.yaxis.axis_label = '(MET with cut + Baseline) / Baseline [%]'
show(p)
