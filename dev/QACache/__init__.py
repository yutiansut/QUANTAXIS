"""
cache data 

"""
from pyarrow import parquet, plasma, RecordBatch, MockOutputStream, RecordBatchStreamWriter, RecordBatchStreamReader, FixedSizeBufferWriter, BufferReader
import numpy as np
import pyarrow.plasma as plasma
import pandas as pd


from QUANTAXIS.QAData import QADataStruct


class PlasmaStore():
    def __init__(self) -> None:
        self.client = plasma.connect("/tmp/plasma")

    def store_datastruct(self, data):
        return self.store_dataframe(data.data)

    def get_datastruct(self, object_id):
        return QADataStruct(self.get_dataframe(object_id))

    def store_dataframe(self, data):
        record_batch = RecordBatch.from_pandas(data)
        object_id = plasma.ObjectID(np.random.bytes(20))
        mock_sink = MockOutputStream()
        with RecordBatchStreamWriter(mock_sink, record_batch.schema) as stream_writer:
            stream_writer.write_batch(record_batch)
        data_size = mock_sink.size()
        buf = self.client.create(object_id, data_size)

        stream = FixedSizeBufferWriter(buf)
        with RecordBatchStreamWriter(stream, record_batch.schema) as stream_writer:
            stream_writer.write_batch(record_batch)
        self.client.seal(object_id)
        return object_id

    def get_dataframe(self, object_id) -> pd.DataFrame:
        # Get PlasmaBuffer from ObjectID
        [data] = self.client.get_buffers([object_id])
        buffer = BufferReader(data)
        reader = RecordBatchStreamReader(buffer)
        record_batch = reader.read_next_batch()
        return record_batch.to_pandas()
