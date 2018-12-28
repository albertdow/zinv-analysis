import awkward
import numpy as np
from numba import njit, float32, int32
from utils.Geometry import RadToCart2D, CartToRad2D, BoundPhi, PartCoorToCart3D, CartToPartCoor3D
from .CollectionCreator import Collection

class EventSumsProducer(object):
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def event(self, event):
        # Create new collections
        event.METnoX = Collection("METnoX", event)
        event.DiMuon = Collection("DiMuon", event)
        event.DiElectron = Collection("DiElectron", event)
        event.MHT40 = Collection("MHT40", event)
        event.HMiss = Collection("HMiss", event)

        # DiMuon
        dimu_pt, dimu_phi = create_dilepton(event.MuonSelection)
        event.DiMuon_pt = dimu_pt
        event.DiMuon_phi = dimu_phi

        diele_pt, diele_phi = create_dilepton(event.ElectronSelection)
        event.DiElectron_pt = diele_pt
        event.DiElectron_phi = diele_phi

        self.isdata = event.config.dataset.isdata
        for variation in event.variations:
            # Create lead jet selection collection
            setattr(event, "NearestJetToMETnoX{}".format(variation),
                    Collection("NearestJetToMETnoX{}".format(variation), event))

            # MET
            met, mephi = create_metnox(
                event.MET, event.MuonSelection, event.ElectronSelection, variation,
            )
            setattr(event, "METnoX_pt{}".format(variation), met)
            setattr(event, "METnoX_phi{}".format(variation), mephi)

            # MET_dCaloMET
            met = getattr(event.MET, "pt{}".format(variation))
            cmet = event.CaloMET.pt
            metnox = getattr(event.METnoX, "pt{}".format(variation))
            setattr(event, "MET_dCaloMET{}".format(variation), np.abs(met-cmet)/metnox)

            # MET Resolution
            metnox_para, metnox_perp = create_metres(
                event.METnoX, event.DiMuon, variation,
            )
            setattr(event, "METnoX_diMuonParaProjPt{}".format(variation), metnox_para)
            setattr(event, "METnoX_diMuonPerpProjPt{}".format(variation), metnox_perp)
            setattr(event, "METnoX_diMuonParaProjPt_Minus_DiMuon_pt{}".format(variation), metnox_para-dimu_pt)
            setattr(event, "METnoX_diMuonPerpProjPt_Plus_DiMuon_pt{}".format(variation), metnox_perp+dimu_pt)
            setattr(event, "METnoX_diMuonParaProjPt_Div_DiMuon_pt{}".format(variation), metnox_para/dimu_pt)
            setattr(event, "METnoX_diMuonPerpProjPt_Plus_DiMuon_pt_Div_DiMuon_pt{}".format(variation), (metnox_perp+dimu_pt)/dimu_pt)

            metnox_para, metnox_perp = create_metres(
                event.METnoX, event.DiElectron, variation,
            )
            setattr(event, "METnoX_diElectronParaProjPt{}".format(variation), metnox_para)
            setattr(event, "METnoX_diElectronPerpProjPt{}".format(variation), metnox_perp)
            setattr(event, "METnoX_diElectronParaProjPt_Minus_DiElectron_pt{}".format(variation), metnox_para-diele_pt)
            setattr(event, "METnoX_diElectronPerpProjPt_Plus_DiElectron_pt{}".format(variation), metnox_perp+diele_pt)
            setattr(event, "METnoX_diElectronParaProjPt_Div_DiElectron_pt{}".format(variation), metnox_para/diele_pt)
            setattr(event, "METnoX_diElectronPerpProjPt_Plus_DiElectron_pt_Div_DiElectron_pt{}".format(variation), (metnox_perp+diele_pt)/diele_pt)

            # MHT
            jet_coll = getattr(event, "JetSelection{}".format(variation))
            ht, mht, mhphi = create_mht(jet_coll, variation)
            setattr(event, "HT40{}".format(variation), ht)
            setattr(event, "MHT40_pt{}".format(variation), mht)
            setattr(event, "MHT40_phi{}".format(variation), mhphi)

            hmiss_pt, hmiss_eta, hmiss_phi = create_hmiss(jet_coll, variation)
            setattr(event, "HMiss_pt{}".format(variation), hmiss_pt)
            setattr(event, "HMiss_eta{}".format(variation), hmiss_eta)
            setattr(event, "HMiss_phi{}".format(variation), hmiss_phi)

            # dPhi(J, METnoX)
            dphi_j_metnox = create_jDPhiMETnoX(event.Jet, event.METnoX, variation)
            setattr(event, "Jet_dPhiMETnoX{}".format(variation), dphi_j_metnox)
            setattr(
                event, "MinDPhiJ1234METnoX{}".format(variation),
                create_minDPhiJ1234METnoX(jet_coll, variation),
            )

            # Nearest(J, METnoX)
            ref_collection = "JetSelection{}".format(variation)
            nearest_jet_indices = create_nearest_jet_metnox_indices(
                getattr(event, ref_collection),
                variation,
            )
            out_collection = "NearestJetToMETnoX{}".format(variation)
            for attr in ["pt", "eta", "phi"]:
                attr_name = attr+variation
                if attr!="pt" and variation!="":
                    attr_name = attr

                ref_coll_content = getattr(getattr(event, ref_collection), attr_name).content
                out_coll_content = np.full(event.size, np.nan)
                out_coll_content[nearest_jet_indices>=0] = ref_coll_content[nearest_jet_indices[nearest_jet_indices>=0]]
                setattr(event, out_collection+"_"+attr_name, out_coll_content)

            # nbjet
            setattr(
                event, "nBJetSelectionMedium{}".format(variation),
                count_nbjet(
                    getattr(event, "JetSelection{}".format(variation)).btagCSVV2.content,
                    getattr(event, "JetSelection{}".format(variation)).starts,
                    getattr(event, "JetSelection{}".format(variation)).stops,
                    0.8484,
                ),
            )

