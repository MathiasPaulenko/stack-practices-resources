"""test_dask_examples.py — Unit tests for Dask DataFrame examples.

Run: python -m pytest test_dask_examples.py -v
Requires: pip install dask[dataframe] pandas pytest
"""
import pandas as pd
import dask.dataframe as dd

from dask_dataframe import create_sample_dataframe, to_dask, lazy_groupby, lazy_filter
from delayed_tasks import load_data, clean, combine, build_pipeline


class TestDaskDataFrame:
    def test_create_sample_shape(self):
        df = create_sample_dataframe()
        assert df.shape == (1000, 4)

    def test_to_dask_partitions(self):
        pdf = create_sample_dataframe()
        ddf = to_dask(pdf, npartitions=4)
        assert ddf.npartitions == 4

    def test_lazy_groupby_computes(self):
        pdf = create_sample_dataframe()
        ddf = to_dask(pdf, npartitions=4)
        result = lazy_groupby(ddf).compute()
        assert len(result) == 50
        assert "amount" in result.columns

    def test_lazy_filter(self):
        pdf = create_sample_dataframe()
        ddf = to_dask(pdf, npartitions=4)
        result = lazy_filter(ddf, min_amount=500.0).compute()
        assert (result["amount"] > 500.0).all()

    def test_divisions_from_pandas(self):
        pdf = create_sample_dataframe()
        ddf = to_dask(pdf, npartitions=4)
        # from_pandas with a RangeIndex produces known divisions
        assert len(ddf.divisions) == ddf.npartitions + 1


class TestDelayedTasks:
    def test_load_data_shape(self):
        df = load_data(0).compute()
        assert df.shape == (100, 2)

    def test_clean_filters_positive(self):
        df = pd.DataFrame({"id": [1, 2], "value": [-1.0, 5.0]})
        result = clean(df).compute()
        assert len(result) == 1
        assert result["value"].iloc[0] == 5.0

    def test_combine_aggregates(self):
        dfs = [pd.DataFrame({"id": [1, 2], "value": [10.0, 20.0]}),
               pd.DataFrame({"id": [1, 2], "value": [5.0, 15.0]})]
        result = combine(dfs).compute()
        assert result[result["id"] == 1]["value"].iloc[0] == 15.0
        assert result[result["id"] == 2]["value"].iloc[0] == 35.0

    def test_build_pipeline(self):
        pipeline = build_pipeline([0, 100])
        result = pipeline.compute()
        assert "id" in result.columns
        assert "value" in result.columns
