import pandas as pd

# def get_break_time(time_series, frequency):
#     dt_all = pd.date_range(start=time_series.iloc[0], end=time_series.iloc[-1], freq = frequency)
#     dt_all_py = [d.to_pydatetime() for d in dt_all]
#     dt_obs_py = [d.to_pydatetime() for d in time_series]
#     return [d for d in dt_all_py if d not in dt_obs_py]