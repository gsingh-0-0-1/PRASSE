# PulsarPlotAnalysis

Written by Gurmehar Singh - gurmehar@gmail.com. Please contact me if you have any questions or would like to contribute!
This is a work in progress, and more contributors is always better.

The purpose of this repository is to take FFT plots and sort through them automatically
without relying on humans. The tests were run on a 2015 MacBook Pro - specs blow:

Processor: 2.7 GHz Intel Core i5

Memory: 8 GB 1867 MHz DDR3 

Keep these in mind when looking at runtime statistics.

Download and use instructions:

To get the latest stable code, head to the releases section and download the .zip file - the source code - for the latest
release. Extract the .zip file and move the folder anywhere you want. From there, open command line and navigate inside the folder.

Make sure to run the setup.py file before doing anything else. Simply do:

```python setup.py```

This will install all the necessary dependencies.

# Version 1.1.0

To run the main script within the working directory for data from the Green Bank Telescope - specifically that provided by the Pulsar Search Collaboratory (PSC) - run:

```python phasesub_stacking_alg.py reg default nogui```

For data from the PSC, there is an added benefit - I have programmed the script to ignore certain frequencies at which RFI is common, so the filter efficiency is a bit higher.

For other data, use:

```python phasesub_stacking_alg.py inp default nogui```

The program will then prompt you to enter

This algorithm does quite well overall - its true positive rate is effectively 100% - it has detected all of the pulsars that have been fed into it. For reference,
355 individual pulsars were put through the program, and all were detected. Given that the current number of known pulsars is around 3,000, this is quite a good
test set. It has a rough false positive rate of 4.5%, based on experimental statistics consisting of over 25,000 individual pieces of data. However, this statistic
depends heavily on how much radio frequency interference appears in the data, which can sometimes slip through the filter. This is the main focus of the project right now,
to ensure that only pulsars make it through the filter. The average runtime hovers around 3 plots per second.

Also, the program will only sort RFI for data from the Pulsar Search Collaboratory provided by the Green Bank Telescope. This is due to different data being formatted differently,
and the location of the DM may be different from plot to plot. Feel free to modify the code to be more flexible and send in a pull request, or contact me with a suggestion.

If you want to play around with individual values that affect the filter, here is the full command:

```python phasesub_stacking_alg.py [crop option] spike_thresh spike_rel_mean_dist noise_thresh noise_rel_mean_distance override obj_min nogui```

I will provide details as to what each option is below, but if you’re simply looking to use this code to get through a lot of data, ignore the following descriptions.

```crop option:```
This option controls how the program crops out the phase-subband graphs. Use “reg” for data from the GBT, and “inp” for other data. If you
use this option, make sure to first check the coordinates in the image of the phase-subband graphs - do this after resizing the image to
780 by 582. The program will automatically resize the images to this size, but you’ll have to tell the program where to crop out the image.
I will likely implement a functional auto-cropping in the near future.

```spike_thresh:```
This option controls the threshold for finding peaks in the data. A higher number means that less points will be flagged as 
a spike or a pulse.

```spike_rel_median_dist:```
This controls how spike_thresh is applied. A larger number tends to stabilize this set of values to a straight line.

```noise_thresh:```
This is the threshold for something to be considered a horizontal line, and flagged as a noise point. A higher number means that
less points will be flagged as noise.

```noise_rel_mean_distance:```
This serves the same purpose for noise_thresh as the spike_rel_mean_dist serves for spike_thresh

```override:```
This number is sort of a “veto” - if there are any points detected above this threshold, the plot will instantly be dumped into the
pulsar folder. It’s not reliant on any values obtained from the image, which makes it a useful tool.

```obj_min:```
This works as the opposite of the override parameter.

For more detailed descriptions, please contact me - it would take a while to explain the entire algorithm here, and I’m not sure I’d be able
to do a decent job in a written paragraph :).

There is also a test feedforward convolutional network included. This uses the principles of a neural network and convolution to analyze
images. Currently, it has detected all pulsars fed into it, giving it a true-positive rate of 100%, and from testing, it has a false positive
rate of around 4.6% - about the same as the first algorithm. However, it does work a bit slower than the first algorithm, at around 1 plot a 
second. This will likely go obsolete and be replaced by a model constructed with TensorFlow in the future, as this was mainly an experiment
I did to test a theory I had.

To get large amounts of data to test this on, either contact me, use the included getplots.py script. Run it like this:

python getplots.py [start dataset] [number of datasets] [directory to download to] [fft/singlepulse]

This will prompt you to enter your PSC username and password.

Alternatively, here’s the Google Drive link where you’ll find test data sets:

https://drive.google.com/drive/folders/1BnETBvG0_tpMDdgcnqM13bYoUaiKwxf9?usp=sharing

Data should go into the “images” folder - put this in the download directory option - and they will be sorted into “pulsar” and “not_pulsar” by the program. For the ```reg``` crop option, the program will check DM when it detects a pulsar, and sort that into an RFI folder.

And remember, this is still in production, so there may be glitches and misclassifications! Contact me if you have a suggestion
I didn’t include here or a bug I missed.

Huge thanks to Martin Nikolov (marvic2409) for helping troubleshoot the software and providing a ton of extra data, as well as programming most of the web integration for 
this software - coming soon.

Credits to Vibha for providing the known pulsars dataset.