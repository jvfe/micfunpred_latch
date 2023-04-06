from latch.types.metadata import (
    Spoiler,
    LatchAuthor,
    LatchMetadata,
    LatchParameter,
    Params,
    Section,
    Text,
)

PARAMS = {
    "samples": LatchParameter(
        display_name="MicFunPred Input",
        samplesheet=True,
    ),
    "perc_ident": LatchParameter(
        display_name="Percent identity",
        description="Percent identity cut-off to assign genus",
    ),
    "genecov": LatchParameter(
        display_name="Gene Coverage",
        description=(
            "Percentage of organism in a genus "
            "to define it as core."
            " Value ranges from 0 to 1."
        ),
    ),
}

FLOW = [
    Section(
        "Samples",
        Text(
            "Sample provided has to include an identifier for the sample (Name)"
            " and two files corresponding to the tab-separated table of OTU abundances"
            " (OTU table) and a multi-FASTA file of OTU sequences (RepSet Seq)."
        ),
        Params("samples"),
    ),
    Spoiler(
        "Optional parameters",
        Text(
            "Optional parameters for MicFunPred."
            "See the [MicFunPred documentation](https://github.com/microDM/MicFunPred#running-micfunpred)"
            " for further details"
        ),
        Params("perc_ident", "genecov"),
    ),
]

WORKFLOW_NAME = "MicFunPred"

wf_docs = LatchMetadata(
    display_name=WORKFLOW_NAME,
    documentation=f"https://github.com/jvfe/{WORKFLOW_NAME}_latch/blob/main/README.md",
    author=LatchAuthor(
        name="jvfe",
        github="https://github.com/jvfe",
    ),
    repository=f"https://github.com/jvfe/{WORKFLOW_NAME}_latch",
    license="MIT",
    parameters=PARAMS,
    tags=["16S", "Amplicon", "Functional profiling"],
    flow=FLOW,
)
