import subprocess
from pathlib import Path

from latch import medium_task, workflow
from latch.resources.launch_plan import LaunchPlan
from latch.types import LatchDir, LatchFile

from .docs import wf_docs
from .types import Sample


@medium_task
def run_software(sample: Sample) -> LatchDir:
    """Task to run a software"""

    sample_name = sample.name
    results_path = "program_results"
    output_dir = Path(results_path).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    output_prefix = f"{str(output_dir)}/{sample_name}"

    _run_cmd = [
        "software",
        "--in1",
        sample.read1.local_path,
        "--in2",
        sample.read2.local_path,
        "-o",
        output_prefix,
    ]

    subprocess.run(_run_cmd)

    return LatchDir(str(output_dir), f"latch:///{results_path}/{sample_name}")


@workflow(wf_docs)
def test_workflow(sample: Sample) -> LatchDir:
    """Workflow to do X

    Header
    ------

    This is a workflow that does X.

    """
    return run_software(sample=sample)


LaunchPlan(
    test_workflow,
    "Test Data",
    {
        "sample": Sample(
            name="SRR579292",
            read1=LatchFile("s3://latch-public/test-data/4318/SRR579292_1.fastq"),
            read2=LatchFile("s3://latch-public/test-data/4318/SRR579292_2.fastq"),
        )
    },
)
