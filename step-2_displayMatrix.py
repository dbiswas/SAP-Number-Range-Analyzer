import plotly.graph_objs as go
import numpy as np

import time
start_time = time.time()

x_axis_count = 100
y_axis_count = 100
matrix_file_name = 'matrix_data.txt'
label_matrix_file_name = 'matrix_label.txt'
system_in_scope = 'MSS'


data = np.genfromtxt(("./DATA/{}-{}").format(system_in_scope, matrix_file_name), dtype=str, encoding=None, delimiter=",")
harvest = data
vegetables = tuple(np.arange(1, (x_axis_count + 1), 1, dtype=int))
farmers = tuple(np.arange(1, (y_axis_count + 1), 1, dtype=int))
z_text = np.genfromtxt(("./DATA/{}-{}").format(system_in_scope, label_matrix_file_name), dtype=str, encoding=None, delimiter=",")

trace = go.Heatmap(
    x=vegetables,
    y=farmers,
    z=harvest,
    type='heatmap',
    xgap=0.5,
    ygap=0.5,
    colorscale='bupu'
    # colorscale='greys'
)
data = [trace]
fig = go.Figure(data=data)
fig.update_traces(text=z_text, texttemplate="%{text}")
fig.show()

print("--- %s seconds ---" % (time.time() - start_time))
