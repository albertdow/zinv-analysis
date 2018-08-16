import uproot
import numpy as np
from numpy import pi
from numba import njit, boolean
from .CollectionCreator import Collection

from utils.Geometry import DeltaR2

class ObjectCrossCleaning(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def event(self, event):
        for collection_name in self.collections:
            collection = getattr(event, collection_name)

            selections = np.ones(collection.stops[-1], dtype=bool)
            for ref_collection_name in self.ref_collections:
                ref_collection = getattr(event, ref_collection_name)
                selections = selections & comp(collection, ref_collection)

            for cat in ["Veto", "Selection"]:
                new_collection_name = collection_name + cat
                old_selection = getattr(event, new_collection_name).selection
                new_selection = old_selection & selections
                getattr(event, new_collection_name).selection = new_selection

def comp(coll1, coll2):
    return comp_jit(coll1.eta.content, coll1.phi.content,
                    coll1.starts, coll1.stops,
                    coll2.eta.content, coll2.phi.content,
                    coll2.starts, coll2.stops)

@njit
def comp_jit(etas1_cont, phis1_cont, starts_1, stops_1,
             etas2_cont, phis2_cont, starts_2, stops_2):
    content = np.ones(stops_1[-1], dtype=boolean)
    for iev, (start_1, stop_1, start_2, stop_2) in enumerate(zip(starts_1,
                                                                 stops_1,
                                                                 starts_2,
                                                                 stops_2)):
        for idx1 in range(start_1, stop_1):
            for idx2 in range(start_2, stop_2):
                deta = etas1_cont[idx1] - etas2_cont[idx2]
                dphi = phis1_cont[idx1] - phis2_cont[idx2]

                if DeltaR2(deta, dphi) < 0.16:
                    content[idx1] = False
                    break
    return content
