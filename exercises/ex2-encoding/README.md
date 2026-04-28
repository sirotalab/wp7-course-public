# Exercise 2 — Encoding in Single Neurons

## Topic

Linear and generalized-linear encoding models for single neurons. You will
fit a linear–Gaussian receptive field via spike-triggered averaging on
natural and white-noise stimuli, study how stimulus statistics bias the
STA and how whitening + MAP estimation correct for it, then move to a
Poisson GLM fit to retinal-ganglion-cell spike trains.

## Style

**Roadmap with two parts; open-ended within each.** The starter sets
out the procedural arc (build model → simulate → estimate → diagnose)
and gives you the Gabor generator + data-loading boilerplate. You decide
the parameter sweeps, regularization strengths, diagnostics, and how to
report the comparisons. No autograder.

## Files in this directory

- `starter.ipynb` — Wiktor's open-ended prompt (Młynarski, 2026), adapted from Pillow et al, *Nature* 2008.
- `landscape.png` — natural-image source for the patch sampler in Part 1.
- `README.md` — this file.

Create your working copy with `pixi run start ex2` (produces `ex2.ipynb`).
Edit that, not `starter.ipynb`.

## Data

**Part 1** — synthetic stimuli plus natural patches sampled from the
co-located `landscape.png`. No external data file needed.

**Part 2** — retinal-ganglion-cell recordings from Uzzell & Chichilnisky
(2004), prepared by the Pillow lab:

    ../../data/data_RGCs/Stim.mat
    ../../data/data_RGCs/SpTimes.mat
    ../../data/data_RGCs/stimtimes.mat

Load with `scipy.io.loadmat`. See `../../data/data_RGCs/README.txt` for
variable shapes and sampling rate. Provided for tutorial use only — do
not redistribute.

## Prerequisites

- **Lectures:** Młynarski — Encoding in single neurons (Lec 02)
- **Previous exercises:** Ex1 (bootstrap / numpy + scipy fluency)
- **Packages:** `numpy`, `scipy`, `matplotlib`, `opencv` (`cv2` for image read), `statsmodels` (Poisson GLM)

## Reading (optional — pick what helps)

- Pillow et al (2008) — [Spatio-temporal correlations and visual signalling in a complete neuronal population](http://pillowlab.princeton.edu/pubs/abs_Pillow08_nature.html). The Nature paper the GLM half is adapted from.
- Schwartz et al (2006) — [Spike-triggered neural characterization](https://jov.arvojournals.org/article.aspx?articleid=2192881). STA + spike-triggered covariance, why whitening matters.
- Paninski (2004) — [Maximum likelihood estimation of cascade point-process neural encoding models](https://www.tandfonline.com/doi/abs/10.1088/0954-898X_15_4_002). The MLE / GLM framework underpinning Part 2.
- Murphy — *Machine Learning: A Probabilistic Approach*, §11.3 (GLMs), §7.5 (MAP / regularization).

## Submit

```bash
pixi run submit ex2
```

See the course site's [Submissions](../../../../website/docs/submissions.md) page for the full contract.
