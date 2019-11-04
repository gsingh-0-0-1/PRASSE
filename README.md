# PulsarPlotAnalysis

The purpose of this program - and eventually, set of programs - is to take FFT plots and sort through them automatically
without relying on humans. To run the main script within the working directory, do:

python phasesub_stacking_alg.py [crop option] spike_thresh spike_rel_mean_dist noise_thresh noise_rel_mean_distance override nogui

I will provide details as to what each option is below, but if you’re simply looking to run this code, this is currently the best
working option:

python phasesub_stacking_alg.py reg 2.8 35 2.5 42 50000 nogui

spike_thresh:
This option controls the threshold for finding peaks in the data. A higher number means that less points will be flagged as 
a spike or a pulse.

spike_rel_median_dist
This controls how spike_thresh is applied. A larger number tends to stabilize this set of values to a straight line.

noise_thresh:
This is the threshold for something to be considered a horizontal line, and flagged as a noise point. A higher number means that
less points will be flagged as noise.

noise_rel_mean_distance
This serves the same purpose for noise_thresh as the spike_rel_mean_dist serves for spike_thresh

override
This number is sort of a “veto” - if there are any points detected above this threshold, the plot will instantly be dumped into the
pulsar folder. It’s not reliant on any values obtained from the image, which makes it a useful tool.

The options demo and reg (and auto, but that’s still iffy) control where the program crops out the phase-subband graph from the FFT plot. 
For most data, use reg - it works for data from the GBT, at least the data provided on the PSC database. I’ll also be adding an option to 
manually input the location of the phase-subband graph for any given set of plots, to avoid errors - look out for that.

The program also tends to miss pulsars with very wide emissions, as in - when a phase-subband graph’s “lines” are very wide
Or thick, the program tends not to detect them if the threshold is too high. This yields the need for a compromise - either
set the threshold low and widen the bottleneck, allowing more data through the filter - but almost guaranteeing that all 
pulsars are caught, or increase the threshold, decreasing the data you see but increasing the risk of missing a pulsar. 
On the bright side, I do believe this is a problem easily fixed, and this will likely be covered in the next release. Sit
tight.

To get large amounts of data to test this on, either contact me, use the included getplots.py script. Run it like this:

python getplots.py [start dataset] [number of datasets] [directory to download to]

Here’s the Google Drive link where you’ll find test data sets:

https://drive.google.com/drive/folders/1BnETBvG0_tpMDdgcnqM13bYoUaiKwxf9?usp=sharing

Make sure to run the setup.py file before doing anything else.

And remember, this is still in production, so there may be glitches and misclassifications! Contact me if you have a suggestion
I didn’t include here or a bug I missed.