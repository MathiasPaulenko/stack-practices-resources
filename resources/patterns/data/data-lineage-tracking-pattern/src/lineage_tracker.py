"""Emit OpenLineage run events from Python pipelines.

Requires: pip install openlineage-python
Backend:  Marquez (docker-compose.yml in this folder)
"""
from openlineage.client import OpenLineageClient
from openlineage.client.event_v2 import (
    InputDataset, Job, OutputDataset, Run, RunEvent, RunState,
)
from openlineage.client.uuid import generate_new_uuid
from datetime import datetime, timezone

client = OpenLineageClient(url="http://marquez:5000")

# producer identifies this emitter; use a repo URL or service name
PRODUCER = "https://github.com/shop/data-pipelines/tree/main/lineage_tracker"


class LineageTracker:
    """Emits START/COMPLETE/FAIL run events for a named job."""

    def __init__(self, job_name, job_namespace="shop"):
        self.job = Job(namespace=job_namespace, name=job_name)
        self.run_id = str(generate_new_uuid())

    def _emit(self, state, inputs, outputs, run_facets=None, job_facets=None):
        run = Run(runId=self.run_id, facets=run_facets or {})
        job = Job(
            namespace=self.job.namespace,
            name=self.job.name,
            facets=job_facets or {},
        )
        event = RunEvent(
            eventType=state,
            eventTime=datetime.now(timezone.utc).isoformat(),
            run=run,
            job=job,
            producer=PRODUCER,
            inputs=[self._to_input_dataset(d) for d in inputs],
            outputs=[self._to_output_dataset(d) for d in outputs],
        )
        client.emit(event)

    def start(self, inputs, outputs, sql=None):
        job_facets = {"sql": {"query": sql}} if sql else {}
        self._emit(RunState.START, inputs, outputs, job_facets=job_facets)

    def complete(self, inputs, outputs):
        self._emit(RunState.COMPLETE, inputs, outputs)

    def fail(self, error_message):
        self._emit(
            RunState.FAIL, [], [],
            run_facets={"errorMessage": {"message": error_message}},
        )

    def _to_input_dataset(self, spec):
        return InputDataset(
            namespace=spec.get("namespace", "default"),
            name=spec["name"],
            facets=spec.get("facets", {})
        )

    def _to_output_dataset(self, spec):
        return OutputDataset(
            namespace=spec.get("namespace", "default"),
            name=spec["name"],
            facets=spec.get("facets", {}),
            outputFacets={}
        )
