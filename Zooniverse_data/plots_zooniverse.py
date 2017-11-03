import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from astropy.table import Table
from Inspect_GALAH_class import *

# ## Assuming you want to look at specific lines (and check RV), then use define the 'help_lines' variable before plotting, otherwise define 'help_line=False'
help_lines=[
    (r'$\mathrm{H_\alpha}$',6562.7970),
    (r'$\mathrm{H_\beta}$' ,4861.3230),
    (r'$\mathrm{Li}$'      ,6707.7635)
    ]
spectra_dir = '/media/storage/HERMES_REDUCED/dr5.2/'

sobjects = [
140709001901194, 150210006401171
]
for s_id in sobjects:
	print 'Working on a sobject_id '+str(s_id)
	# Now let's create the class FITS for a given sobject_id and use the provided functions on it!
	fits = fits_class(sobject_id=s_id, directory=spectra_dir)

	# ## Plot normalised spectrum on 4 axes
	print 'Plotting'
	fits.plot_norm_spectrum_on4axes(help_lines=help_lines, savefig='PLOTS_4CCDs_HaHbasym')
