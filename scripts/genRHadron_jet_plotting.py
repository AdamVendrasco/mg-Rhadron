import ROOT
import matplotlib.pyplot as plt

output_directory = "/eos/user/a/avendras/mg-Rhadron/plot_archive/gen_RHadron_1800_jetmatching_plots/"
root_file_path = "/eos/home-a/avendras/mg-Rhadron/mg-Rhadron_mGl-1800/root-files/mg-Rhadron_mGl-1800-CMSSW_12_4_8-n1000-jet_matching_ON.root"

# Open the ROOT file, access the tree
f = ROOT.TFile.Open(root_file_path)
tree = f.Get("Events")
n_entries = tree.GetEntries()
print("Total entries in tree:", n_entries)

# ---------------
# Debug: Inspection of reco::GenParticle.
# ---------------
tree.GetEntry(0)
gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN")
if gen_particles_wrapper:
    gen_particles = gen_particles_wrapper.product()
    if gen_particles.size() > 0:
        first_gen = gen_particles.at(0)
        print("Methods and attributes of reco::GenParticle:")
        print(dir(first_gen))

# Target RHadron PDG IDs
target_pdgIds = { ... }

# Dictionaries to store data
gen_particle_data = {
    "pt": [],  # Store pT of the leading RHadrons
    "all_pt": [],  # Store pT of all RHadrons
    "pdgId": [],
}

jet_data = {
    "leading_jet_pt": [],  # Store pT of the leading jet
}

def extract_gen_particles(event_index):
    """Extracts relevant gen particle attributes for a given event."""
    tree.GetEntry(event_index)
    gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN", None)

    if not gen_particles_wrapper:
        return  # Skip event if wrapper is missing

    gen_particles = gen_particles_wrapper.product()
    if event_index % 100 == 0:
        print(f"Event {event_index} has {gen_particles.size()} gen particles")

    # Find the leading RHadron in the event
    leading_pt = None
    leading_eta = None
    leading_phi = None
    leading_pdgId = None

    for j in range(gen_particles.size()):
        gen = gen_particles.at(j)
        if abs(gen.pdgId()) in target_pdgIds:
            # Record all RHadrons' pT
            gen_particle_data["all_pt"].append(gen.pt())

            if leading_pt is None or gen.pt() > leading_pt:
                leading_pt = gen.pt()
                leading_eta = gen.eta()
                leading_phi = gen.phi()
                leading_pdgId = gen.pdgId()

    # If a leading RHadron is found, store its pt, eta, phi, and pdgid
    if leading_pt is not None:
        gen_particle_data["pt"].append(leading_pt)
        gen_particle_data["pdgId"].append(leading_pdgId)
        print(f"Event {event_index}: Leading RHadron - pT: {leading_pt:.2f}, eta: {leading_eta:.2f}, phi: {leading_phi:.2f}, pdgId: {leading_pdgId}")

def extract_leading_jet(event_index):
    """Extracts the leading jet pT for a given event."""
    tree.GetEntry(event_index)
    gen_jets_wrapper = getattr(tree, "recoGenJets_ak4GenJets__GEN", None)

    if not gen_jets_wrapper:
        return  # Skip event if wrapper is missing

    gen_jets = gen_jets_wrapper.product()
    if gen_jets.size() == 0:
        return  # No jets in this event

    # Find the leading jet
    leading_jet_pt = max(gen_jets, key=lambda jet: jet.pt()).pt()

    jet_data["leading_jet_pt"].append(leading_jet_pt)
    
    if event_index % 100 == 0:
        print(f"Event {event_index}: Leading jet pT = {leading_jet_pt:.2f}")

# Process all events
for i in range(n_entries):
    extract_gen_particles(i)
    extract_leading_jet(i)

def plot_histogram(data1, data2=None, xlabel="", title="", filename="", bins=20, x_range=None, color1="red", color2="blue"):
    """Generates and saves histogram for given dataset."""
    plt.clf()
    plt.figure(figsize=(8, 6))

    plt.hist(data1, bins=bins, histtype="step", color=color1, alpha=0.7, label="Leading RHadrons")
    if data2 is not None:
        plt.hist(data2, bins=bins, histtype="step", color=color2, alpha=0.7, label="All RHadrons")

    if x_range is not None:
        plt.xlim(x_range)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.title(title)
    plt.yscale("log")
    plt.legend()

    if xlabel == "Gen RHadron Eta":
        plt.ylim(1, max(plt.ylim()[1], 1e6))
    plt.savefig(f"{output_directory}{filename}")
    print(f"Histogram saved as {filename}")
    plt.close()

# Generate histograms
hist_params = {
    "pt": { "xlabel": "Gen RHadron pT", "title": "Leading vs All RHadron pT Distribution", "filename": "leading_vs_all_gen_RHadron_pt_histogram.png", "bins": 50, "color1": "green", "color2": "blue" },
    "pdgId": { "xlabel": "Gen RHadron pdgId", "title": "Gen RHadron pdgId Distribution", "filename": "gen_RHadron_pdgid_histogram.png", "bins": 50 }
}

plot_histogram(
    gen_particle_data["pt"],
    gen_particle_data["all_pt"],
    xlabel=hist_params["pt"]["xlabel"],
    title=hist_params["pt"]["title"],
    filename=hist_params["pt"]["filename"],
    bins=hist_params["pt"]["bins"],
    color1=hist_params["pt"]["color1"],
    color2=hist_params["pt"]["color2"]
)

for key, params in hist_params.items():
    if key != "pt":
        plot_histogram(
            gen_particle_data[key],
            xlabel=params["xlabel"],
            title=params["title"],
            filename=params["filename"],
            bins=params["bins"]
        )

# Plot leading jet pt
title = "Leading Jet pT Distribution"
plot_histogram(
    jet_data["leading_jet_pt"],
    xlabel="Leading Jet pT [GeV]",
    title=title,
    filename="leading_jet_pt_histogram.png",
    bins=50,
    color1="red"
)
