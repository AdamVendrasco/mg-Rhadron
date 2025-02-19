#!/usr/bin/env python3
import ROOT
import matplotlib.pyplot as plt

# File paths
output_dir = "/eos/user/a/avendras/mg-Rhadron/plot_archive/gen_particle_plots/"
root_file_path = "/eos/home-a/avendras/mg-Rhadron/mg-Rhadron_mGl-1800/root-files/mg-Rhadron_mGl-1800-CMSSW_12_4_8-n1000-jet_matching_ON.root"

# Open ROOT file and access tree
f = ROOT.TFile.Open(root_file_path)
tree = f.Get("Events")
n_entries = tree.GetEntries()
print(f"Total entries in tree: {n_entries}")

# Initialize dictionary to store particle data
gen_particle_data = {
    "pt": [], "eta": [], "phi": [], "pdgId": []
}

def extract_gen_particles(event_index):
    """Extracts relevant gen particle attributes for a given event."""
    tree.GetEntry(event_index)
    gen_particles_wrapper = getattr(tree, "recoGenParticles_genParticles__GEN", None)
    if not gen_particles_wrapper: return
    
    gen_particles = gen_particles_wrapper.product()
    if event_index % 100 == 0:
        print(f"Event {event_index} has {gen_particles.size()} gen particles")
    
    for j in range(gen_particles.size()):
        gen = gen_particles.at(j)
        if abs(gen.pdgId()) != 2212 and  abs(gen.pdgId()) != 22:  
            gen_particle_data["pt"].append(gen.pt())
            gen_particle_data["eta"].append(gen.eta())
            gen_particle_data["phi"].append(gen.phi())
            gen_particle_data["pdgId"].append(gen.pdgId())
            if gen.pdgId() == 2212:
                print("hello I am a proton")

# Process all events
for i in range(n_entries):
    extract_gen_particles(i)

def plot_histogram(data, xlabel, title, filename, bins=20, x_range=None, color="red"):
    """Generates and saves a histogram for the given dataset."""
    plt.clf()
    plt.hist(data, bins=bins, histtype="step", color=color, range=x_range)
    plt.xlabel(xlabel)
    plt.ylabel("Counts")
    plt.title(title)
    plt.yscale("log")
    plt.savefig(f"{output_dir}{filename}")
    print(f"Histogram saved as {filename}")
    plt.close()

# Plotting parameters
hist_params = {
    "pt": {"xlabel": "Gen Particle pT", "title": "Gen Particle pT Distribution", "filename": "gen_pt_histogram.png", "bins": 50, "color": "green"},
    "eta": {"xlabel": "Gen Particle Eta", "title": "Gen Particle Eta Distribution", "filename": "gen_eta_histogram.png", "bins": 50, "x_range": (-5, 5), "color": "blue"},
    "phi": {"xlabel": "Gen Particle Phi", "title": "Gen Particle Phi Distribution", "filename": "gen_phi_histogram.png", "bins": 1000, "x_range": (-5, 5), "color": "red"},
    "pdgId": {"xlabel": "Gen Particle pdgId", "title": "Gen Particle pdgId Distribution", "filename": "gen_pdgid_histogram.png", "bins": 50, "color": "red"}
}

# Generate and save histograms
for key, params in hist_params.items():
    plot_histogram(
        gen_particle_data[key],
        xlabel=params["xlabel"],
        title=params["title"],
        filename=params["filename"],
        bins=params["bins"],
        x_range=params.get("x_range", None),
        color=params["color"]
    )
