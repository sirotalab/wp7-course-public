# %% [markdown]
## Neural Data Science
### Exercise 3: Neural populations

# Jonathan Gant, Arash Shahidi, and Wiktor Młynarski
#
# LMU Biology
#
# mlynarski@bio.lmu.de
# %% [markdown]
# 1. Response variability.
#
#       a) compute spike counts  for each neuron for each trial for selected stimuli.
#
#       b) Display histograms of some neurons and plot mean + SD - how much variability is there?
#
#       c)What are the Fano factors/CVs (i.e. ration of SD/mean etc)
# %% [markdown]
# 2. Noise correlations.
#
#       a) Compute noise correlations on individual spikes and for individual stimuli. To do this compute spike counts for each neuron for a given stimulus and then compute correlation matrices between neurons across all trials.
#
#       b)Visualize these noise correlations for different stimuli. Do we see different structure?
# %% [markdown]
# 3. Visualizing neural dynamics.
#
#       a) compute instantaneous firing rates by convolving each neuron on each trial with a Gaussian kernel.
#
#       b) Concantenate multiple trials from  multiple images together and compute PCA, plot variance explained etc.
#
#       c) In the PCA space, plot individual trials of responses to same image on multiple trials and different images on multiple trials. What's visible? How does it relate to noise correlations?
# %%

import numpy as np
import matplotlib.pyplot as plt
import scipy.io
from sklearn.decomposition import PCA

# load data
filepath = "../../data/crcns_pvc8/1.mat"
mat = scipy.io.loadmat(filepath)


# resp_train: array of spiketrains from all neurons to all images/trials
# [#neurons #image #trials #milliseconds]. Time 0 is stimulus onset. Stimuli are presented for 106 ms;
# the times are for when the stimulus is on the screen.

# extract neural responses
R = mat["resp_train"]
n_cells, n_images, n_trials, n_tp = R.shape

# extract stimulus images
I = mat["images"]

print(I.shape)


# %% Plot spike raster  of the entire population for one trial and for one image and plot that image

img_id = 1
trial_id = 1

raster_sel = R[:, img_id, trial_id, :]

plt.figure(figsize=(15, 5))
plt.subplot(1, 5, (1, 4))
plt.imshow(raster_sel, origin="lower", aspect="auto", cmap="Greys")
# plt.colorbar()
plt.xlabel("Time [ms]")
plt.ylabel("Neuron ID")
plt.title("Population response to image %d trial %d" % (img_id, trial_id))

plt.subplot(1, 5, 5)
plt.imshow(I[0, img_id], aspect="equal", cmap="Greys_r")
plt.title("Stimulus %d" % img_id)
plt.tick_params(
    axis="both",
    which="both",
    bottom=False,
    left=False,
    labelbottom=False,
    labelleft=False,
)


# %% Plot spike raster of the single neuron population for all trials for one image and plot that image

img_id = 95
cell_id = 8

raster_sel = R[cell_id, img_id, :, :]

plt.figure(figsize=(15, 5))
plt.subplot(1, 5, (1, 4))
plt.imshow(raster_sel, origin="lower", aspect="auto", cmap="Greys")
# plt.colorbar()
plt.xlabel("Time [ms]")
plt.ylabel("Trial ID")
plt.title("Responses of neuron %d to stimulus %d" % (cell_id, img_id))

plt.subplot(1, 5, 5)
plt.imshow(I[0, img_id], aspect="equal", cmap="Greys_r")
plt.title("Stimulus %d" % img_id)
plt.tick_params(
    axis="both",
    which="both",
    bottom=False,
    left=False,
    labelbottom=False,
    labelleft=False,
)


# %%

# Select full images

# Odd images from 1 to 539 are full images, even images from 2 to 540 are partial images
plot_images = False
if plot_images:
    for i in range(I.shape[1]):
        if i % 2 == 1 and i < 540:
            plt.subplot(1, 5, 5)
            plt.imshow(I[0, i], aspect="equal", cmap="Greys_r")
            plt.title("Stimulus %d" % i)
            plt.tick_params(
                axis="both",
                which="both",
                bottom=False,
                left=False,
                labelbottom=False,
                labelleft=False,
            )
            plt.show()

R_subset = R[:, 1:541:2, :, :]
I_subset = I[0, 1:541:2]

# %%
