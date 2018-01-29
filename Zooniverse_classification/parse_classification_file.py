import os, json
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ----------------------------
# -------- Zooniverse data ---
# ----------------------------
print 'Reading data'
zoo_class_data = pd.read_csv('galah-spectra-classifications.csv')
zoo_subjects = Table.read('galah-spectra-subjects.csv', format='ascii.csv')

# ----------------------------
# -------- Settings ----------
# ----------------------------
workflow_id = 5235
workflow_vers_min = 35.

zoo_class_data = zoo_class_data[np.logical_and(zoo_class_data['workflow_id'] == workflow_id,
                                                   zoo_class_data['workflow_version'] >= workflow_vers_min)]

# ----------------------------
# -------- Initial plots -----
# ----------------------------
users, users_count = np.unique(zoo_class_data['user_name'], return_counts=True)
plt.bar(np.arange(len(users)), users_count, color='black', alpha=0.3)
plt.xticks(np.arange(len(users)), users)
plt.semilogy()
plt.title('Classifications per user')
plt.tight_layout()
plt.savefig('users_stats.png')
plt.close()

# ----------------------------
# -------- Determine classes -
# ----------------------------
print 'Parsing input csv with classifications'
data_class_out = Table(names=['sobject_id', 'zoo_selection', 'n_shown'], dtype=['int64', 'S1024', 'int16'])
for idx, class_row in zoo_class_data.iterrows():
    # get user inputs
    user_input = json.loads(class_row['annotations'])[0]['value']
    user_input = '__'.join([str(u) for u in user_input])
    # determine galah sobject_id of the object
    zoo_subject_cur = class_row['subject_ids']
    zoo_subjects_row = zoo_subjects[zoo_subjects['subject_id'] == zoo_subject_cur]
    if len(zoo_subjects_row) == 0:
        # object not found
        continue
    galah_sobject = str(zoo_subjects_row['metadata'])
    galah_sobject = galah_sobject.split(':')[1].split('_')[0][2:]
    # save into output array
    data_class_out.add_row([galah_sobject, user_input, 1])

# determine unique possible inputs
uniq_classes = np.unique(np.hstack([c.split('__') for c in data_class_out['zoo_selection']]))

# add addtitional cols
for u_c in uniq_classes:
    data_class_out[u_c] = 0

# parse zoo_selection field and increase counts for selected classes
print 'Counting classifications'
for i_row in range(len(data_class_out)):
    user_zoo_sel = data_class_out[i_row]['zoo_selection'].split('__')
    for u_z_s in user_zoo_sel:
        data_class_out[i_row][u_z_s] +=1

# remove col that is not nedeed any more
data_class_out.remove_column('zoo_selection')

# combine objects with multiple classification results
print 'Combining multiple classification of an object'
sobj_uniq, sob_c = np.unique(data_class_out['sobject_id'], return_counts=True)
print ' Number of repeats:', np.sum(sob_c > 1)
for sobj_multi in sobj_uniq[sob_c > 1]:
    idx_multi = data_class_out['sobject_id'] == sobj_multi
    data_class_out_sub = data_class_out[idx_multi]
    # aggregate rows
    sum_class_rows = np.sum(data_class_out_sub.to_pandas().values, axis=0)
    sum_class_rows[0] = sobj_multi
    # remove rows of repeats
    data_class_out.remove_rows(np.where(idx_multi)[0])
    # add agregated data back to Table
    data_class_out.add_row(sum_class_rows)

# export final classification results
data_class_out.write('zooniverse_results_20180129.fits', overwrite=True)

# ----------------------------
# -------- Final plots -------
# ----------------------------
n_marked_obj = [np.sum(data_class_out[u_c] >= 1) for u_c in uniq_classes]
plt.bar(np.arange(len(n_marked_obj)), n_marked_obj, color='black', alpha=0.3)
plt.xticks(np.arange(len(uniq_classes)), uniq_classes, rotation=90)
plt.semilogy()
plt.title('Classifications per class')
plt.tight_layout()
plt.savefig('class_stats.png')
plt.close()

