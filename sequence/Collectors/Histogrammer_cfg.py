import numpy as np
from utils.Colours import colours_dict

inf = np.infty
pi = np.pi+0.00001

histogrammer_cfgs = [
    {
        "name": "Weight",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.Weight"],
        "bins": [[-inf]+list(np.linspace(0., 100., 101))+[inf]],
    }, {
        "name": "METnoX_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.METnoX_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
    }, {
        "name": "METnoX_phi",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.METnoX_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "MET_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MET_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
    }, {
        "name": "MET_phi",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MET_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "CaloMET_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.CaloMET_pt"],
        "bins": [[-inf]+list(np.linspace(0., 500., 51))+[inf]],
    }, {
        "name": "CaloMET_phi",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.CaloMET_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "HT40",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.HT40"],
        "bins": [[-inf]+list(np.linspace(0., 3000., 61))+[inf]],
    }, {
        "name": "MHT40_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MHT40_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 41))+[inf]],
    }, {
        "name": "MHT40_phi",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MHT40_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "MHT40_pt_div_METnoX_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MHT40_pt / ev.METnoX_pt"],
        "bins": [[-inf]+list(np.linspace(0., 3., 61))+[inf]],
    }, {
        "name": "MinDPhiJ1234METnoX",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MinDPhiJ1234METnoX"],
        "bins": [[-inf]+list(np.linspace(0., pi, 51))+[inf]],
    }, {
        "name": "MET_dCaloMET",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MET_dCaloMET"],
        "bins": [[-inf]+list(np.linspace(0., 1., 51))+[inf]],
    }, {
        "name": "nJetSelection",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.JetSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 10., 11))+[inf]],
    }, {
        "name": "LeadJetSelection_pt",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1200., 49))+[inf]],
    }, {
        "name": "LeadJetSelection_eta",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
    }, {
        "name": "LeadJetSelection_phi",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "LeadJetSelection_chEmEF",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_chEmEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
    }, {
        "name": "LeadJetSelection_chHEF",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_chHEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
    }, {
        "name": "LeadJetSelection_neEmEF",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_neEmEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
    }, {
        "name": "LeadJetSelection_neHEF",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.LeadJetSelection_neHEF"],
        "bins": [[-inf]+list(np.linspace(0., 1., 41))+[inf]],
    }, {
        "name": "nMuonSelection",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.MuonSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
    }, {
        "name": "nElectronSelection",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.ElectronSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
    }, {
        "name": "nPhotonSelection",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.PhotonSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
    }, {
        "name": "nTauSelection",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.TauSelection.size"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
    }, {
        "name": "nBJetSelectionMedium",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.nBJetSelectionMedium"],
        "bins": [[-inf]+list(np.linspace(0., 5., 6))+[inf]],
    }, {
        "name": "LeadMuonSelection_pt",
        "cutflows": ["SingleMuon", "DoubleMuon"],
        "variables": ["ev: ev.LeadMuonSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
    }, {
        "name": "LeadMuonSelection_eta",
        "cutflows": ["SingleMuon", "DoubleMuon"],
        "variables": ["ev: ev.LeadMuonSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
    }, {
        "name": "LeadMuonSelection_phi",
        "cutflows": ["SingleMuon", "DoubleMuon"],
        "variables": ["ev: ev.LeadMuonSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "SecondMuonSelection_pt",
        "cutflows": ["DoubleMuon"],
        "variables": ["ev: ev.SecondMuonSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
    }, {
        "name": "SecondMuonSelection_eta",
        "cutflows": ["DoubleMuon"],
        "variables": ["ev: ev.SecondMuonSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
    }, {
        "name": "SecondMuonSelection_phi",
        "cutflows": ["DoubleMuon"],
        "variables": ["ev: ev.SecondMuonSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "LeadElectronSelection_pt",
        "cutflows": ["SingleElectron", "DoubleElectron"],
        "variables": ["ev: ev.LeadElectronSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
    }, {
        "name": "LeadElectronSelection_eta",
        "cutflows": ["SingleElectron", "DoubleElectron"],
        "variables": ["ev: ev.LeadElectronSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
    }, {
        "name": "LeadElectronSelection_phi",
        "cutflows": ["SingleElectron", "DoubleElectron"],
        "variables": ["ev: ev.LeadElectronSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "SecondElectronSelection_pt",
        "cutflows": ["DoubleElectron"],
        "variables": ["ev: ev.SecondElectronSelection_pt"],
        "bins": [[-inf]+list(np.linspace(0., 1000., 51))+[inf]],
    }, {
        "name": "SecondElectronSelection_eta",
        "cutflows": ["DoubleElectron"],
        "variables": ["ev: ev.SecondElectronSelection_eta"],
        "bins": [[-inf]+list(np.linspace(-5., 5., 51))+[inf]],
    }, {
        "name": "SecondElectronSelection_phi",
        "cutflows": ["DoubleElectron"],
        "variables": ["ev: ev.SecondElectronSelection_phi"],
        "bins": [[-inf]+list(np.linspace(-pi, pi, 51))+[inf]],
    }, {
        "name": "PV_npvsGood",
        "cutflows": ["Monojet", "SingleMuon", "DoubleMuon", "SingleElectron", "DoubleElectron", "MonojetQCD"],
        "variables": ["ev: ev.PV_npvsGood"],
        "bins": [[-inf]+list(np.linspace(0., 100., 51))+[inf]],
    },
]

sample_colours = {
    "MET":            "black",
    "SingleMuon":     "black",
    "SingleElectron": "black",
    "ZJetsToNuNu":    colours_dict["blue"],
    "WJetsToLNu":     colours_dict["green"],
    "Diboson":        colours_dict["orange"],
    "DYJetsToLL":     colours_dict["gold"],
    "EWKV2Jets":      colours_dict["purple"],
    "SingleTop":      colours_dict["pink"],
    "TTJets":         colours_dict["violet"],
    "QCD":            colours_dict["red"],
    "G1Jet":          colours_dict["mint"],
    "VGamma":         colours_dict["yellow"],
}

axis_label = {
    "Weight": "Weight",
    "METnoX_pt": "E_{T}^{miss} (GeV)",
    "METnoX_phi": "E_{T}^{miss} #phi",
    "MET_pt": "E_{T,PF}^{miss} (GeV)",
    "MET_phi": "E_{T,PF}^{miss} #phi",
    "CaloMET_pt": "E_{T,Calo.}^{miss} (GeV)",
    "CaloMET_phi": "E_{T,Calo.}^{miss} #phi",
    "HT40": "H_{T}(p_{T,j} > 40) (GeV)",
    "MHT40_pt": "H_{T}^{miss}(p_{T,j} > 40) (GeV)",
    "MHT40_phi": "H_{T}^{miss}(p_{T,j} > 40) #phi",
    "MHT40_pt_div_METnoX_pt": "H_{T}^{miss}(p_{T,j} > 40) / E_{T}^{miss}",
    "MinDPhiJ1234METnoX": "min( #Delta#Phi(j_{1,2,3,4}, E_{T}^{miss}) )",
    "MET_dCaloMET": "|E_{T,PF}^{miss} - E_{T,Calo.}^{miss}| / E_{T}^{miss}",
    "nJetSelection": "No. jets selected clean",
    "LeadJetSelection_pt": "p_{T}(j_{0}) (GeV)",
    "LeadJetSelection_eta": "#eta(j_{0})",
    "LeadJetSelection_phi": "#phi(j_{0})",
    "LeadJetSelection_chEmEF": "f_{Ch. EM En.}(j_{0})",
    "LeadJetSelection_chHEF": "f_{Ch. Had. En.}(j_{0})",
    "LeadJetSelection_neEmEF": "f_{Neut. EM En.}(j_{0})",
    "LeadJetSelection_neHEF": "f_{Neut. Had. En.}(j_{0})",
    "nMuonSelection": "No. muon selected",
    "nElectronSelection": "No. electron selected",
    "nPhotonSelection": "No. photon selected",
    "nTauSelection": "No. #tau selected clean",
    "nBJetSelectionMedium": "No. b-jets selected clean (medium WP)",
    "LeadMuonSelection_pt": "p_{T}(#mu_{0}) (GeV)",
    "LeadMuonSelection_eta": "#eta(#mu_{0})",
    "LeadMuonSelection_phi": "#phi(#mu_{0})",
    "SecondMuonSelection_pt": "p_{T}(#mu_{1}) (GeV)",
    "SecondMuonSelection_eta": "#eta(#mu_{1})",
    "SecondMuonSelection_phi": "#phi(#mu_{1})",
    "LeadElectronSelection_pt": "p_{T}(e_{0}) (GeV)",
    "LeadElectronSelection_eta": "#eta(e_{0})",
    "LeadElectronSelection_phi": "#phi(e_{0})",
    "SecondElectronSelection_pt": "p_{T}(e_{1}) (GeV)",
    "SecondElectronSelection_eta": "#eta(e_{1})",
    "SecondElectronSelection_phi": "#phi(e_{1})",
    "PV_npvsGood": "No. of good PVs",
}
