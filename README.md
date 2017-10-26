# QBiC-workflow-nf-centraxx
This workflow implemented in [Nextflow](https://www.nextflow.io) processes incomping gzipped variant calling format files and prepares it for the final upload in the patient information system CentraxX.

## Workflow in a nutshell
Input data are variant calling format ([VCF](https://samtools.github.io/hts-specs/)) files, that are automatically extracted from an archive, if necessary. The VCF files are then send to a process that performs variant annotation with SnpEff, that will lead to additional information about the variant. These annotated variants will then be used as basis for extraction to a more simpler variant overview format, reducing the information to gene name and its amino acid exchange (if mutation is not silent). Variants that have been called, but that are synonymous are recorded and tagged as `VARIANTABSENT`. 

From this simplified information, the variants are compared with a gene whitelist, which contains information of variants of a predefined gene panel, and their abundance has been computed from all VCF files stored at QBiC at a given time point. The called variants are filtered for their presence in the whitelist and the XML for the import in the patient information system CentraxX is prepared.

Last but not least, the information about the detected variants gets pushed to CentraxX via its REST interface.

## Workflow graph
This graph gives a brief overview of the processes included in the workflow. It was generated with the `-with-dag` flag when calling the workflow via Nextflow ([DAG visualisation](https://www.nextflow.io/docs/latest/tracing.html#dag-visualisation)). `Channel.fromPath` is the entry point and reads files carrying a `*.vcf*`-tag from a given directory. This includes **gzipped** vcf files. 

![https://github.com/qbicsoftware/qbic-workflow-nf-centraxx/blob/master/centraxx_wf.svg](https://github.com/qbicsoftware/qbic-workflow-nf-centraxx/blob/master/centraxx_wf.svg)

## Step 1: unpackingVCF
_TODO: Add description here_

## Step 2: variantAnnotation
_TODO: Add description here_

## Step 3: extractVariantInfo
_TODO: Add description here_

## Step 4: createCentraxxXML
_TODO: Add description here_

## Step 5: pushXMLtoCentraxX
_TODO: Add description here_
