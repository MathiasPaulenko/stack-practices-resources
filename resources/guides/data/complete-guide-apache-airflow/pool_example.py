# tests/test_dags.py — run in CI alongside unit tests
import pytest
from airflow.models import DagBag

def test_no_import_errors():
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    assert len(dag_bag.import_errors) == 0, f"DAG import failures: {dag_bag.import_errors}"

def test_catchup_disabled():
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    for dag in dag_bag.dags.values():
        assert dag.catchup is False, f"{dag.dag_id} has catchup enabled"

def test_dag_loaded():
    dag_bag = DagBag(dag_folder="dags/", include_examples=False)
    assert "simple_etl" in dag_bag.dags
