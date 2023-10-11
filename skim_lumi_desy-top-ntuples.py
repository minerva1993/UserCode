import json
from ROOT import *
import os, sys, shutil
import numpy as np

rootDir = './input'
outDir = './output/'

list_to_process = os.listdir(rootDir)
json_path = '/nfs/dust/cms/user/venturaa/August2023/CMSSW_10_6_32/src/TopAnalysis/Configuration/analysis/common/test/scripts/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON_PU50cut.txt'
with open(json_path, 'r') as f:
    data = json.load(f)


for infile in list_to_process:

    if not infile.endswith('.root'): continue
    print ('processing... ' + infile)

    org_file = TFile.Open(os.path.join(rootDir, infile), 'Read')

    try: os.remove(os.path.join(outDir, infile))
    except: pass
    shutil.copyfile(os.path.join(rootDir, infile), os.path.join(outDir, infile))
    out_file = TFile.Open(os.path.join(outDir,infile), 'Update')
    out_file.cd('writeNTuple')
    gDirectory.Delete('NTuple;1')

    org_tree = org_file.Get('writeNTuple/NTuple')
    out_tree = TTree("NTuple","NTuple")
    nevt = org_tree.GetEntries()
    print("Processing " + str(nevt) + " events")

    for i in range(nevt):
        org_tree.GetEntry(i)
        run = org_tree.runNumber
        lumi = org_tree.lumiBlock

        if str(run) in data:
            all_lumi = []
            for lum in data[str(run)]:
                lumi_begin = lum[0]
                lumi_end = lum[1] + 1
                lumi_range = range(lumi_begin,lumi_end)
                all_lumi.extend(lumi_range)

            if lumi in all_lumi:
                out_tree.Fill()
        else: continue

    out_file.Write()
    out_file.Close()

    #out_tree = 
