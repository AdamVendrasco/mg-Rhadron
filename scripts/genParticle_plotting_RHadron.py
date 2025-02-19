import ROOT
import matplotlib.pyplot as plt

# ========================================
# Setup and ROOT File Initialization
# ========================================
output_directory = "/eos/user/a/avendras/mg-Rhadron/plot_archive/gen_RHadron_1800_jetmatching_plots/"
root_file_path = "/eos/user/a/avendras/mg-Rhadron/mg-Rhadron_mGl-1800/root-files/mg-Rhadron_mGl-1800-CMSSW_12_4_8-n1000-jet_matching_ON.root"

# Open the ROOT file and access the tree
f = ROOT.TFile.Open(root_file_path)
tree = f.Get("Events")
n_entries = tree.GetEntries()
print("Total entries in tree:", n_entries)

# ========================================
# List All Branches in the Tree
# ========================================
def list_branches():
    branches = tree.GetListOfBranches()
    print("\nList of branches in the tree:")
    for branch in branches:
        print(branch.GetName())

list_branches()

# ========================================
# Define Target RHadron pdgId Range
# ========================================
target_pdgIds = set(range(1000000, 1010000)) 

# ========================================
# Debug: Inspection of reco::GenParticle
# ========================================
def inspect_gen_particles(event_index=0):
    tree.GetEntry(event_index)
    gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN", None)
    if gen_particles_wrapper:
        gen_particles = gen_particles_wrapper.product()
        if gen_particles.size() > 0:
            first_gen = gen_particles.at(0)
            print("\nMethods and attributes of reco::GenParticle:")
            print(dir(first_gen))

inspect_gen_particles()

# ========================================
# Inspecting recoGenJets_ak4GenJets__GEN Branch Contents
# ========================================
def inspect_jet_branches():
    ak4_branch = tree.GetBranch("recoGenJets_ak4GenJets__GEN.")
    if ak4_branch:
        print("\nFound branch using GetBranch:", ak4_branch.GetName())
    else:
        print("\nBranch recoGenJets_ak4GenJets__GEN not found using GetBranch.")

    ak8_branch = tree.GetBranch("recoGenJets_ak8GenJets__GEN.")
    if ak8_branch:
        print("Found branch using GetBranch:", ak8_branch.GetName())
    else:
        print("Branch recoGenJets_ak8GenJets__GEN not found using GetBranch.")

inspect_jet_branches()

# ========================================
# Extract RHadron pT Information
# ========================================
all_gen_pt = []  # all_gen -> RHadron ### NEED TO redefine this for better var name
all_gen_eta = []
leading_gen_pt = []  # leading_gen -> leading RHadron pT per event ### NEED TO redefine this for better var name

def extract_gen_particles(event_index):
    """Extracts leading gen particle pT for a given event (for target RHadrons)."""
    tree.GetEntry(event_index)
    gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN", None)
    if not gen_particles_wrapper:
        return

    gen_particles = gen_particles_wrapper.product()
    if event_index % 100 == 0:
        print(f"Event {event_index} has {gen_particles.size()} gen particles")
    
    leading_pt = 0
    for j in range(gen_particles.size()):
        gen = gen_particles.at(j)
        if 1000600 <= abs(gen.pdgId()) <= 1100000:
            all_gen_pt.append(gen.pt())
            all_gen_eta.append(gen.eta())
            if gen.pt() > leading_pt:
                leading_pt = gen.pt()
    if leading_pt > 0:
        leading_gen_pt.append(leading_pt)

# Process each event for RHadron information
for i in range(n_entries):
    extract_gen_particles(i)

# ========================================
# Extract Leading Jet pT from GenParticles (using isJet flag)
# ========================================
leading_jet_pt_from_gen = []

def extract_leading_jet_pt_from_gen(event_index):
    """
    Extracts the leading jet pT from gen particles marked as jets (isJet() == True)
    in a given event.
    """
    tree.GetEntry(event_index)
    gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN", None)
    if not gen_particles_wrapper:
        return

    gen_particles = gen_particles_wrapper.product()
    max_pt = 0
    for j in range(gen_particles.size()):
        gen = gen_particles.at(j)
        if gen.isJet() and gen.pt() > max_pt:
            max_pt = gen.pt()
    if max_pt > 0:
        leading_jet_pt_from_gen.append(max_pt)

# Process each event for leading jet pT
for i in range(n_entries):
    extract_leading_jet_pt_from_gen(i)

print(f"\nExtracted leading jet (from gen particles) pT for {len(leading_jet_pt_from_gen)} events.")

# ========================================
# Extract Leading AK4 Jet pT from recoGenJets_ak4GenJets__GEN branch
# ========================================
leading_ak4_pt = []

def extract_leading_ak4_pt(event_index):
    """Extracts the leading AK4 jet pT from the recoGenJets_ak4GenJets__GEN branch."""
    tree.GetEntry(event_index)
    ak4jets_wrapper = getattr(tree, "recoGenJets_ak4GenJets__GEN", None)
    if not ak4jets_wrapper:
        return
    ak4jets = ak4jets_wrapper.product()
    if ak4jets.size() == 0:
        return
    max_pt = 0.0
    for j in range(ak4jets.size()):
        jet = ak4jets.at(j)
        if jet.pt() > max_pt and jet.status() == 1:
            max_pt = jet.pt()
    if max_pt > 0:
        leading_ak4_pt.append(max_pt)

# Process each event for leading AK4 jet pT
for i in range(n_entries):
    extract_leading_ak4_pt(i)

