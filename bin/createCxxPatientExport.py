#!/usr/bin/env python2
import sys
import vcf2xml


def grep_time_stamp_and_panel(file_path):
    meta_info = dict()
    meta_info['time_stamp'] = '1970-01-01T11:59:59'
    meta_info['panel'] = 'unknown gene panel'
    with open(file_path, 'r') as fh:
        for line in fh:
            if line.startswith("#"):
                parsed_line = line[1:].split("=")
                if not parsed_line[1].rstrip():
                    continue
                meta_info[parsed_line[0]] = parsed_line[1].rstrip()
    return meta_info

variantsWhitelist = vcf2xml.loadVariantsWhitelistFile(sys.argv[2])
vcfData = vcf2xml.loadGeneVariantsFromFile(sys.argv[1])

filteredGeneList = vcf2xml.matchVariantsToQBiCPanel(vcfData, variantsWhitelist)

sampleID = sys.argv[3]

meta_info = grep_time_stamp_and_panel(sys.argv[1])


xmlOutputString = vcf2xml.createPatientExport(filteredGeneList,
                                              sampleID,
                                              meta_info['time_stamp'],
                                              meta_info['panel'])

# TODO: check if we need utf8 encoding here
print(u"{0}".format(xmlOutputString).encode('utf-8'))
