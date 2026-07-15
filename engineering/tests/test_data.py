import pandas as pd
import pytest
from engineering.argus_lab.data import assign_event_windows,normalize_month,validate_columns

def test_month_normalization_aligns_different_timestamps():
    values=pd.Series(["2020-01-01","2020-01-31"])
    assert normalize_month(values).nunique()==1

def test_event_windows_respect_information_order():
    frame=pd.DataFrame({"date":pd.to_datetime(["1999-01-01","2001-01-01","2003-01-01","2005-01-01"]),"SampleStartYear":[2000]*4,"SampleEndYear":[2002]*4,"Year":[2004]*4})
    assert list(assign_event_windows(frame))==["pre_sample","in_sample","post_sample","post_pub"]

def test_schema_failure_is_explicit():
    with pytest.raises(ValueError,match="missing columns"):validate_columns(pd.DataFrame({"a":[1]}),{"a","b"},"test")
