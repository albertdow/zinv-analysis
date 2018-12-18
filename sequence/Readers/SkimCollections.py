from utils.Lambda import Lambda
from . import Collection

class SkimCollections(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def begin(self, event):
        self.isdata = event.config.dataset.isdata

        if not self.isdata:
            # Add variation jet collections
            variation_selection_dict = {}
            for variation in event.variations:
                variation_selection_dict.update({
                    (incoll, outcoll+variation):
                    selection.replace("pt", "pt{}".format(variation))
                    for (incoll, outcoll), selection in self.selection_dict.items()
                    if incoll in ["Jet"]
                })
            self.selection_dict.update(variation_selection_dict)

        self.selection_functions = {k: Lambda(v)
                                    for k, v in self.selection_dict.items()}

    def event(self, event):
        for (input_collection, output_collection), selection in self.selection_functions.items():
            setattr(event, output_collection,
                    Collection(output_collection, event, input_collection,
                               getattr(event, input_collection)(selection)))

    def end(self):
        self.selection_functions = {}
