from collections import namedtuple
import os
from multiprocessing import Pool

from drawing.dist_ratio import dist_ratio
from utils.Histogramming import Histogram, Histograms

# Take the cfg module and drop unpicklables
Config = namedtuple("Config", "sample_names sample_colours axis_label")

class HistReader(object):
    split_samples = {
        "DYJetsToLL": {
            "DYJetsToEE": ["ev: ev.LeptonIsElectron"],
            "DYJetsToMuMu": ["ev: ev.LeptonIsMuon"],
            "DYJetsToTauTau": ["ev: ev.LeptonIsTau"],
        },
        "WJetsToLNu": {
            "WJetsToENu": ["ev: ev.LeptonIsElectron"],
            "WJetsToMuNu": ["ev: ev.LeptonIsMuon"],
            "WJetsToTauNu": ["ev: ev.LeptonIsTau"],
        },
    }
    def __init__(self, **kwargs):
        cfg = kwargs.pop("cfg")
        self.cfg = Config(
            sample_names = cfg.sample_names,
            sample_colours = cfg.sample_colours,
            axis_label = cfg.axis_label,
        )
        self.__dict__.update(kwargs)

        # convert cfg to histogram classes
        configs = []
        for cfg in cfg.histogrammer_cfgs:
            # expand categories
            for dataset, cutflow in cfg["categories"]:
                cutflow_restriction = "ev: ev.Cutflow_{}".format(cutflow)
                selection = [cutflow_restriction]
                weight = cfg["weight"].format(dataset=dataset)
                identifier = (dataset, cutflow, None, cfg["name"])

                configs.append({
                    "identifier": identifier,
                    "hist_config": {
                        "name": cfg["name"],
                        "variables": cfg["variables"],
                        "bins": cfg["bins"],
                        "weight": weight,
                        "selection": selection,
                    },
                })

        self.histograms = Histograms()
        self.histograms.extend([
            (config["identifier"], Histogram(**config["hist_config"]))
            for config in configs
        ])

    def begin(self, event):
        parent = event.config.dataset.parent
        self.parents = self.split_samples[parent].keys() \
                       if parent in self.split_samples \
                       else [parent]
        selection = self.split_samples[parent] \
                    if parent in self.split_samples \
                    else {}
        self.histograms.begin(event, self.parents, selection)

    def end(self):
        self.histograms.end()

    def event(self, event):
        self.histograms.event(event)

    def merge(self, other):
        self.histograms.merge(other.histograms)

class HistCollector(object):
    def __init__(self, **kwargs):
        # drop unpicklables
        cfg = kwargs.pop("cfg")
        self.cfg = Config(
            sample_names = cfg.sample_names,
            sample_colours = cfg.sample_colours,
            axis_label = cfg.axis_label,
        )
        self.__dict__.update(kwargs)

        self.outdir = os.path.join("output", self.name)
        if not os.path.exists(self.outdir):
            os.makedirs(self.outdir)

    def collect(self, dataset_readers_list):
        histograms = None
        for dataset, readers in dataset_readers_list:
            if histograms is None:
                histograms = readers[0].histograms
            else:
                histograms.merge(readers[0].histograms)
        histograms.save(self.outdir)
        if self.plot:
            self.draw(histograms)
        return dataset_readers_list

    def draw(self, histograms):
        datasets = list(set(n[0] for n, h in histograms.histograms))

        dataset_cutflow_histnames = set((n[0], n[1], n[3]) for n, h in histograms.histograms)
        dataset_cutflow_histnames = sorted(
            sorted(
                sorted(
                    dataset_cutflow_histnames,
                    key = lambda x: x[2],
                ),
                key = lambda x: x[1],
            ),
            key = lambda x: x[0],
        )

        args = []
        for dataset, cutflow, histname in dataset_cutflow_histnames:
            path = os.path.join(self.outdir, dataset, cutflow, "plots")
            if not os.path.exists(path):
                os.makedirs(path)

            hist_data = None
            hists_mc = []
            for n, h in histograms.histograms:
                if (n[0], n[1], n[3]) != (dataset, cutflow, histname):
                    continue

                if n[2] in datasets and dataset != n[2]:
                    continue

                if n[2] in ["MET", "SingleMuon", "SingleElectron"] and dataset != n[2]:
                    continue

                plot_item = {
                    "name": n[3],
                    "sample": n[2],
                    "bins": h.histogram["bins"],
                    "counts": h.histogram["counts"],
                    "yields": h.histogram["yields"],
                    "variance": h.histogram["variance"],
                }
                if n[2] == dataset:
                    hist_data = plot_item
                else:
                    hists_mc.append(plot_item)

            args.append([hist_data, hists_mc, os.path.join(path, histname), self.cfg])

        pool = Pool(processes=8)
        pool.map(dist_ratio, args)
        pool.close()
        pool.join()
        #for arg in args:
        #    dist_ratio(arg)

        return histograms

    def reload(self, outdir):
        histograms = Histograms()
        histograms.reload(os.path.join(outdir, self.name))
        self.draw(histograms)
        return histograms
