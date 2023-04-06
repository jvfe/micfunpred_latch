from dataclasses import dataclass

from dataclasses_json import dataclass_json
from latch.types import LatchFile


@dataclass
class Sample:
    name: str
    otu_table: LatchFile
    repset_seq: LatchFile


@dataclass_json
@dataclass
class MicFunPredInput:
    name: str
    otu_table: LatchFile
    repset_seq: LatchFile
    perc_ident: int
    genecov: float
