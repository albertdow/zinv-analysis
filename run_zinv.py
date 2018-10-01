#!/usr/bin/env python
import os
import sys
import warnings
warnings.filterwarnings('ignore')

from atuproot.AtUproot import AtUproot
from atsge.build_parallel import build_parallel
from utils.grouped_run import grouped_run
from datasets.datasets import get_datasets
from sequence.config import build_sequence

import logging
logging.getLogger(__name__).setLevel(logging.INFO)
logging.getLogger("alphatwirl").setLevel(logging.INFO)
logging.getLogger("atsge.SGEJobSubmitter").setLevel(logging.INFO)

logging.getLogger(__name__).propagate = False
logging.getLogger("alphatwirl").propagate = False
logging.getLogger("atsge.SGEJobSubmitter").propagate = False
logging.getLogger("atuproot.AtUproot").propagate = False

import argparse
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset_cfg", type=str,
                        help="Dataset config to run over")
    parser.add_argument("sequence_cfg", type=str,
                        help="Config for how to process events")
    parser.add_argument("-o", "--outdir", default="output", type=str,
                        help="Where to save the results")
    parser.add_argument("--mode", default="multiprocessing", type=str,
                        help="Which mode to run in (multiprocessing, htcondor, "
                             "sge)")
    parser.add_argument("--ncores", default=0, type=int,
                        help="Number of cores to run on")
    parser.add_argument("--nblocks-per-dataset", default=-1, type=int,
                        help="Number of blocks per dataset")
    parser.add_argument("--nblocks-per-sample", default=-1, type=int,
                        help="Number of blocks per sample")
    parser.add_argument("--blocksize", default=1000000, type=int,
                        help="Number of events per block")
    parser.add_argument("--quiet", default=False, action='store_true',
                        help="Keep progress report quiet")
    parser.add_argument("--profile", default=False, action='store_true',
                        help="Profile the code")
    parser.add_argument("--sample", default=None, type=str,
                        help="Select some sample")
    parser.add_argument("--redraw", default=False, action='store_true',
                        help="Overrides most options. Runs over collectors "
                             "only to rerun the draw function on outdir")
    return parser.parse_args()

def generate_report(outdir):
    filepath = os.path.join(outdir, "report.txt")
    with open(filepath, 'w') as f:
        f.write("python "+" ".join(sys.argv)+"\n")

vmem_dict = {
    "MET_Run2016B_v2": 12,
    "MET_Run2016C_v1": 12,
    "SingleMuon_Run2016B_v2": 12,
    "SingleMuon_Run2016C_v1": 12,
    "SingleMuon_Run2016D_v1": 12,
    "SingleMuon_Run2016E_v1": 12,
    "SingleMuon_Run2016F_v1": 12,
    "SingleMuon_Run2016G_v1": 12,
    "SingleMuon_Run2016H_v2": 12,
    "SingleElectron_Run2016H_v2": 12,
    "TTJets_Inclusive": 16,
    "QCD_Pt-800To1000_ext1": 12,
    "QCD_Pt-1000To1400_ext1": 12,
    "QCD_Pt-1400To1800_ext1": 12,
    "QCD_Pt-1800To2400_ext1": 12,
    "WZTo2Q2Nu": 12,
    "ZGToNuNuG": 12,
    "ZGToLLG": 12,
    "WWTo2L2Nu": 12,
    "WZTo1L3Nu": 12,
    "ZJetsToNuNu_Pt-50To100": 12,
    "ZJetsToNuNu_Pt-250To400": 12,
    "ZJetsToNuNu_Pt-250To400_ext1": 12,
    "ZJetsToNuNu_Pt-250To400_ext2": 12,
    "ZJetsToNuNu_Pt-400To650": 12,
    "ZJetsToNuNu_Pt-400To650_ext1": 12,
    "ZJetsToNuNu_Pt-650ToInf": 12,
    "ZJetsToNuNu_Pt-650ToInf_ext1": 12,
    "DYJetsToLL_Pt-0To50": 12,
    "DYJetsToLL_Pt-50To100": 20,
    "DYJetsToLL_Pt-100To250": 12,
    "WJetsToLNu_Pt-0To50": 12,
    "WJetsToLNu_Pt-50To100": 16,
    "WJetsToLNu_Pt-100To250_ext2": 16,
    "WJetsToLNu_Pt-250To400": 12,
    "WJetsToLNu_Pt-250To400_ext1": 12,
    "WJetsToLNu_Pt-400To600": 12,
    "WJetsToLNu_Pt-400To600_ext1": 12,
    "WJetsToLNu_Pt-600ToInf": 12,
    "WJetsToLNu_Pt-600ToInf_ext1": 12,
    "G1Jet_Pt-100To250": 12,
    "G1Jet_Pt-100To250_ext1": 12,
    "G1Jet_Pt-250To400": 12,
    "G1Jet_Pt-250To400_ext1": 12,
    "G1Jet_Pt-400To650": 12,
    "G1Jet_Pt-400To650_ext1": 12,
    "G1Jet_Pt-650ToInf": 12,
    "G1Jet_Pt-650ToInf_ext1": 12,
    "SingleTop_s-channel_InclusiveDecays": 12,
    "EWKZToNuNu2Jets_ext2": 12,
}
def run(sequence, datasets, options):
    process = AtUproot(options.outdir,
        quiet = options.quiet,
        max_blocks_per_dataset = options.nblocks_per_dataset,
        max_blocks_per_process = options.nblocks_per_sample,
                       nevents_per_block = options.blocksize,
        profile = options.profile,
        profile_out_path = "profile.txt",
    )
    process.parallel = build_parallel(
        options.mode,
        quiet = options.quiet,
        processes = options.ncores,
        dispatcher_options = {
            "vmem_dict": vmem_dict,
            "walltime_dict": {},
        },
    )
    return process.run(datasets, sequence)

def redraw(sequence, datasets, options):
    return [
        collector.reload(options.outdir)
        for (reader, collector) in sequence
        if hasattr(collector, "reload")
    ]

def parallel_draw(jobs, options):
    if len(jobs)==0:
        return
    jobs = [job for subjobs in jobs for job in subjobs]
    jobs = [jobs[i:i+len(jobs)/100+1]
            for i in xrange(0, len(jobs), len(jobs)/100+1)]

    parallel = build_parallel(
        options.mode,
        quiet = options.quiet,
        processes = options.ncores,
        dispatcher_options = {},
    )
    parallel.begin()
    try:
        parallel.communicationChannel.put_multiple([{
            'task': grouped_run,
            'args': args,
            'kwargs': {},
        } for args in jobs])
        parallel.communicationChannel.receive()
    except KeyboardInterrupt:
        parallel.terminate()
    parallel.end()

if __name__ == "__main__":
    options = parse_args()
    if not os.path.exists(options.outdir):
        os.makedirs(options.outdir)
    generate_report(options.outdir)

    sequence = build_sequence(options.sequence_cfg, options.outdir)
    datasets = get_datasets(options.dataset_cfg)
    if options.sample is not None:
        datasets = [d for d in datasets
                    if d.name==options.sample or \
                       d.parent==options.sample]

    if options.redraw:
        jobs = redraw(sequence, datasets, options)
    else:
        jobs = run(sequence, datasets, options)
        jobs = [reduce(lambda x, y: x + y, [ssjobs
            for ssjobs in sjobs
            if not ssjobs is None
        ]) for sjobs in jobs]
    parallel_draw(jobs, options)
