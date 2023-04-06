import subprocess
from pathlib import Path

from latch import medium_task, workflow, small_task, map_task
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from typing import List

from wf.docs import wf_docs
from wf.types import Sample, MicFunPredInput


@small_task
def organize_inputs(
    samples: List[Sample], perc_ident: int, genecov: float
) -> List[MicFunPredInput]:
    return [
        MicFunPredInput(
            name=sample.name,
            otu_table=sample.otu_table,
            repset_seq=sample.repset_seq,
            perc_ident=perc_ident,
            genecov=genecov,
        )
        for sample in samples
    ]


@medium_task
def run_micfunpred(sample: MicFunPredInput) -> LatchDir:
    """Task to run a software"""

    sample_name = sample.name
    local_resultpath = Path(sample_name).resolve()
    results_path = "MicFunPred_results"

    _run_cmd = [
        "MicFunPred_run_pipeline.py",
        "--otu_table",
        sample.otu_table.local_path,
        "--repset_seq",
        sample.repset_seq.local_path,
        "--perc_ident",
        str(sample.perc_ident),
        "--genecov",
        str(sample.genecov),
        "--output",
        str(local_resultpath),
        "--threads",
        "32",
        "--contrib",
    ]

    subprocess.run(_run_cmd)

    return LatchDir(str(local_resultpath), f"latch:///{results_path}/")


@workflow(wf_docs)
def micfunpred(
    samples: List[Sample], perc_ident: int = 97, genecov: float = 0.5
) -> List[LatchDir]:
    """A conserved approach to predict functional profiles from 16S rRNA sequence data

    MicFunPred
    ------

    MicFunPred[^1] is a tool to predict functional profiles from 16S
    (Amplicon) data. It relies on ~32,000 genome sequences downloaded
    from Integrated Microbial Genome database (IMG) representing human,
    plants, mammals, aquatic and terrestrial ecosystem.

    It uses as input:
    - Abundance/BIOM table (tab separated)
    - OTUs/ASVs sequences (FASTA format)


    [^1]: Dattatray S. Mongad, Nikeeta S. Chavan, Nitin P. Narwade, Kunal Dixit,
    Yogesh S. Shouche, Dhiraj P. Dhotre, MicFunPred: A conserved approach to
    predict functional profiles from 16S rRNA gene sequence data, Genomics.
    https://doi.org/10.1016/j.ygeno.2021.08.016
    """
    micfunpred_inputs = organize_inputs(
        samples=samples, perc_ident=perc_ident, genecov=genecov
    )

    return map_task(run_micfunpred)(sample=micfunpred_inputs)


LaunchPlan(
    micfunpred,
    "Test Data",
    {
        "samples": [
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
    },
)