@njit
def create_lead_object(collection, starts, stops, pos=0):
    nev = stops.shape[0]
    collection_1d = np.zeros(nev, dtype=float32)
    for iev, (start, stop) in enumerate(zip(starts, stops)):
        if start+pos >= stop:
            collection_1d[iev] = np.nan
        else:
            collection_1d[iev] = collection[start+pos]
    return collection_1d

@njit
def count_nbjet(jet_btags, starts, stops, threshold):
    nev = stops.shape[0]
    nbjets = np.zeros(nev, dtype=int32)
    for iev, (start, stop) in enumerate(zip(starts, stops)):
        for ij in range(start, stop):
            if jet_btags[ij] > threshold:
                nbjets[iev] += 1
    return nbjets

def create_minDPhiJ1234METnoX(jets, variation):
    return create_minDPhiJ1234METnoX_jit(
        getattr(jets, "dPhiMETnoX{}".format(variation)).content,
        jets.starts, jets.stops,
    )

@njit
def create_minDPhiJ1234METnoX_jit(jets_dphi, starts, stops):
    nev = stops.shape[0]
    mindphis = np.zeros(nev, dtype=float32)
    for iev, (start, stop) in enumerate(zip(starts, stops)):
        mindphi = 2*np.pi
        for ij in range(start, min(stop, start+4)):
            mindphi = min(mindphi, abs(jets_dphi[ij]))
        mindphis[iev] = mindphi
    return mindphis

def create_jDPhiMETnoX(jets, met, variation):
    return awkward.JaggedArray(
        jets.starts, jets.stops,
        create_jDPhiMETnoX_jit(
            getattr(met, "phi{}".format(variation)),
            jets.phi.content, jets.starts, jets.stops,
        ),
    )

@njit
def create_jDPhiMETnoX_jit(mephi, jetphi, starts, stops):
    jet_dphis = np.zeros(jetphi.shape[0], dtype=float32)
    for iev, (start, stop) in enumerate(zip(starts, stops)):
        for jet_index in range(start, stop):
            jet_dphis[jet_index] = BoundPhi(jetphi[jet_index] - mephi[iev])
    return jet_dphis

def create_nearest_jet_metnox_indices(jets, variation):
    return create_nearest_jet_metnox_indices_jit(
        getattr(jets, "dPhiMETnoX{}".format(variation)).content,
        jets.starts, jets.stops,
    )

@njit
def create_nearest_jet_metnox_indices_jit(jets_dphimet, starts, stops):
    nearest_jet_metnox_indices = -1*np.ones(starts.shape[0], dtype=int32)
    for iev, (start, stop) in enumerate(zip(starts, stops)):
        if start < stop:
            nearest_jet_metnox_indices[iev] = start+np.argmin(jets_dphimet[start:stop])
    return nearest_jet_metnox_indices

def create_mht(jets, variation):
    return create_mht_jit(
        getattr(jets, "pt{}".format(variation)).content,
        jets.phi.content, jets.starts, jets.stops,
    )

