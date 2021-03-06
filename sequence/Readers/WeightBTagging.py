import numpy as np
import numba as nb
import pandas as pd
import awkward as awk
import operator

from cachetools import cachedmethod
from cachetools.keys import hashkey
from functools import partial

from utils.NumbaFuncs import weight_numba, get_bin_indices

dict_apply = np.vectorize(lambda d, x: d[x])

def btag_formula(x, df):
    @nb.njit
    def btag_formula_numba(x_, eqtype, xlow, xhigh, p0, p1, p2, p3, p4, p5, p6):
        xtest = np.minimum(np.maximum(x_, xlow), xhigh)
        sf = np.ones_like(xtest, dtype=np.float32)
        sf[eqtype==0] = (p0*((1+(p1*xtest))/(1+(p2*xtest))) + p3)[eqtype==0]
        sf[eqtype==1] = ((p0 + p1*xtest + p2*xtest**2 + p3*xtest**3)*(1 + (p4 + p5*xtest + p6*xtest**2)))[eqtype==1]
        sf[eqtype==2] = ((p0 + p1/(xtest**2) + p2*xtest)*(1 + (p4 + p5*xtest + p6*xtest**2)))[eqtype==2]
        return sf
    return btag_formula_numba(
        x, df["eqtype"].values, df["xlow"].values, df["xhigh"].values,
        df["p0"].values, df["p1"].values, df["p2"].values, df["p3"].values,
        df["p4"].values, df["p5"].values, df["p6"].values,
    )

def evaluate_btagsf(df, attrs, h2f):
    @cachedmethod(operator.attrgetter('cache'), key=partial(hashkey, 'fevaluate_btagsf'))
    def fevaluate_btagsf(ev, evidx, nsig, source, attrs_):
        jet_flavour = dict_apply(h2f, ev.Jet.hadronFlavour.content)

        # Create mask
        mask = np.ones((jet_flavour.shape[0], df.shape[0]), dtype=np.bool8)

        # Flavour mask
        event_attrs = [jet_flavour.astype(np.float32)]
        mins = [df["jetFlavor"].values.astype(np.float32)]
        maxs = [(df["jetFlavor"].values+1).astype(np.float32)]

        for jet_attr, df_attr in attrs_:
            obj_attr = getattr(ev.Jet, jet_attr)
            if callable(obj_attr):
                obj_attr = obj_attr(ev)
            event_attrs.append(obj_attr.content.astype(np.float32))
            mins.append(df[df_attr+"Min"].values.astype(np.float32))
            maxs.append(df[df_attr+"Max"].values.astype(np.float32))

        # Create indices from mask
        indices = get_bin_indices(event_attrs, mins, maxs, 3)
        idx_central = indices[:,0]
        idx_down = indices[:,1]
        idx_up = indices[:,2]

        jpt = ev.Jet.ptShift(ev)
        sf = btag_formula(jpt.content, df.iloc[idx_central])
        sf_up = btag_formula(jpt.content, df.iloc[idx_up])
        sf_down = btag_formula(jpt.content, df.iloc[idx_down])

        sf_up = (source=="btagSF")*(sf_up/sf-1.)
        sf_down = (source=="btagSF")*(sf_down/sf-1.)
        return awk.JaggedArray(
            jpt.starts, jpt.stops, weight_numba(sf, nsig, sf_up, sf_down),
        )

    def return_evaluate_btagsf(ev):
        source = ev.source if ev.source in ev.attribute_variation_sources+["btagSF"] else ''
        return fevaluate_btagsf(ev, ev.iblock, ev.nsig, source, tuple(attrs))

    return return_evaluate_btagsf

class WeightBTagging(object):
    ops = {"loose": 0, "medium": 1, "tight": 2, "reshaping": 3}
    flavours = {"b": 0, "c": 1, "udsg": 2}
    hadron_to_flavour = {
        5: 0, -5: 0,
        4: 1, -4: 1,
        0: 2, 1: 2, 2: 2, 3: 2, -1: 2, -2: 2, -3: 2, 21: 2,
    }
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

        df = pd.read_csv(self.calibration_file, sep=',\s+')
        params = np.vstack(df["params"].apply(lambda x: eval(x[1:-1])))
        df["eqtype"] = params[:,0]
        df["xlow"] = params[:,1]
        df["xhigh"] = params[:,2]
        df["p0"] = params[:,3]
        df["p1"] = params[:,4]
        df["p2"] = params[:,5]
        df["p3"] = params[:,6]
        df["p4"] = params[:,7]
        df["p5"] = params[:,8]
        df["p6"] = params[:,9]

        op_num = self.ops[self.operating_point]
        df = df.loc[(df["CSVv2;OperatingPoint"] == op_num)]\
                .reset_index(drop=True)

        mask = np.zeros(df.shape[0], dtype=np.bool8)
        for flav, mtype in self.measurement_types.items():
            mask = mask | ((df["measurementType"]==mtype) & (df["jetFlavor"]==self.flavours[flav]))
        df = df.loc[mask]

        self.calibrations = df[[
            "sysType", "measurementType", "jetFlavor", "etaMin", "etaMax",
            "ptMin", "ptMax", "discrMin", "discrMax", "eqtype", "xlow", "xhigh",
            "p0", "p1", "p2", "p3", "p4", "p5", "p6",
        ]].sort_values(["sysType"]).reset_index(drop=True)

    def begin(self, event):
        attrs = [("eta", "eta"), ("ptShift", "pt")]
        if self.operating_point == "reshaping":
            attrs.append(("btagCSVV2", "discr"))

        setattr(event, "Jet_btagSF", evaluate_btagsf(
            self.calibrations, attrs, self.hadron_to_flavour,
        ))

    def end(self):
        self.calibrations = None
