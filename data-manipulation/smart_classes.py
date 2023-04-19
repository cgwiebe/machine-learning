import pandas as pd

class WatchedDataFrame(pd.DataFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _report_shape_change(self, initial_shape):
        updated_shape = self.shape
        perc_change = (str(round(((updated_shape[0] - initial_shape[0])/initial_shape[0])*100))+'%', str(round(((updated_shape[1] - initial_shape[1])/initial_shape[1])*100))+'%')
        if initial_shape != updated_shape:
            print(f"Dataframe shape changed by {perc_change}, from {initial_shape} to {updated_shape}")

    def __setitem__(self, key, value):
        initial_shape = self.shape
        super().__setitem__(key, value)
        self._report_shape_change(initial_shape)

    def __delitem__(self, key):
        initial_shape = self.shape
        super().__delitem__(key)
        self._report_shape_change(initial_shape)

    def drop(self, *args, **kwargs):
        initial_shape = self.shape
        result = super().drop(*args, **kwargs)
        self._report_shape_change(initial_shape)
        return result

    def insert(self, *args, **kwargs):
        initial_shape = self.shape
        super().insert(*args, **kwargs)
        self._report_shape_change(initial_shape)

    def merge(self, right, *args, **kwargs):
        initial_shape_left = self.shape
        initial_shape_right = right.shape
        result = super(WatchedDataFrame, self).merge(right, *args, **kwargs)
        merged_df = WatchedDataFrame(result)
        merged_df._report_shape_change(initial_shape_left)
        if isinstance(right, WatchedDataFrame):
            right._report_shape_change(initial_shape_right)
        return merged_df


    @staticmethod
    def concat(objs, *args, **kwargs):
        initial_shapes = [obj.shape for obj in objs]
        result = pd.concat(objs, *args, **kwargs)
        wdf_result = WatchedDataFrame(result)
        for idx, obj in enumerate(objs):
            if isinstance(obj, WatchedDataFrame):
                obj._report_shape_change(initial_shapes[idx])
        return wdf_result

"""
# Example usage
data1 = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}

data2 = {
    'A': [1, 4, 7],
    'D': [10, 11, 12],
    'E': [13, 14, 15]
}

df1 = WatchedDataFrame(data1)
df2 = WatchedDataFrame(data2)

# Merging dataframes using the instance method
merged_df = df1.merge(df2, on='A', how='outer')
print("Merged dataframe using the instance method:")
print(merged_df)
"""

import datetime

class EasyDateTime:
    def __init__(self, date_or_timestamp):
        if isinstance(date_or_timestamp, (int, float)):
            self.datetime_obj = datetime.datetime.fromtimestamp(date_or_timestamp)
        elif isinstance(date_or_timestamp, (str, datetime.date, datetime.datetime)):
            self.datetime_obj = self._parse_date(date_or_timestamp)
        else:
            raise ValueError("Unsupported input type. Please use int, float, str, datetime.date, or datetime.datetime.")

    @staticmethod
    def _parse_date(date_str_or_obj):
        if isinstance(date_str_or_obj, str):
            try:
                date_obj = datetime.datetime.fromisoformat(date_str_or_obj)
            except ValueError:
                try:
                    date_obj = datetime.datetime.strptime(date_str_or_obj, "%Y-%m-%d")
                except ValueError:
                    raise ValueError("Invalid date string format. Please use ISO format or 'YYYY-MM-DD'.")
        else:
            date_obj = date_str_or_obj

        return date_obj

    def to_date(self):
        return self.datetime_obj.date()

    def to_datetime(self):
        return self.datetime_obj

    def to_timestamp(self):
        return self.datetime_obj.timestamp()

    def __str__(self):
        return self.datetime_obj.isoformat()
    
"""
# Example usage
easy_dt = EasyDateTime("2023-03-27")
print(easy_dt.to_date())  # 2023-03-27
print(easy_dt.to_datetime())  # 2023-03-27 00:00:00
print(easy_dt.to_timestamp())  # 1672224000.0

easy_dt = EasyDateTime(1672224000)
print(easy_dt.to_date())  # 2023-03-27
print(easy_dt.to_datetime())  # 2023-03-27 00:00:00
print(easy_dt.to_timestamp())  # 1672224000.0
"""