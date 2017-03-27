

def get_tumor_rec(df, patient_id):
    """
    Returns the target value for the patient 
    (1 or 0 coding for tumor recurrence)
    """
    return int(df[df.Patient_ID==patient_id].Local_tumor_recurrence)


def get_hpv_status(df, patient_id):
    """
    Returns the target value for the patient 
    (1 or 0 coding for hpv status)
    """
    return int(df[df.Patient_ID==patient_id]['HPV/p16_status'])


def get_patients_by_rec(df, patient_list, patient_patches, hpv_status):
    """
    Returns the sublist of patient_list for which the recurrence_status in df is either 0 or 1
    checks if at least one patch is available by looking up in patient_patches
    """
    patients = []
    counter = 0
    for patient in patient_list:
        if (len(patient_patches[patient])>0):
            patient_status = get_hpv_status(df, patient)
            counter += 1-patient_status
            if(patient_status==hpv_status):
                patients.append(patient)
    return patients

def get_hpv_status_dic(df):
    hpv_dic = {}
    for patient_id in list(df.Patient_ID):
        hpv_dic[patient_id] = get_hpv_status(df, patient_id)
    return hpv_dic
