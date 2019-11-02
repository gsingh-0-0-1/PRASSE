# PulsarPlotAnalysis

The purpose of this program - and eventually, set of programs - is to take FFT plots and sort through them automatically
without relying on humans. To run the main script within the working directory, do:

python phasesub_stacking_alg.py [crop option] spike_thresh noise_thresh y_relative_mean_distance

For simplicity, crop will usually be ‘reg’ (see below for more detail), spike_thresh should be around 2.5/2.6, noise_thresh
Should be just below - 2.4/2.5, and the last one should almost always be 30.

The options demo and reg control where the program crops out the phase-subband graph from the FFT plot. Demo works for
the sample GBNCC dataset provided, and reg tends to work for data from the GBT. Expect an update soon which will allow for
non-user-dependent line detection and more intelligent automatic cropping. I’ll also be adding an option to manually input
the location of the phase-subband graph for any given set of plots, to avoid errors. Look out for that.

The program also tends to miss pulsars with very wide emissions, as in - when a phase-subband graph’s “lines” are very wide
Or thick, the program tends not to detect them if the threshold is too high. This yields the need for a compromise - either
set the threshold low and widen the bottleneck, allowing more data through the filter - but almost guaranteeing that all 
Pulsars are caught, or increase the threshold, decreasing the data you see but increasing the risk of missing a pulsar. 
On the bright side, I do believe this is a problem easily fixed, and this will likely be covered in the next release. Sit
tight.

Oddly enough, GitHub does not allow for empty directories to exist in repos, so just run the setup.py file if you decide to
Clone or download to repo.