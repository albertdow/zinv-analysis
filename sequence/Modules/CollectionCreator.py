import numpy as np
import uproot

class Collection(object):
    def __init__(self, name, event, ref_name=None, selection=None):
        self.name = name
        self.event = event
        self.ref_name = ref_name
        self.selection = selection

        self.branch_cache = {}

    def __getattr__(self, attr):
        if attr in ["name", "event"]:
            raise AttributeError("{} should be defined but isn't".format(attr))

        branch_name = self.name+"_"+attr
        if not self.event.hasbranch(branch_name):
            branch = self.create_branch(attr)
            setattr(self.event, branch_name, branch)
        return getattr(self.event, branch_name)

    def create_branch(self, attr):
        ref_branch = getattr(self.event, self.ref_name+"_"+attr)
        selection_jag = uproot.interp.jagged.JaggedArray(
            self.selection,
            ref_branch.starts,
            ref_branch.stops,
        )

        new_stops = np.cumsum(map(np.sum, selection_jag))
        new_starts = np.roll(new_stops, 1)
        new_starts[0] = 0

        return uproot.interp.jagged.JaggedArray(
            ref_branch.contents[self.selection],
            new_starts,
            new_stops,
        )

    def __call__(self, func):
        return self.apply_selection(func)

    def __repr__(self):
        return "{}({!r}, {!r}, {!r})".format(
            self.__class__.__name__,
            self.name,
            self.ref_name,
            self.selection,
        )

    def apply_selection(self, func):
        class CollectionWrapper(object):
            def __init__(self, collection):
                self.collection = collection

            def __getattr__(self, attr):
                result = getattr(self.collection, attr)
                return result.contents

        temp_collection = CollectionWrapper(self)
        return func(temp_collection)

class CollectionCreator(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def event(self, event):
        for collection in self.collections:
            setattr(event, collection, Collection(collection, event))

