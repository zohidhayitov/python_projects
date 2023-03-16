# %%
import pandas as pd
df = pd.read_excel('meteostansiya.xlsx', usecols=['Kenglik (°N)', 'Uzunlik (°E)'])
list_view = df.values.tolist()
print(list_view)
# %%

# import folium.plugins as plugins
# import numpy as np

# np.random.seed(3141592)
# initial_data = np.random.normal(size=(100, 2)) * np.array([[1, 1]]) + np.array(
#     [[41.533, 64.600]]
# )

# move_data = np.random.normal(size=(100, 2)) * 0.01

# data = [(initial_data + move_data * i).tolist() for i in range(100)]

# time_ = 0
# N = len(data)
# itensify_factor = 30
# for time_entry in data:
#     time_ = time_+1
#     for row in time_entry:
#         weight = min(np.random.uniform()*(time_/(N))*itensify_factor, 1)
#         row.append(weight)

# hm = plugins.HeatMapWithTime(data)

# hm.add_to(mapObj)