from wf import micfunpred
from wf.types import Sample
from latch.types import LatchFile


micfunpred(
    samples=[
        Sample(
            name="Test_Sample",
            otu_table=LatchFile(
                "s3://latch-public/test-data/4318/micfunpred_test_counts.tsv"
            ),
            repset_seq=LatchFile(
                "s3://latch-public/test-data/4318/micfunpred_test.fasta"
            ),
        )
    ]
)
