import numpy as np
import pandas as pd
import operator

from cachetools import cachedmethod
from cachetools.keys import hashkey
from functools import partial

from utils.NumbaFuncs import get_bin_indices, weight_numba

def evaluate_qcdewk_weight():
    @cachedmethod(operator.attrgetter('cache'), key=partial(hashkey, 'fevaluate_qcdewk_weight'))
    def fevaluate_qcdewk_weight(ev, evidx, nsig, source):
        central = ev.WeightQcdEwkNominal
        try:
            up = getattr(ev, 'WeightQcdEwk_{}Up'.format(source))
            down = getattr(ev, 'WeightQcdEwk_{}Down'.format(source))
        except AttributeError:
            up = 0.
            down = 0.
        return weight_numba(central, nsig, up, down)

    return lambda ev: fevaluate_qcdewk_weight(ev, ev.iblock, ev.nsig, ev.source)

class WeightQcdEwk(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def begin(self, event):
        if event.config.dataset.isdata:
            return

        event.WeightQcdEwk = evaluate_qcdewk_weight()

        self.variations = [""]\
                + [n+"Up" for n in self.nuisances]\
                + [n+"Down" for n in self.nuisances]

        self.parent = event.config.dataset.parent
        if self.parent not in self.input_paths:
            return

        input_dict = {}
        global_bin_min = None
        global_bin_max = None
        for param in self.params:
            path, key = self.input_paths[self.parent]
            bin_min, bin_max, correction, _, _ = read_input(path, key.format(param))

            if global_bin_min is None:
                global_bin_min = bin_min
            if global_bin_max is None:
                global_bin_max = bin_max

            assert np.all(global_bin_min == bin_min)
            assert np.all(global_bin_max == bin_max)

            input_dict[param] = correction

        input_df = pd.DataFrame(input_dict)
        input_df["bin_min"] = global_bin_min
        input_df["bin_max"] = global_bin_max
        input_df = input_df.set_index(["bin_min", "bin_max"])

        input_df["isz"] = self.parent in ["ZJetsToNuNu", "DYJetsToLL", "ZJetsToLL", "GStarJetsToLL"]
        input_df["isw"] = self.parent in ["WJetsToLNu"]

        # nominal
        columns = [""]
        for nuisance in self.nuisances:
            input_df[nuisance] = 0
        input_df[""] = input_df.eval(self.formula)

        # Up/down variations
        for nuisance in self.nuisances:
            input_df[nuisance] = 1
            input_df[nuisance+"Up"] = input_df.eval(self.formula)
            input_df[nuisance] = -1
            input_df[nuisance+"Down"] = input_df.eval(self.formula)
            input_df[nuisance] = 0
            columns.append(nuisance+"Up")
            columns.append(nuisance+"Down")
        input_df = input_df[columns]

        if self.overflow:
            ser = input_df.iloc[-1,:]
            ser.name = (ser.name[-1], np.inf)
            input_df = input_df.append(ser)
        if self.underflow:
            ser = input_df.iloc[0,:]
            ser.name = (-np.inf, ser.name[0])
            input_df = input_df.append(ser)
            input_df.iloc[-1,:] = 1
        self.input_df = input_df.sort_index()
        #self.input_df = input_df.reset_index()

    def event(self, event):
        if self.parent not in self.input_paths:
            weights = np.ones(event.size)
            event.WeightQcdEwkNominal = weights
            for variation in self.variations[1:]:
                setattr(
                    event,
                    "WeightQcdEwk_{}".format(variation),
                    np.zeros(event.size),
                )
        else:
            corrections = self.input_df.iloc[get_bin_indices(
                event.GenPartBoson_pt,
                self.input_df.index.get_level_values("bin_min").values,
                self.input_df.index.get_level_values("bin_max").values,
            )]
            event.WeightQcdEwkNominal = corrections[""].values
            for variation in self.variations[1:]:
                setattr(
                    event,
                    "WeightQcdEwk_{}".format(variation),
                    (corrections[variation]/corrections[""]).values - 1.
                )

def read_input(path, histname):
    with open(path, 'r') as f:
        lines = f.read().splitlines()

    start_idx = next(idx
                     for idx in range(len(lines))
                     if "# BEGIN HISTO1D {}".format(histname) in lines[idx])
    end_idx = next(idx
                   for idx in range(start_idx, len(lines))
                   if "# END HISTO1D" in lines[idx])

    data = np.array([map(float, l.split()) for l in lines[start_idx+2: end_idx]])

    bin_min, bin_max = data[:,0], data[:,1]
    correction = data[:,2]
    errdown, errup = data[:,3], data[:,4]

    return bin_min, bin_max, correction, errdown, errup
