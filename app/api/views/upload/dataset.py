import csv
import json
from typing import Any, Dict, Iterator, List, Optional

import pyexcel


class Record:

    def __init__(self,
                 filename: str,
                 data: str = '',
                 label: Any = None,
                 metadata: Optional[Dict] = None):
        if metadata is None:
            metadata = {}
        self.filename = filename
        self.data = data
        self.label = label
        self.metadata = metadata


class Dataset:

    def __init__(self,
                 filenames: List[str],
                 column_data: str = 'text',
                 column_label: str = 'label',
                 **kwargs):
        self.filenames = filenames
        self.column_data = column_data
        self.column_label = column_label
        self.kwargs = kwargs

    def __iter__(self) -> Iterator[Record]:
        for filename in self.filenames:
            yield from self.load(filename)

    def load(self, filename: str) -> Iterator[Record]:
        """Loads a file content."""
        raise NotImplementedError()

    def from_row(self, filename: str, row: Dict) -> Record:
        data = row.pop(self.column_data)
        label = row.pop(self.column_label)
        record = Record(filename=filename, data=data, label=label, metadata=row)
        return record


class FileBaseDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        record = Record(filename=filename, data=filename)
        yield record


class TextFileDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            record = Record(filename=filename, data=f.read())
            yield record


class TextLineDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            for line in f:
                record = Record(filename=filename, data=line.rstrip())
                yield record


class CsvDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            delimiter = self.kwargs.get('delimiter', ',')
            reader = csv.reader(f, delimiter=delimiter)
            header = next(reader)
            for row in reader:
                row = dict(zip(header, row))
                yield self.from_row(filename, row)


class JSONDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            dataset = json.load(f)
            for row in dataset:
                yield self.from_row(filename, row)


class JSONLDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            for line in f:
                row = json.loads(line)
                yield self.from_row(filename, row)


class ExcelDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        records = pyexcel.iget_records(filename)
        for row in records:
            yield self.from_row(filename, row)


class FastTextDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            for i, line in enumerate(f, start=1):
                labels = []
                tokens = []
                for token in line.rstrip().split(' '):
                    if token.startswith('__label__'):
                        labels.append(token[len('__label__'):])
                    else:
                        tokens.append(token)
                data = ' '.join(tokens)
                record = Record(filename=filename, data=data, label=labels)
                yield record


class ConllDataset(Dataset):

    def load(self, filename: str) -> Iterator[Record]:
        with open(filename) as f:
            pass
