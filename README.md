# PulsarPlotAnalysis

The purpose of this program - and eventually, set of programs - is to take FFT plots and sort through them automatically
without relying on humans. To run the main script within the working directory, do:

python phasesub_stacking_alg.py [crop option] spike_thresh noise_thresh y_relative_mean_distance

For simplicity, crop will usually be ‘reg’ (see below for more detail), spike_thresh should be around 2.5/2.6, noise_thresh
Should be just below - 2.4/2.5, and the last one should almost always be 30.

spike_thresh:
This option controls the threshold for finding peaks in the data. The number entered is how many standard deviations above
The mean a point has to be to be counted as significant.

noise_thresh:
This is a more complicated option, but it works similarly to spike_thresh.

y_relative_mean_distance
This is even more complicated, but keep it at 30. Look through the code to see what exactly it does, if you wish.

The options demo and reg (and auto, but that’s still iffy) control where the program crops out the phase-subband graph from the FFT plot. 
For most data, use reg - it works for data from the GBT, at least the data provided on the PSC database. I’ll also be adding an option to 
manually input the location of the phase-subband graph for any given set of plots, to avoid errors - look out for that.

The program also tends to miss pulsars with very wide emissions, as in - when a phase-subband graph’s “lines” are very wide
Or thick, the program tends not to detect them if the threshold is too high. This yields the need for a compromise - either
set the threshold low and widen the bottleneck, allowing more data through the filter - but almost guaranteeing that all 
pulsars are caught, or increase the threshold, decreasing the data you see but increasing the risk of missing a pulsar. 
On the bright side, I do believe this is a problem easily fixed, and this will likely be covered in the next release. Sit
tight.

To get large amounts of data to test this on, either contact me or use the included getplots.py script. Run it like this:

python getplots.py [start dataset] [end dataset] [directory to download to]

Make sure to run the setup.py file before doing anything else.

And remember, this is still in production, so there may be glitches and misclassifications! Contact me if you have a suggestion
I didn’t include here or a bug I missed.