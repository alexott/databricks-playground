import json
from datetime import datetime, timezone, date
from typing import Any
import os
import uuid

from click.core import batch
from pyspark.sql.streaming import StreamingQueryListener

from databricks.sdk import WorkspaceClient
from pyspark.sql.streaming.listener import QueryProgressEvent, QueryStartedEvent, \
    QueryTerminatedEvent, QueryIdleEvent


class AdditionalJsonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime) or isinstance(o, date):
            return o.isoformat()
        if isinstance(o, uuid.UUID):
            return o.hex

        return json.JSONEncoder.default(self, o)


class UcVolumeWriteListener(StreamingQueryListener):
    def __init__(self, uc_volume_dir: str, file_name_prefix: str, write_interval_sec: int = 60):
        """Initializes the UcVolumeWriteListener.
        This listener writes query events to a specified UC Volume directory in JSON format.

        Args:
            uc_volume_dir (str): Path to UC Volume directory to write to `/Volumes/<catalog>/<schema>/<voleume>/<directory>`
            The directory will be created if it does not exist.
            file_name_prefix (str): Prefix for the output file names.
            write_interval_sec (int, optional): Interval in seconds for writing to the volume. Defaults to 60.
        """
        super().__init__()
        self.uc_volume_dir = uc_volume_dir
        self.stream_name = file_name_prefix
        self.base_record: dict[str, Any] = {
            "rowsProcessed": 0,
            "duration": 0,
            "timestamp": None,
            "stream_name": self.stream_name,
        }
        # TODO: add handling of error situations when we can't write to the volume?
        os.makedirs(uc_volume_dir, exist_ok=True)
        self.last_update = datetime.now(timezone.utc)
        self.buffer = []
        self.write_interval_sec = write_interval_sec

    def _push_to_volume(self, data: dict, event, force_write: bool = False):
        # TODO: do buffering, and write to the volume in batches
        ts = datetime.now(timezone.utc)
        if "timestamp" not in data:
            data["timestamp"] = ts.isoformat()
        data["report_timestamp"] = ts.isoformat()
        data["runId"] = event.runId
        data["query_id"] = event.id
        data["stream_name"] = self.stream_name
        self.buffer.append(data)
        # maybe write the data...
        time_diff = (ts - self.last_update).total_seconds()
        if force_write or (time_diff >= self.write_interval_sec):
            path = os.path.join(self.uc_volume_dir, f"{ts.strftime('%Y-%m-%d-%H-%M-%S.%fZ')}.json")
            with open(path, "w") as f:
                for i in self.buffer:
                    t = json.dumps(i, cls=AdditionalJsonEncoder)
                    f.write(t+"\n")
            self.last_update = ts
            self.buffer = []

    def onQueryStarted(self, event: QueryStartedEvent):
        r = self.base_record.copy()
        r["status"] = "started"
        r["timestamp"] = event.timestamp
        r["query_name"] = event.name
        print("Query started", r)
        self._push_to_volume(r, event)

    def onQueryProgress(self, event: QueryProgressEvent):
        progress = event.progress
        r = self.base_record.copy()
        r["status"] = "running"
        r["rowsProcessed"] = progress.numInputRows
        r["durationMs"] = progress.batchDuration
        r["batchId"] = progress.batchId
        r["numInputRows"] = progress.numInputRows
        r["inputRowsPerSecond"] = progress.inputRowsPerSecond
        r["timestamp"] = progress.timestamp
        r["query_name"] = progress.name
        print("Query progressed", r)

        self._push_to_volume(r, progress)

    def onQueryIdle(self, event: QueryIdleEvent):
        r = self.base_record.copy()
        r["status"] = "idle"
        r["timestamp"] = event.timestamp
        print("Query idle", r)
        self._push_to_volume(r, event)

    def onQueryTerminated(self, event: QueryTerminatedEvent):
        r = self.base_record.copy()
        if event.exception:
            r["status"] = "failed"
            r["exception"] = event.exception
            print(
                f"Query terminated with exception: id={event.id}, exception={event.exception}"
            )
        else:
            r["status"] = "succeeded"

        print("Query termindated", r)
        self._push_to_volume(r, event, force_write=True)
