import numpy as np
from utils.Colours import colours_dict

inf = np.infty
pi = np.pi+0.00001

# dataset-cutflows split into regions
monojet_categories = [("MET", "Monojet"), ("MET", "MonojetSB"), ("MET", "MonojetSR"),
                      ("MET", "MonojetQCD"), ("MET", "MonojetQCDSB"), ("MET", "MonojetQCDSR")]

muon_categories = [("MET", "SingleMuon"), ("MET", "SingleMuonSB"), ("MET", "SingleMuonSR"),
                   ("SingleMuon", "SingleMuon"), ("SingleMuon", "SingleMuonSB"), ("SingleMuon", "SingleMuonSR")]
dimuon_categories = [("MET", "DoubleMuon"), ("MET", "DoubleMuonSB"), ("MET", "DoubleMuonSR"),
                     ("SingleMuon", "DoubleMuon"),("SingleMuon", "DoubleMuonSB"), ("SingleMuon", "DoubleMuonSR")]

ele_categories = [("SingleElectron", "SingleElectron"),
                  ("SingleElectron", "SingleElectronSB"),
                  ("SingleElectron", "SingleElectronSR")]
diele_categories = [("SingleElectron", "DoubleElectron"),
                    ("SingleElectron", "DoubleElectronSB"),
                    ("SingleElectron", "DoubleElectronSR")]

categories = monojet_categories + muon_categories + dimuon_categories \
        + ele_categories + diele_categories

