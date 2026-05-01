from docling.datamodel.document import DoclingDocument
from dataclasses import dataclass


@dataclass
class Document:
    content: DoclingDocument
    doc_id: str
    source: str


@dataclass
class Chunk:
    content: str
    chunk_id: str
    doc_id: str
    source: str