print(f"\nExtracted leading AK4 jet pT for {len(leading_ak4_pt)} events.")

# ========================================
# Extract Leading AK8 Jet pT from recoGenJets_ak8GenJets__GEN branch
# ========================================
leading_ak8_pt = []

def extract_leading_ak8_pt(event_index):
    """Extracts the leading AK8 jet pT from the recoGenJets_ak8GenJets__GEN branch."""
    tree.GetEntry(event_index)
    ak8jets_wrapper = getattr(tree, "recoGenJets_ak8GenJets__GEN", None)
    if not ak8jets_wrapper:
        return
    ak8jets = ak8jets_wrapper.product()
    if ak8jets.size() == 0:
        return
    max_pt = 0.0
    for j in range(ak8jets.size()):
        jet = ak8jets.at(j)
        if jet.pt() > max_pt:
            max_pt = jet.pt()
    if max_pt > 0:
        leading_ak8_pt.append(max_pt)

# Process each event for leading AK8 jet pT
for i in range(n_entries):
    extract_leading_ak8_pt(i)

print(f"\nExtracted leading AK8 jet pT for {len(leading_ak8_pt)} events.")

# ========================================
# Plotting Functions
# ========================================
def plot_histogram(data, xlabel, title, filename, bins=20, x_range=None, color="red"):
    """Generates and saves a histogram for a given dataset."""
    plt.clf()
    plt.figure(figsize=(8, 6))
    plt.hist(data, bins=bins, histtype="step", color=color)
    if x_range is not None:
        plt.xlim(x_range)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.title(title)
    plt.yscale("log")

    if xlabel == "Gen RHadron Eta":
        plt.ylim(1, max(plt.ylim()[1], 1e6))
    
    plt.savefig(f"{output_directory}{filename}")
    print(f"Histogram saved as {filename}")
    plt.close()

def plot_overlay_histograms(data_dict, xlabel, title, filename, bins=50, x_range=None):
    """Generates and saves an overlay of histograms for multiple datasets."""
    plt.clf()
    plt.figure(figsize=(8, 6))
    for label, data in data_dict.items():
        plt.hist(data, bins=bins, histtype="step", label=label)
    if x_range is not None:
        plt.xlim(x_range)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.title(title)
    plt.yscale("log")

    if xlabel == "Gen RHadron Eta":
        plt.ylim(1, max(plt.ylim()[1], 1e6))
    
    plt.legend()
    plt.savefig(f"{output_directory}{filename}")
    print(f"Overlay histogram saved as {filename}")
    plt.close()

# ========================================
# Plotting RHadron pT Distributions
# ========================================
# Overlay of RHadron pT distributions
overlay_data = {
    "Leading Gen RHadron pT": leading_gen_pt,
    "All Gen RHadron pT": all_gen_pt,
}
plot_overlay_histograms(
    overlay_data,
    xlabel="Gen RHadron pT (GeV)",
    title="Overlay of Leading and All Gen_1800_RHadron pT Distributions",
    filename="overlay_gen_RHadron_pt_histogram.png",
    bins=50
)

# Individual RHadron pT histograms
hist_params = {
    "leading_pt": {
        "xlabel": "Leading Gen RHadron pT (GeV)",
        "title": "Leading Gen_1800_RHadron pT Distribution",
        "filename": "leading_gen_RHadron_pt_histogram.png",
        "bins": 50,
        "color": "blue"
    },
    "all_pt": {
        "xlabel": "All Gen RHadron pT (GeV)",
        "title": "All Gen_1800_RHadron pT Distribution",
        "filename": "all_gen_RHadron_pt_histogram.png",
        "bins": 50,
        "color": "orange"
    },
    "all_gen_eta": {
        "xlabel": "All Gen RHadron Eta",
        "title": "All 1800_Gen_RHadron Eta",
        
        "filename": "gen_RHadron_eta_histogram.png",
        "bins": 50,
        "color": "orange"
    }  
}

gen_particle_data = {
    "leading_pt": leading_gen_pt,
    "all_pt": all_gen_pt,
    "all_gen_eta": all_gen_eta  
}

for key, params in hist_params.items():
    plot_histogram(
        gen_particle_data[key],
        xlabel=params["xlabel"],
        title=params["title"],
        filename=params["filename"],
        bins=params["bins"],
        color=params["color"]
    )


# ========================================
# Plotting Leading AK4 Jet pT Distribution
# ========================================
plot_histogram(
    leading_ak4_pt,
    xlabel="Leading AK4 Jet pT (GeV)",
    title="Leading AK4 Jet pT Distribution",
    filename="leading_ak4_jet_pt_histogram.png",
    bins=50,
    color="blue"
)

# ========================================
# Plotting Leading AK8 Jet pT Distribution
# ========================================
plot_histogram(
    leading_ak8_pt,
    xlabel="Leading AK8 Jet pT (GeV)",
    title="Leading AK8 Jet pT Distribution",
    filename="leading_ak8_jet_pt_histogram.png",
    bins=50,
    color="orange"
)

# ========================================
# Plotting Overlay of Leading AK4 and AK8 Jet pT Distributions
# ========================================
overlay_ak_jets = {
    "Leading AK4 Jet": leading_ak4_pt,
    "Leading AK8 Jet": leading_ak8_pt
}
plot_overlay_histograms(
    overlay_ak_jets,
    xlabel="Jet pT (GeV)",
    title="Overlay of Leading AK4 and AK8 Jet pT Distributions",
    filename="overlay_leading_ak4_ak8_jet_pt_histogram.png",
    bins=50
)