histogrammer_cfgs = [
    {
        "name": "METnoX_pt",
        "categories": categories,
        "variables": ["ev: ev.METnoX_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "METnoX_phi",
        "categories": categories,
        "variables": ["ev: ev.METnoX_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "METnoX_diMuonParaProjPt_Minus_DiMuon_pt",
        "categories": dimuon_categories,
        "variables": ["ev: ev.METnoX_diMuonParaProjPt_Minus_DiMuon_pt"],
        "bins": [[-inf]+list(np.linspace(-250, 250., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "METnoX_diMuonPerpProjPt",
        "categories": dimuon_categories,
        "variables": ["ev: ev.METnoX_diMuonPerpProjPt"],
        "bins": [[-inf]+list(np.linspace(-250., 250., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "DiMuon_pt",
        "categories": dimuon_categories,
        "variables": ["ev: ev.DiMuon_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "DiMuon_phi",
        "categories": dimuon_categories,
        "variables": ["ev: ev.DiMuon_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "METnoX_diElectronParaProjPt_Minus_DiElectron_pt",
        "categories": diele_categories,
        "variables": ["ev: ev.METnoX_diElectronParaProjPt_Minus_DiElectron_pt"],
        "bins": [[-inf]+list(np.linspace(-250, 250., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "METnoX_diElectronPerpProjPt",
        "categories": diele_categories,
        "variables": ["ev: ev.METnoX_diElectronPerpProjPt"],
        "bins": [[-inf]+list(np.linspace(-250., 250., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "DiElectron_pt",
        "categories": diele_categories,
        "variables": ["ev: ev.DiElectron_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "DiElectron_phi",
        "categories": diele_categories,
        "variables": ["ev: ev.DiElectron_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MET_pt",
        "categories": categories,
        "variables": ["ev: ev.MET_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MET_phi",
        "categories": categories,
        "variables": ["ev: ev.MET_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "CaloMET_pt",
        "categories": categories,
        "variables": ["ev: ev.CaloMET_pt"],
        "bins": [[-inf]+list(np.linspace(0., 500., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "CaloMET_phi",
        "categories": categories,
        "variables": ["ev: ev.CaloMET_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "HT40",
        "categories": categories,
        "variables": ["ev: ev.HT40"],
        "bins": [[-inf]+list(np.linspace(0., 3000., 61))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MHT40_pt",
        "categories": categories,
        "variables": ["ev: ev.MHT40_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MHT40_phi",
        "categories": categories,
        "variables": ["ev: ev.MHT40_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MHT40_pt_div_METnoX_pt",
        "categories": categories,
        "variables": ["ev: ev.MHT40_pt / ev.METnoX_pt"],
        "bins": [[-inf]+list(np.linspace(0., 3., 61))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MinDPhiJ1234METnoX",
        "categories": categories + [(d, "{}_remove_dphi_jet_met_selection".format(c))
                                    for d, c in categories if "QCD" not in c],
        "variables": ["ev: ev.MinDPhiJ1234METnoX"],
        "bins": [[-inf]+list(np.linspace(0., pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MET_dCaloMET",
        "categories": categories,
        "variables": ["ev: ev.MET_dCaloMET"],
        "bins": [[-inf]+list(np.linspace(0., 1., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MTW",
        "categories": muon_categories + ele_categories\
                      + [(d, "{}_remove_mtw_selection".format(c))
                         for d, c in muon_categories+ele_categories if "SingleMuon" in c or "SingleElectron" in c],
        "variables": ["ev: ev.MTW"],
        "bins": [[-inf]+list(np.linspace(0., 200., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MLL",
        "categories": dimuon_categories + diele_categories,
        "variables": ["ev: ev.MLL"],
        "bins": [[-inf]+list(np.linspace(65., 115., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "MLL_wide",
        "categories": dimuon_categories + diele_categories\
                      + [(d, "{}_remove_mll_selection".format(c))
                         for d, c in dimuon_categories+diele_categories if "DoubleMuon" in c or "DoubleElectron" in c],
        "variables": ["ev: ev.MLL"],
        "bins": [[-inf]+list(np.linspace(0., 200., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nJetVeto",
        "categories": categories,
        "variables": ["ev: ev.JetVeto.size"],
        "bins": [[-inf]+list(np.linspace(0., 10., 11))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nJetSelection",
        "categories": categories,
        "variables": ["ev: ev.JetSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 10., 11))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_pt",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1200., 49))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_eta",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_phi",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_chEmEF",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_chEmEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_chHEF",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_chHEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_neEmEF",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_neEmEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadJetSelection_neHEF",
        "categories": categories,
        "variables": ["ev: ev.LeadJetSelection_neHEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondJetSelection_pt",
        "categories": categories,
        "variables": ["ev: ev.SecondJetSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1200., 49))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondJetSelection_eta",
        "categories": categories,
        "variables": ["ev: ev.SecondJetSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondJetSelection_phi",
        "categories": categories,
        "variables": ["ev: ev.SecondJetSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "DPhiJ1J2",
        "categories": categories,
        "variables": ["ev: ev.DPhiJ1J2"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nMuonVeto",
        "categories": categories,
        "variables": ["ev: ev.MuonVeto.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nMuonSelection",
        "categories": categories,
        "variables": ["ev: ev.MuonSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nElectronVeto",
        "categories": categories,
        "variables": ["ev: ev.ElectronVeto.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nElectronSelection",
        "categories": categories,
        "variables": ["ev: ev.ElectronSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nPhotonVeto",
        "categories": categories + [(d, "{}_remove_pho_veto".format(c))
                                    for d, c in categories],
        "variables": ["ev: ev.PhotonVeto.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nPhotonSelection",
        "categories": categories,
        "variables": ["ev: ev.PhotonSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nTauVeto",
        "categories": categories + [(d, "{}_remove_tau_veto".format(c))
                                    for d, c in categories],
        "variables": ["ev: ev.TauVeto.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nTauSelection",
        "categories": categories,
        "variables": ["ev: ev.TauSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nBJetSelectionMedium",
        "categories": categories + [(d, "{}_remove_nbjet_veto".format(c))
                                    for d, c in categories],
        "variables": ["ev: ev.nBJetSelectionMedium"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadMuonSelection_pt",
        "categories": muon_categories + dimuon_categories,
        "variables": ["ev: ev.LeadMuonSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadMuonSelection_eta",
        "categories": muon_categories + dimuon_categories,
        "variables": ["ev: ev.LeadMuonSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadMuonSelection_phi",
        "categories": muon_categories + dimuon_categories,
        "variables": ["ev: ev.LeadMuonSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondMuonSelection_pt",
        "categories": dimuon_categories,
        "variables": ["ev: ev.SecondMuonSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondMuonSelection_eta",
        "categories": dimuon_categories,
        "variables": ["ev: ev.SecondMuonSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondMuonSelection_phi",
        "categories": dimuon_categories,
        "variables": ["ev: ev.SecondMuonSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadElectronSelection_pt",
        "categories": ele_categories + diele_categories,
        "variables": ["ev: ev.LeadElectronSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadElectronSelection_eta",
        "categories": ele_categories + diele_categories,
        "variables": ["ev: ev.LeadElectronSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadElectronSelection_phi",
        "categories": ele_categories + diele_categories,
        "variables": ["ev: ev.LeadElectronSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondElectronSelection_pt",
        "categories": diele_categories,
        "variables": ["ev: ev.SecondElectronSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondElectronSelection_eta",
        "categories": diele_categories,
        "variables": ["ev: ev.SecondElectronSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondElectronSelection_phi",
        "categories": diele_categories,
        "variables": ["ev: ev.SecondElectronSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "PV_npvsGood",
        "categories": categories,
        "variables": ["ev: ev.PV_npvsGood"],
        "bins": [[-inf]+list(np.linspace(0., 100., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeptonDecay",
        "categories": categories,
        "variables": ["ev: ev.LeptonDecay"],
        "bins": [[-inf]+list(np.linspace(10., 20., 11))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "nGenBosons",
        "categories": categories,
        "variables": ["ev: ev.nGenBosons"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "GenPartBoson_pt",
        "categories": categories,
        "variables": ["ev: ev.GenPartBoson_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "GenPartBoson_eta",
        "categories": categories,
        "variables": ["ev: ev.GenPartBoson_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "GenPartBoson_phi",
        "categories": categories,
        "variables": ["ev: ev.GenPartBoson_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "GenPartBoson_mass",
        "categories": categories,
        "variables": ["ev: ev.GenPartBoson_mass"],
        "bins": [[-inf]+list(np.linspace(0., 500., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "GenPartBoson_p3",
        "categories": categories,
        "variables": ["ev: ev.GenPartBoson_pt*np.cosh(ev.GenPartBoson_eta)"],
        "bins": [[-inf]+list(np.linspace(0., 2000., 41))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadGenPartBosonDaughters_pt",
        "categories": categories,
        "variables": ["ev: ev.LeadGenPartBosonDaughters.pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadGenPartBosonDaughters_eta",
        "categories": categories,
        "variables": ["ev: ev.LeadGenPartBosonDaughters.eta"],
        "bins": [[-inf]+list(np.linspace(-5, 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadGenPartBosonDaughters_phi",
        "categories": categories,
        "variables": ["ev: ev.LeadGenPartBosonDaughters.phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "LeadGenPartBosonDaughters_p3",
        "categories": categories,
        "variables": ["ev: ev.LeadGenPartBosonDaughters.pt*np.cosh(ev.LeadGenPartBosonDaughters_eta)"],
        "bins": [[-inf]+list(np.linspace(0., 2000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondGenPartBosonDaughters_pt",
        "categories": categories,
        "variables": ["ev: ev.SecondGenPartBosonDaughters.pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondGenPartBosonDaughters_eta",
        "categories": categories,
        "variables": ["ev: ev.SecondGenPartBosonDaughters.eta"],
        "bins": [[-inf]+list(np.linspace(-5, 5., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondGenPartBosonDaughters_phi",
        "categories": categories,
        "variables": ["ev: ev.SecondGenPartBosonDaughters.phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "SecondGenPartBosonDaughters_p3",
        "categories": categories,
        "variables": ["ev: ev.SecondGenPartBosonDaughters.pt*np.cosh(ev.SecondGenPartBosonDaughters_eta)"],
        "bins": [[-inf]+list(np.linspace(0., 2000., 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    }, {
        "name": "Weight_MET",
        "categories": monojet_categories,
        "variables": ["ev: ev.Weight_MET"],
        "bins": [[-inf]+list(np.linspace(-50, 950, 51))+[inf]],
        "weights": [("nominal", "ev: ev.Weight_{dataset}")],
    },
]

sample_colours = {
    "MET":            "black",
    "SingleMuon":     "black",
    "SingleElectron": "black",
    "ZJetsToNuNu":    colours_dict["blue"],
    "WJetsToLNu":     colours_dict["green"],
    "WJetsToENu":     colours_dict["lgreen"],
    "WJetsToMuNu":    colours_dict["green"],
    "WJetsToTauNu":   colours_dict["teal"],
    "Diboson":        colours_dict["orange"],
    "DYJetsToLL":     colours_dict["gold"],
    "DYJetsToEE":     colours_dict["gold1"],
    "DYJetsToMuMu":   colours_dict["gold2"],
    "DYJetsToTauTau": colours_dict["gold3"],
    "EWKV2Jets":      colours_dict["purple"],
    "SingleTop":      colours_dict["pink"],
    "TTJets":         colours_dict["violet"],
    "QCD":            colours_dict["red"],
    "G1Jet":          colours_dict["mint"],
    "VGamma":         colours_dict["yellow"],
    "Minor":          colours_dict["gray"],
}

sample_names = {
    "MET":            r'MET',
    "SingleMuon":     r'Single Muon',
    "SingleElectron": r'Single Electron',
    "ZJetsToNuNu":    r'$Z_{\nu\nu}$+jets',
    "WJetsToLNu":     r'$W_{l\nu}$+jets',
    "WJetsToENu":     r'$W_{e\nu}$+jets',
    "WJetsToMuNu":    r'$W_{\mu\nu}$+jets',
    "WJetsToTauNu":   r'$W_{\tau\nu}$+jets',
    "Diboson":        r'Diboson',
    "DYJetsToLL":     r'$Z/\gamma^{*}_{ll}$+jets',
    "DYJetsToEE":     r'$Z/\gamma^{*}_{ee}$+jets',
    "DYJetsToMuMu":   r'$Z/\gamma^{*}_{\mu\mu}$+jets',
    "DYJetsToTauTau": r'$Z/\gamma^{*}_{\tau\tau}$+jets',
    "EWKV2Jets":      r'VBS',
    "SingleTop":      r'Single Top',
    "TTJets":         r'$t\bar{t}$+jets',
    "QCD":            r'Multijet',
    "G1Jet":          r'$\gamma$+jets',
    "VGamma":         r'$V+\gamma$',
    "Minor":          r'Minors',
}

axis_label = {
    "Weight_MET": r'Weight',
    "Weight_SingleMuon": r'Weight',
    "Weight_SingleElectron": r'Weight',
    "METnoX_pt": r'$E_{T}^{miss}$ (GeV)',
    "METnoX_phi": r'$E_{T}^{miss}\ \phi$',
    "METnoX_diMuonParaProjPt_Minus_DiMuon_pt": r'$E_{T,\parallel}^{miss} - p_{T}(\mu\mu)$ (GeV)',
    "METnoX_diMuonPerpProjPt": r'$E_{T,\perp}^{miss}$ (GeV)',
    "DiMuon_pt": r'$p_{T}(\mu\mu)$ (GeV)',
    "DiMuon_phi": r'$p_{T}(\mu\mu)\ \phi$',
    "METnoX_diElectronParaProjPt_Minus_DiElectron_pt": r'$E_{T,\parallel}^{miss} - p_{T}(e e)$ (GeV)',
    "METnoX_diElectronPerpProjPt": r'$E_{T,\perp}^{miss}$ (GeV)',
    "DiElectron_pt": r'$p_{T}(e e)$ (GeV)',
    "DiElectron_phi": r'$p_{T}(e e)\ \phi$',
    "MET_pt": r'$E_{T,PF}^{miss}$ (GeV)',
    "MET_phi": r'$E_{T,PF}^{miss}\ \phi$',
    "CaloMET_pt": r'$E_{T,Calo.}^{miss}$ (GeV)',
    "CaloMET_phi": r'$E_{T,Calo.}^{miss}\ \phi$',
    "HT40": r'$H_{T}(p_{T,j} > 40)$ (GeV)',
    "MHT40_pt": r'$H_{T}^{miss}(p_{T,j} > 40)$ (GeV)',
    "MHT40_phi": r'$H_{T}^{miss}(p_{T,j} > 40)\ \phi$',
    "MHT40_pt_div_METnoX_pt": r'$H_{T}^{miss}(p_{T,j} > 40) / E_{T}^{miss}$',
    "MinDPhiJ1234METnoX": r'$min( \Delta\Phi(j_{1,2,3,4}, E_{T}^{miss}) )$',
    "MET_dCaloMET": r'$|E_{T,PF}^{miss} - E_{T,Calo.}^{miss}| / E_{T}^{miss}$',
    "MTW": r'$m_{T}(l, E_{T,PF}^{miss})$ (GeV)',
    "MLL": r'$m(l, l)$ (GeV)',
    "MLL_wide": r'$m(l, l)$ (GeV)',
    "nJetVeto": r'No. clean veto jets',
    "nJetSelection": r'No. clean selected jets',
    "LeadJetSelection_pt": r'$p_{T}(j_{0})$ (GeV)',
    "LeadJetSelection_eta": r'$\eta(j_{0})$',
    "LeadJetSelection_phi": r'$\phi(j_{0})$',
    "LeadJetSelection_chEmEF": r'$f_{\mathrm{Ch. EM En.}}(j_{0})$',
    "LeadJetSelection_chHEF": r'$f_{\mathrm{Ch. Had. En.}}(j_{0})$',
    "LeadJetSelection_neEmEF": r'$f_{\mathrm{Neut. EM En.}}(j_{0})$',
    "LeadJetSelection_neHEF": r'$f_{\mathrm{Neut. Had. En.}}(j_{0})$',
    "SecondJetSelection_pt": r'$p_{T}(j_{1})$ (GeV)',
    "SecondJetSelection_eta": r'$\eta(j_{1})$',
    "SecondJetSelection_phi": r'$\phi(j_{1})$',
    "DPhiJ1J2": r'$\Delta\phi (j_{0}, j_{1})$',
    "nMuonVeto": r'No. veto muon',
    "nMuonSelection": r'No. selected muon',
    "nElectronVeto": r'No. veto electron',
    "nElectronSelection": r'No. selected electron',
    "nPhotonVeto": r'No. veto photon',
    "nPhotonSelection": r'No. selected photon',
    "nTauVeto": r'No. clean selected $\tau$',
    "nTauSelection": r'No. clean selected $\tau$',
    "nBJetSelectionMedium": r'No. clean selected b-jets (medium WP)',
    "LeadMuonSelection_pt": r'$p_{T}(\mu_{0})$ (GeV)',
    "LeadMuonSelection_eta": r'$\eta(\mu_{0})$',
    "LeadMuonSelection_phi": r'$\phi(\mu_{0})$',
    "SecondMuonSelection_pt": r'$p_{T}(\mu_{1})$ (GeV)',
    "SecondMuonSelection_eta": r'$\eta(\mu_{1})$',
    "SecondMuonSelection_phi": r'$\phi(\mu_{1})$',
    "LeadElectronSelection_pt": r'$p_{T}(e_{0})$ (GeV)',
    "LeadElectronSelection_eta": r'$\eta(e_{0})$',
    "LeadElectronSelection_phi": r'$\phi(e_{0})$',
    "SecondElectronSelection_pt": r'$p_{T}(e_{1})$ (GeV)',
    "SecondElectronSelection_eta": r'$\eta(e_{1})$',
    "SecondElectronSelection_phi": r'$\phi(e_{1})$',
    "PV_npvsGood": r'No. of good PVs',
    "LeptonDevay": r'Lepton decay pdg ID',
    "nGenBosons": r'No. of gen. bosons',
    "GenPartBoson_pt": r'Gen. $p_{T}(V)$ (GeV)',
    "GenPartBoson_eta": r'Gen. $\eta(V)$ (GeV)',
    "GenPartBoson_phi": r'Gen. $\phi(V)$ (GeV)',
    "GenPartBoson_mass": r'Gen. $m(V)$ (GeV)',
    "GenPartBoson_p3": r'Gen. $|p(V)|$ (GeV)',
    "LeadGenPartBosonDaughters_pt": r'Gen. lead lepton $p_{T}$ (GeV)',
    "LeadGenPartBosonDaughters_eta": r'Gen. lead lepton $\eta$',
    "LeadGenPartBosonDaughters_phi": r'Gen. lead lepton $\phi$',
    "LeadGenPartBosonDaughters_p3": r'Gen. lead lepton $|p|$ (GeV)',
    "SecondGenPartBosonDaughters_pt": r'Gen. 2nd lepton $p_{T}$ (GeV)',
    "SecondGenPartBosonDaughters_eta": r'Gen. 2nd lepton $\eta$',
    "SecondGenPartBosonDaughters_phi": r'Gen. 2nd lepton $\phi$',
    "SecondGenPartBosonDaughters_p3": r'Gen. 2nd lepton $|p|$ (GeV)',
    "Jet_genPtClosure": r'$(p_{T}^{j} - p_{T,gen}^{j})/p_{T}^{j}$',
}
