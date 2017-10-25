#!/usr/bin/env python2

import sys
from collections import defaultdict


class DummyVCFRecord:
    def __init__(self, CHROM, POS, REF, ALT, INFO):
        self.CHROM = CHROM
        self.POS = POS
        self.REF = REF
        self.ALT = ALT.split(',')
        self.INFO = {}

        infoSplit = INFO.split(';')
        annString = [s for s in infoSplit if 'ANN=' in s]

        if len(annString) == 0:
            self.INFO['ANN'] = []
        else:
            annStringSplit = annString[0].strip().split(',')
            self.INFO['ANN'] = annStringSplit


def mangleSnpEffAnnotationString(annstring):
    """
    # Annotation      : T|missense_variant|MODERATE|CCT8L2|ENSG00000198445|transcript|ENST00000359963|protein_coding|1/1|c.1406G>A|p.Gly469Glu|1666/2034|1406/1674|469/557|  |
    # SubField number : 1|       2        |    3   |  4   |       5       |    6     |      7        |      8       | 9 |    10   |    11     |   12    |   13    |   14  |15| 16
    """
    annsplit = annstring.strip().split('|')
    annotateMap = defaultdict(str)
    annotateMap['allele'] = annsplit[0]
    annotateMap['effect'] = annsplit[1]
    annotateMap['putative_impact'] = annsplit[2]
    annotateMap['gene_name'] = annsplit[3]
    annotateMap['gene_id'] = annsplit[4]
    annotateMap['feature_type'] = annsplit[5]
    annotateMap['feature_id'] = annsplit[6]
    annotateMap['transcript_biotype'] = annsplit[7]
    annotateMap['rank_vs_total'] = annsplit[8]
    annotateMap['HGVS_c'] = annsplit[9]
    annotateMap['HGVS_p'] = annsplit[10]
    annotateMap['cDNApos_vs_cDNAlen'] = annsplit[11]
    annotateMap['CDSpos_vs_CDSlen'] = annsplit[12]
    annotateMap['proteinpos_vs_proteinlen'] = annsplit[13]
    annotateMap['distance_to_feature'] = annsplit[14]
    annotateMap['errors'] = annsplit[15]

    return annotateMap


def extractVCFdata(vcfFilename):
    """
    super-rudimentary vcf file reader... since pyvcf module does not work
    """
    vcfDict = {}
    vcfFile = open(vcfFilename, 'r')
    vcflines = vcfFile.readlines()

    for row in vcflines:
        if row.startswith('#'):
            continue

        rowsplit = row.strip().split('\t')
        chrom = rowsplit[0]
        position = rowsplit[1]
        refBase = rowsplit[3]
        altBase = rowsplit[4]
        info = rowsplit[7]

        record = DummyVCFRecord(chrom, position, refBase, altBase, info)

        dictKey = str(chrom) + ':' + str(position)

        vcfDict[dictKey] = record

    return vcfDict


def extractVCFGenes(vcfFilename):
    vcfFile = open(vcfFilename, 'r')
    vcflines = vcfFile.readlines()

    geneDict = defaultdict(int)
    for row in vcflines:
        if row.startswith('#'):
            continue

        rowsplit = row.strip().split('\t')
        chrom = rowsplit[0]
        position = rowsplit[1]
        refBase = rowsplit[3]
        altBase = rowsplit[4]
        info = rowsplit[7]

        record = DummyVCFRecord(chrom, position, refBase, altBase, info)

        firstAnn = record.INFO['ANN']

        if len(firstAnn) > 0:
            annDict = mangleSnpEffAnnotationString(firstAnn[0])
            geneDict[annDict['gene_name']] += 1

    return geneDict


def extractVariants(vcfFilename):
    vcfVarDict = extractVCFdata(vcfFilename)


    extractedVariants = []

    for position, vcfRecord in vcfVarDict.items():
        # refBase = vcfRecord.REF
        # altBase = vcfRecord.ALT
        annField = vcfRecord.INFO['ANN']

        blackList = []
        for ann in annField:
            annDict = mangleSnpEffAnnotationString(ann)

            # annAllele = annDict['allele']
            genename = annDict['gene_name'].strip()
            dnaChange = annDict['HGVS_c'].strip()
            aaChange = annDict['HGVS_p'].strip()
            combinedChange = '|'.join([genename, dnaChange, aaChange])
            print(combinedChange)

            if dnaChange != '' and aaChange != '' and combinedChange not in blackList:
                # print genename, dnaChange, aaChange
                extractedVariants.append((genename, dnaChange, aaChange))
                blackList.append(combinedChange)

    return(extractedVariants)


def main():
    """
    The scripts entry point
    """
    annVCFPath = sys.argv[1]
    significantVariants = extractVariants(annVCFPath)
    analyzedGenes = extractVCFGenes(annVCFPath)

    for variant in significantVariants:
        print(variant[0] + '\t' + variant[2] + '\n')

        if analyzedGenes.has_key(variant[0]):
            del analyzedGenes[variant[0]]

    # all remaining genes were analyzed but no variant was detected for them
    for gene in analyzedGenes.keys():
        print(gene + '\tVARIANTABSENT\n')


if __name__ == '__main__':
    try:
        main()
    except Exception:
        sys.exit(1)
    finally:
        sys.exit(0)

