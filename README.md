# QBiC-workflow-nf-centraxx
This workflow implemented in [Nextflow](https://www.nextflow.io) processes incomping gzipped variant calling files and prepares it for the final upload in the patient information system CentraxX.

## Workflow graph
This graph gives a brief overview of the processes included in the workflow. It was generated with the `-with-dag` flag when calling the workflow via Nextflow ([DAG visualisation](https://www.nextflow.io/docs/latest/tracing.html#dag-visualisation)). `Channel.fromPath` is the entry point and reads files carrying a `*.vfc*`-tag from a given directory. This includes **gzipped** vcf files. 

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
