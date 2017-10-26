#!/usr/bin/env nextflow
/*
vim: syntax=groovy
-*- mode: groovy;-*-
========================================================================================
               QBiC Centraxx pipeline   
========================================================================================
 Pipeline for annotating variants and registering them to the patient CentraXX system.
 Started in October 2017.
 #### Homepage / Documentation
 https://github.com/qbicsoftware/qbic-workflow-wf-centraxx
 #### Authors
 Sven Fillinger <sven.fillinger@qbic.uni-tuebingen.de>
----------------------------------------------------------------------------------------
*/

//Version of the pipeline

version=1.0

def helpMessage() {
    log.info"""
    =========================================
    QBiC Centraxx pipeline v${version}
    =========================================
    Usage:


	Mandatory parameters:
  		-folder <string>         Folder containing the input VCF files.
  		-name <string>           Base file name, typically the processed sample ID (e.g. 'GS120001_01').

	Optional parameters:
  		-out_folder <string>     Folder where analysis results should be stored. Default is same as in '-folder' (e.g. Sample_xyz/).
                           Default is: 'default'.

	Special parameters:
  		--log <file>             Enables logging to the specified file.
  		--email                  Sends you an e-mail on success/fail/etc (NOT YET IMPLEMENTED)
 """
}

//Help message if nothing else is specified

params.help = false

if(params.help){
	helpMessage()
	exit 0
}

params.folder = false
params.output = "./results"
params.prefix = "ann_"
params.whitelist = false


//Check NF version similar to NGI-RNAseq, thanks guys!

nf_required_version = '0.25.0'
try {
    if( ! nextflow.version.matches(">= $nf_required_version") ){
        throw GroovyException('Nextflow version too old')
    }
} catch (all) {
    log.error "====================================================\n" +
              "  Nextflow version $nf_required_version required! You are running v$workflow.nextflow.version.\n" +
              "  Pipeline execution will continue, but things may break.\n" +
              "  Please run `nextflow self-update` to update Nextflow.\n" +
              "============================================================"
}

//We're using the same defaults as in the original workflow specification here


//Validate inputs



//Header log info

log.info "========================================="
log.info " QBiC Centraxx pipeline: v${version}"
log.info "========================================="


def summary = [:]
summary['Folder']     = params.folder
summary['Output']     = params.output
summary['Whitelist']  = params.whitelist


if(params.email) summary['E-Mail address'] = params.email
log.info summary.collect { k,v -> "${k.padRight(15)}: $v" }.join("\n")
log.info "========================================="

if(!params.folder) {
  log.info "[ERROR] No input folder given."
  exit 1
}

if(!params.whitelist){
  log.error "No variant whitelist provided. Please check the required input parameters"
  exit 1
}

outputFolder = new File(params.output)
if(!outputFolder.exists()){
  outputFolder.mkdirs()
}


// Read in all putative compressed VCF files
packedVCF = Channel.fromPath(params.folder+"/*.vcf*")
// can be removed
//annVCF = Channel.fromPath(params.folder+"/ann_*.vcf")
//packedVCF = Channel.create()

process unpackingVCF {
  /*
  Some unpacking before we can run the annotation
  */
  publishDir params.output, mode: 'copy'

  input:
  file archive from packedVCF

  output:
  file "$trimmed_name" into readyVCF

  script:
  trimmed_name = archive.toString() - '.gz'
  
  if(trimmed_name != archive.toString()){
    """
    gunzip -c ${archive} > $trimmed_name
    """
  } else {
    """
    """
  }
}

process variantAnnotation {
  /* 
  Variant annotation with snpEff
  VCF files need to be extracted.
  */
  publishDir params.output, mode: 'copy'

  input:
  file vcf from readyVCF

  output:
  file "ann_${vcf}" into annVCFs

  script:
  """
  snpEff hg19 ${vcf} > ann_${vcf}
  """
}


process extractVariantInfo {

  publishDir params.output, mode: 'copy'

  input:
  file vcf from annVCFs

  output:
  file "${trimmed_name}_extracted_variants.txt" into extractedVariants

  script:
  trimmed_name = vcf.toString() - '.vcf'
  """
  extract_variants.py '${vcf}' > ${trimmed_name}_extracted_variants.txt
  """
}


process createCentraxxXML {
  
  publishDir params.output, mode: 'copy'

  input:
  file variants from extractedVariants

  output:
  file "${qbic_id}_toCentraXX.xml" into centraxXML

  script:
  base_name = variants.toString() - '.txt'
  qbic_id = (base_name =~ /Q[A-X0-9]{4}[0-9]{3}[A-X][A-X0-9]/)
  qbic_id = qbic_id[0]
  """
  python2.7 /home/sven1103/git/qbic-workflow-nextflow-centraxx/bin/createCxxPatientExport.py ${variants} ${params.whitelist} ${qbic_id} > ${qbic_id}_toCentraXX.xml
  """


}


process pushXMLtoCentraxX {

  input:
    file variants from centraxXML

  script:
  """
  echo 'Pushing XML to Centraxx...'
  """

}
