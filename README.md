# PulsarPlotAnalysis

The purpose of this program - and eventually, set of programs - is to take FFT plots and sort through them automatically
without relying on humans. 

As of now, there is one main script - phasesub_stacking_alg.py. This looks through the phase-subband graph row by row, and
treats each of those rows as an individual image. It then stacks those "images" and based on a user-determined threshold,
checks if there are peaks above said threshold. To run the program within the working directory, do:

python phasesub_stacking_alg.py [demo / reg] thresh (how many SD's above the mean)

The options demo and reg control where the program crops out the phase-subband graph from the FFT plot. Demo works for
the sample GBNCC dataset provided, and reg tends to work for data from the GBT. Expect an update soon which will allow for
non-user-dependent line detection and more intelligent automatic cropping.
