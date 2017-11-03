import os
from subprocess import call
from astropy.table import Table
import numpy as np

'''
16042 GALAH_APOGEE
16043 GALAH_bensby
16051 GALAH_bmstar
15988 GALAH_coolG
16046 GALAH_HIP_lbol
16047 GALAH_Li_rich
15983 GALAH_MP
15984 GALAH_MPl
15982 GALAH_OCGC
15987 GALAH_seis
15986 GALAH_TGAS_lbol
15985 GALAH_ts_iDR1
'''

# project and subject set ids
project_id = 5471
subject_set_id = 15985
subject_ids_csv = 'galah-spectra-subjects.csv'

# read data
subject_ids_data = Table.read(subject_ids_csv, format='ascii.csv')

# subset of data for selected set
subject_ids_data = subject_ids_data[subject_ids_data['subject_set_id'] == subject_set_id]
subject_ids_data.filled()

# found unique and repeated id
u_filename = subject_ids_data['metadata']  # examplelooks like "{""Filename"":""131216002601003_norm.png""}"
u_filename = np.array([f.split(':')[1][2:-4] for f in u_filename])
u_filename_uniq, u_filename_count = np.unique(u_filename, return_counts=True)
u_filename_rep = u_filename_uniq[u_filename_count > 1]
if len(u_filename_rep) < 1:
	raise SystemExit

# get subject_id for all of the repeats
remove_s_ids = list([])
for u_id in u_filename_rep:
	idx_rep = np.where(u_filename == u_id)[0]
	subject_ids_rep = subject_ids_data[idx_rep]['subject_id'].data
	remove_s_ids.append(subject_ids_rep[1:])

remove_s_ids = np.hstack(remove_s_ids)
print 'To remove:',len(remove_s_ids)

# construct cmd command that shold be run to remove the repeats
list_subject_ids_str = ' '.join([str(r_id) for r_id in remove_s_ids])
comand = 'panoptes subject-set remove-subjects '+str(subject_set_id)+' '+list_subject_ids_str

print comand
# call(comand)
os.system(comand)