@njit
def create_mht_jit(jetpt, jetphi, starts, stops):
    nev = stops.shape[0]
    hts = np.zeros(nev, dtype=float32)
    mhts = np.zeros(nev, dtype=float32)
    mhphis = np.zeros(nev, dtype=float32)

    for iev, (start, stop) in enumerate(zip(starts, stops)):
        ht, mhx, mhy = 0., 0., 0.
        for jet_index in range(start, stop):
            if jetpt[jet_index] > 40.:
                ht += jetpt[jet_index]
                px, py = RadToCart2D(jetpt[jet_index], jetphi[jet_index])
                mhx -= px
                mhy -= py
        hts[iev] = ht
        mhts[iev], mhphis[iev] = CartToRad2D(mhx, mhy)

    return hts, mhts, mhphis

def create_hmiss(jets, variation):
    return create_hmiss_jit(
        getattr(jets, "pt{}".format(variation)).content,
        jets.eta.content, jets.phi.content,
        jets.starts, jets.stops,
    )

@njit
def create_hmiss_jit(jetpt, jeteta, jetphi, starts, stops):
    nev = stops.shape[0]
    hmiss_pts = np.zeros(nev, dtype=float32)
    hmiss_etas = np.zeros(nev, dtype=float32)
    hmiss_phis = np.zeros(nev, dtype=float32)

    for iev, (start, stop) in enumerate(zip(starts, stops)):
        hxmiss, hymiss, hzmiss = 0., 0., 0.
        for ij in range(start, stop):
            px, py, pz = PartCoorToCart3D(jetpt[ij], jeteta[ij], jetphi[ij])
            hxmiss -= px
            hymiss -= py
            hzmiss -= pz
        if hxmiss == hymiss == hzmiss == 0.:
            hmiss_pt, hmiss_eta, hmiss_phi = 0., 0., 0.,
        else:
            hmiss_pt, hmiss_eta, hmiss_phi = CartToPartCoor3D(hxmiss, hymiss, hzmiss)
        hmiss_pts[iev] = hmiss_pt
        hmiss_etas[iev] = hmiss_eta
        hmiss_phis[iev] = hmiss_phi
    return hmiss_pts, hmiss_etas, hmiss_phis

def create_dilepton(muons):
    return jit_create_dilepton(
        muons.pt.content, muons.phi.content,
        muons.pt.starts, muons.pt.stops,
    )
@njit
def jit_create_dilepton(muons_pt, muons_phi, muons_starts, muons_stops):
    nev = muons_starts.shape[0]
    dimupts = np.zeros(nev, dtype=float32)
    dimuphis = np.zeros(nev, dtype=float32)

    for iev, (start, stop) in enumerate(zip(muons_starts, muons_stops)):
        nmu = stop-start
        if nmu != 2:
            dimupt = np.nan
            dimuphi = np.nan
        else:
            mux1, muy1 = RadToCart2D(muons_pt[start], muons_phi[start])
            mux2, muy2 = RadToCart2D(muons_pt[start+1], muons_phi[start+1])
            dimupt, dimuphi = CartToRad2D(mux1+mux2, muy1+muy2)
        dimupts[iev] = dimupt
        dimuphis[iev] = dimuphi

    return dimupts, dimuphis

def create_metres(metnox, dimuon, variation):
    return create_metres_jit(
        getattr(metnox, "pt{}".format(variation)),
        getattr(metnox, "phi{}".format(variation)),
        dimuon.pt, dimuon.phi,
    )

@njit
def create_metres_jit(met, mephi, dimupt, dimuphi):
    dphi = BoundPhi(mephi-dimuphi)
    return met*np.cos(dphi), met*np.sin(dphi)

def create_metnox(met, muons, electrons, variation):
    return create_metnox_jit(getattr(met, "pt{}".format(variation)),
                             getattr(met, "phi{}".format(variation)),
                             muons.pt.content,
                             muons.phi.content,
                             muons.pt.starts,
                             muons.pt.stops,
                             electrons.pt.content,
                             electrons.phi.content,
                             electrons.pt.starts,
                             electrons.pt.stops)

@njit
def create_metnox_jit(met, mephi,
                      mupt, muphi, mustarts, mustops,
                      elpt, elphi, elstarts, elstops):
    nev = met.shape[0]
    mets_out = np.zeros(nev, dtype=float32)
    mephis_out = np.zeros(nev, dtype=float32)

    for iev, (musta, musto, elsta, elsto) in enumerate(zip(
        mustarts, mustops, elstarts, elstops
    )):
        mex, mey = RadToCart2D(met[iev], mephi[iev])
        for muidx in range(musta, musto):
            mux, muy = RadToCart2D(mupt[muidx], muphi[muidx])
            mex, mey = mex+mux, mey+muy
        for elidx in range(elsta, elsto):
            elx, ely = RadToCart2D(elpt[elidx], elphi[elidx])
            mex, mey = mex+elx, mey+ely
        mets_out[iev], mephis_out[iev] = CartToRad2D(mex, mey)

    return mets_out, mephis_out
