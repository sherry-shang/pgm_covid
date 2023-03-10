import dash  # pip install dash
import dash_cytoscape as cyto  # pip install dash-cytoscape==0.2.0 or higher
from dash import html
from dash.dependencies import Output, Input, State
import copy
import dash_bootstrap_components as dbc
import networkx as nx
from pgmpy.models import BayesianNetwork
from pgmpy.estimators import MaximumLikelihoodEstimator
from pgmpy.inference import VariableElimination
import pandas as pd  # pip install pandas
from app_whole import app
import re

def GenerateSubBayesianNetwork( g, source, target ):
    edges = set()
    max_len  = len(shortest_path1(g, source, target)) - 1
    all_paths = nx.all_simple_paths(g, source, target, cutoff = max_len)
    for path in all_paths:
        for i in range( len( path ) - 1 ):
            edges.add( ( path[i], path[i+1] ) )
    return BayesianNetwork( list( edges ) )

dt = pd.read_csv('cond_prob_sev.csv')
#reference = pd.read_pickle("C:\\Users\\shang\\Downloads\\sev_discrete_to_real(1).pickle")

cyto.load_extra_layouts()
'''
demographic=[ 'Age au recrutement',
'Age au recrutement:',
 'BMI:',
'Electronic cigarettes?',
'Height in m:',
'Living where?',
'Living with?',
 'Is the participant employed as a Healthcare Worker?  ',
 'Is the participant employed in a Microbiology Laboratory?  ',
'Patient pregnant?',
 'Sex at birth:',
 'Sexe:',
 'Smoking status:',
'Weight in kg:',
]
treatment=[
'Anticoagulants?',
'Adjunctive therapy during hospitalization',
'Colchicine?',
 'Dialysis ?',
'Did or does the patient receive adjunctive therapy?',
 'Did or does the patient receive ventilatory support?',
'Drugs?',
'HGO or insulin?',
 'If yes (check all that apply): (choice=Blood transfusion)',
 'If yes (check all that apply): (choice=Dialysis or hemofiltration)',
 'If yes (check all that apply): (choice=Extracorporeal membrane oxygenation (ECMO))',
 'If yes (check all that apply): (choice=High-frequency oscillatory ventilation (HFOV))',
 'If yes (check all that apply): (choice=Inhaled nitric oxide (iNO))',
 'If yes (check all that apply): (choice=Invasive support with mechanical ventilation)',
 'If yes (check all that apply): (choice=Neuromuscular blocking agents)',
 'If yes (check all that apply): (choice=Non-invasive cannula/mask support)',
 'If yes (check all that apply): (choice=Non-invasive support via High-flow nasal cannula (HFNC))',
 'If yes (check all that apply): (choice=Non-invasive ventilation CPAP/BPAP)',
 'If yes (check all that apply): (choice=Other(s), specify)',
 'If yes (check all that apply): (choice=Prone positioning)',
 'If yes (check all that apply): (choice=Tracheostomy)',
 'If yes (check all that apply): (choice=Vasopressor/inotropic support)',
 'If yes: (choice=Blood transfusion)',
 'If yes: (choice=Dialysis or hemofiltration)',
 'If yes: (choice=Extracorporeal membrane oxygenation (ECMO))',
 'If yes: (choice=High-flow nasal cannula (HFNC))',
 'If yes: (choice=High-frequency oscillatory ventilation)',
 'If yes: (choice=Inhaled nitric oxide (iNO))',
 'If yes: (choice=Invasive with mechanical ventilation)',
 'If yes: (choice=Neuromuscular blocking agents)',
 'If yes: (choice=Non-invasive ventilation CPAP/BPAP)',
 'If yes: (choice=Other(s), (specify))',
 'If yes: (choice=Oxygen therapy with cannula/mask)',
 'If yes: (choice=Prone positioning)',
 'If yes: (choice=Tracheostomy)',
 'If yes: (choice=Vasopressor/inotropic support)',
 'On arrival,  is the participant receiving oxygen ?',
'Oxygen therapy',
'Please specify drugs used. (choice=Amphetamines)',
 'Please specify drugs used. (choice=Cannabis)',
 'Please specify drugs used. (choice=Cocaine)',
 'Please specify drugs used. (choice=Opiods)',
 'Please specify drugs used. (choice=Other)',
'Systemic corticosteroid?',
 'Treatments administered: (choice=Antifungal)',
 'Treatments administered: (choice=Azithromycin (Zithromax))',
 'Treatments administered: (choice=Colchicine)',
 'Treatments administered: (choice=Hydroxychloroquine (Plaquenil))',
 'Treatments administered: (choice=IVIG)',
 'Treatments administered: (choice=Interferon alpha)',
 'Treatments administered: (choice=Interferon beta)',
 'Treatments administered: (choice=Ivermectin (Stromectol))',
 'Treatments administered: (choice=Kineret (Anakinra))',
 'Treatments administered: (choice=Lopinavir/Ritonavir (Kaletra))',
 'Treatments administered: (choice=Neuraminidase inhibitor)',
 'Treatments administered: (choice=Other COVID-19 treatments (specify))',
 'Treatments administered: (choice=Other antibiotic (specify))',
 'Treatments administered: (choice=Other antiviral (specify))',
 'Treatments administered: (choice=Other immunomodulator (specify))',
 'Treatments administered: (choice=Plasma)',
 'Treatments administered: (choice=Remdesivir)',
 'Treatments administered: (choice=Ribavirin)',
 'Treatments administered: (choice=Sarilumab (Kevzara))',
 'Treatments administered: (choice=Stem cells)',
 'Treatments administered: (choice=Systematic corticosteroid)',
 'Treatments administered: (choice=Tocilizumab (Actemra))',
'Ventilatory support:'
]
lab_results=[
'Albumin (LOWEST value)',
'Albumin:',
 'At the time of collection, FiO2:',
 'At the time of collection, SpO2 on oxygen:',
 'At the time of collection, is the participant receiving oxygen ?',
'ACE inhibitor or Angiotensin Receptor Blocker?',
 'ALT (HIGHEST value)',
 'ALT:',
 'APTT (activated partial thromboplastin time) (HIGHEST value)',
 'APTT (activated partial thromboplastin time):',
 'AVPU Scale:',
 'Baseline creatinine:',
 'Basophil (relative value) (HIGHEST value)',
 'Basophil (relative value):',
 'Basophil (x 10^9/L):',
 'C-reactive protein (CRP) (HIGHEST value)',
 'C-reactive protein (CRP):',
 'Creatinine (HIGHEST value)',
 'Creatinine:',
 'D-Dimer (HIGHEST value)',
 'D-Dimer:',
 'Diastolic BP:',
 'Diastolic BP:.1',
 'Eosinophil (relative value)',
 'Eosinophil (relative value) (HIGHEST value)',
 'Eosinophil (x 10^9/L):',
 'FiO2 (associated with the previous SpO2):',
 'Glasgow Coma Scale (GCS) - lowest value:',
 'Glucose (HIGHEST value)',
 'Glucose:',
 'Haemoglobin (LOWEST value)',
 'Haemoglobin :',
 'Heart rate (associated with BP above):',
 'Heart rate (associated with BP above):.1',
 'Immunosupressed state?',
 'International Normalized Ratio (INR) (HIGHEST value)',
 'International Normalized Ratio (INR):',
 'LDH (HIGHEST value)',
 'LDH:',
 'Lymphocyte (relative value) (LOWEST value)',
 'Lymphocyte (relative value):',
 'Lymphocyte (x 10^9/L):',
 'Monocyte (relative valeur) (HIGHEST value)',
 'Monocyte (relative value):',
 'Monocyte (x 10^9/L):',
 'Neutrophil (relative value) (HIGHEST value)',
 'Neutrophil (x 10^9/L):',
 'Neutrophils (relative value):',
 'O2 saturation at room air :',
 'O2 saturation at room air :.1',
 'On arrival, SpO2 on oxygen:',
 'Platelet (LOWEST value)',
 'Platelets:',
'Positive bacterial culture documented during hospitalization?',
 'Positive viral infection documented during hospitalization:',
 'Potassium K+ (HIGHEST value)',
 'Potassium K+:',
 'Procalcitonin (PCT):',
 'Respiratory rate (associated with BP above):',
 'Respiratory rate (associated with BP above):.1',
 'Sodium Na+ (HIGHEST value)',
 'Sodium Na+:',
 'SpO2 (the lowest associated with the highest support):',
 'Systolic BP:',
 'Systolic BP:.1',
 'Temperature:',
 'Temperature:.1',
 'Total Bilirubin:',
 'Total WBC count (HIGHEST value) ',
 'Total WBC count:',
 'Total bilirubin (HIGHEST value)',
 'Urea (HIGHEST value)',
 'Urea:'
]
symptom_list=[
    'Asymptomatic?',
    'Joint pain (Arthralgia) ?',
    'Confusion / altered mental status ?',
    'Red eye (Conjunctivitis) ?',
    'Seizure ?',
    'Diarrhea ?',
    'Abdominal pain ?',
    'Chest pain ?',
    'Shortness of breath (Dyspnea) ?',
    'Dizziness ?',
    'Extremity weakness or numbness ?',
    'Fatigue ?',
    'Fever (?38.0 Celcius) ?',
    'Hemoptysis / Bloody sputum ?',
    'Loss of appetite ?',
    'Ear pain ?',
    'Sore throat ?',
    'Headache ?',
    'Muscle aches (Myalgia) ?',
    'Nausea / vomiting ?',
    'Leg swelling (Edema) ?',
    'Loss of taste / lost of smell ?',
    'Skin rash ?',
    'Runny nose (Rhinorrhea) ?',
    'Wheezing or stridor ?',
    'Cough ?',
    'Trouble speaking (Aphasia / Dysphasia) ?',
]
followup_symptom_list=[
    'Joint pain (Arthralgia) ?.1',
    'Confusion / altered mental status ?.1',
    'Red eye (Conjunctivitis) ?.1',
    'Seizure ?.1',
    'Diarrhea ?.1',
    'Abdominal pain ?.1',
    'Chest pain ?.1',
    'Shortness of breath (Dyspnea) ?.1',
    'Dizziness ?.1',
    'Extremity weakness or numbness ?.1',
    'Fatigue ?.1',
    'Fever (?38.0 Celcius) ?.1',
    'Hemoptysis / Bloody sputum ?.1',
    'Loss of appetite ?.1',
    'Ear pain ?.1',
    'Sore throat ?.1',
    'Headache ?.1',
    'Muscle aches (Myalgia) ?.1',
    'Nausea / vomiting ?.1',
    'Leg swelling (Edema) ?.1',
    'Loss of taste / lost of smell ?.1',
    'Skin rash ?.1',
    'Runny nose (Rhinorrhea) ?.1',
    'Wheezing or stridor ?.1',
    'Cough ?.1',
    'Trouble speaking (Aphasia / Dysphasia) ?.1'
]
comorbidity_list=[
    'Prior transient ischemic attack (TIA) ?',
    'Asthma ?',
    'Other chronic cardiac disease ?',
    'Other chronic neurological disorder (other than stroke/TIA) ?',
    'Other chronic lung disease ? ',
    'Prior stroke ? ',
    'Malignant neoplasm ?',
    'Dementia ? ',
    'Diabetes ?',
    'Atrial fibrillation or flutter ?',
    'HIV or AIDS ?',
    'Arterial Hypertension ?',
    'Pulmonary hypertension ?',
    'Immunosupressed state?',
    'Prior myocardial infarction ?',
    'Heart failure ?',
    'Coronary artery disease ?',
    'Chronic hematologic disease ?',
    'Liver disease ?',
    'Malnutrition ?',
    'COPD (emphysema, chronic bronchitis) ?',
    'Obesity ?',
    'Psychiatric disease?',
    'Chronic kidney disease ?',
    'Rheumatologic disease ?',
    'Does the patient have other comorbidities?',
    'Acute Respiratory Distress Syndrome (ARDS)?',
'Acute kidney injury?',
'Anemia?',
'Anxiety and depression:',
'Bacteremia?',
'Bacterial pneumonia?',
'Breathlessness:',
'Bronchiolitis?',
'Cardiac arrest?',
'Coronary angiography (Cardiac catheterization)?',
'Cryptogenic organizing pneumonia (COP)?',
'Decompensated heart failure?',
'Deep vein thrombosis (DVT)?',
'Disseminated intravascular coagulation (DIC)?',
'Endocarditis? ',
'Gastrointestinal haemorrhage?',
'Liver dysfunction?',
'Malignant neoplasm - actively receiving treatment?',
'Malignant neoplasm - metastatic?',
'Meningitis or encephalitis?',
    'Myocarditis?',
'New atrial fibrillation or flutter (AF)?',
'Non-ST-elevation myocardial infarction (NSTEMI)? ',
'Number of comorbidities: ',
'Number of other comorbidities: ',
'Number of other complications: ',
'Other cardiac arrhythmia?',
'Other immunosuppressive medications?',
'Pancreatitis?',
'Pericarditis?',
'Pleural effusion?',
'Pneumothorax?',
'Rhabdomyolysis or myositis?',
'ST-elevation myocardial infarction (STEMI)?',
'Has the participant had any new disease and/or worsening and/or deterioration of a pre-existing disease?',
'Hyperglycemia?',
'Hypoglycemia?',
'Seizure?',
'Severity of COPD:',
'Stroke?',
'TIA?',
'Ventricular tachycardia or fibrillation (VT/VF)?',
'Viral pneumonia/pneumonitis?'
]
others=[
    'Ability to self-care at discharge versus pre-COVID:',
'Disposition:',
'Does the participant report persistent symptoms related to SARS-CoV-2 infection?',
'Duration of hospitalization:',
'Emergency visit only?',
'How many times have you fallen in the past year?',
'How much difficulty do you have climbing a flight of 10 stairs?',
'How much difficulty do you have lifting or carrying 10 lbs?',
'How much difficulty do you have transferring from a chair to a bed?',
'How much difficulty do you have walking across a room?',
'How would you rate your current level of functioning? See options above.',
'ICU admission?',
'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?',
'If yes, specify virus: (choice=Adenovirus)',
'If yes, specify virus: (choice=Influenza)',
'If yes, specify virus: (choice=Metapneumovirus)',
'If yes, specify virus: (choice=Other, specify)',
'If yes, specify virus: (choice=Parainfluenza)',
'If yes, specify virus: (choice=RSV)',
'If yes, specify virus: (choice=Rhinovirus/enterovirus)',
'Level of care (final):',
'Long Covid',
'Mobility',
'Pain and discomfort:',
'Self-care',
'Usual activities, including work, study, housework, family or leisure activities:',
'Vital status at discharge:',
'Vital status:'
]
'''

demographic=[ 'Age au recrutement',
'Age au recrutement:',
 'BMI:',
'Electronic cigarettes?',
'Height in m:',
'Living where?',
'Living with?',
 'Is the participant employed as a Healthcare Worker?  ',
 'Is the participant employed in a Microbiology Laboratory?  ',
'Patient pregnant?',
 'Sex at birth:',
 'Sexe:',
 'Smoking status:',
'Weight in kg:',
]
treatment=[
'Anticoagulants?',
'Adjunctive therapy during hospitalization',
'Colchicine?',
 'Dialysis ?',
'Did or does the patient receive adjunctive therapy?',
 'Did or does the patient receive ventilatory support?',
'Drugs?',
'HGO or insulin?',
 'If yes (check all that apply): (choice=Blood transfusion)',
 'If yes (check all that apply): (choice=Dialysis or hemofiltration)',
 'If yes (check all that apply): (choice=Extracorporeal membrane oxygenation (ECMO))',
 'If yes (check all that apply): (choice=High-frequency oscillatory ventilation (HFOV))',
 'If yes (check all that apply): (choice=Inhaled nitric oxide (iNO))',
 'If yes (check all that apply): (choice=Invasive support with mechanical ventilation)',
 'If yes (check all that apply): (choice=Neuromuscular blocking agents)',
 'If yes (check all that apply): (choice=Non-invasive cannula/mask support)',
 'If yes (check all that apply): (choice=Non-invasive support via High-flow nasal cannula (HFNC))',
 'If yes (check all that apply): (choice=Non-invasive ventilation CPAP/BPAP)',
 'If yes (check all that apply): (choice=Other(s), specify)',
 'If yes (check all that apply): (choice=Prone positioning)',
 'If yes (check all that apply): (choice=Tracheostomy)',
 'If yes (check all that apply): (choice=Vasopressor/inotropic support)',
 'If yes: (choice=Blood transfusion)',
 'If yes: (choice=Dialysis or hemofiltration)',
 'If yes: (choice=Extracorporeal membrane oxygenation (ECMO))',
 'If yes: (choice=High-flow nasal cannula (HFNC))',
 'If yes: (choice=High-frequency oscillatory ventilation)',
 'If yes: (choice=Inhaled nitric oxide (iNO))',
 'If yes: (choice=Invasive with mechanical ventilation)',
 'If yes: (choice=Neuromuscular blocking agents)',
 'If yes: (choice=Non-invasive ventilation CPAP/BPAP)',
 'If yes: (choice=Other(s), (specify))',
 'If yes: (choice=Oxygen therapy with cannula/mask)',
 'If yes: (choice=Prone positioning)',
 'If yes: (choice=Tracheostomy)',
 'If yes: (choice=Vasopressor/inotropic support)',
 'On arrival,  is the participant receiving oxygen ?',
'Oxygen therapy',
'Please specify drugs used. (choice=Amphetamines)',
 'Please specify drugs used. (choice=Cannabis)',
 'Please specify drugs used. (choice=Cocaine)',
 'Please specify drugs used. (choice=Opiods)',
 'Please specify drugs used. (choice=Other)',
'Systemic corticosteroid?',
 'Treatments administered: (choice=Antifungal)',
 'Treatments administered: (choice=Azithromycin (Zithromax))',
 'Treatments administered: (choice=Colchicine)',
 'Treatments administered: (choice=Hydroxychloroquine (Plaquenil))',
 'Treatments administered: (choice=IVIG)',
 'Treatments administered: (choice=Interferon alpha)',
 'Treatments administered: (choice=Interferon beta)',
 'Treatments administered: (choice=Ivermectin (Stromectol))',
 'Treatments administered: (choice=Kineret (Anakinra))',
 'Treatments administered: (choice=Lopinavir/Ritonavir (Kaletra))',
 'Treatments administered: (choice=Neuraminidase inhibitor)',
 'Treatments administered: (choice=Other COVID-19 treatments (specify))',
 'Treatments administered: (choice=Other antibiotic (specify))',
 'Treatments administered: (choice=Other antiviral (specify))',
 'Treatments administered: (choice=Other immunomodulator (specify))',
 'Treatments administered: (choice=Plasma)',
 'Treatments administered: (choice=Remdesivir)',
 'Treatments administered: (choice=Ribavirin)',
 'Treatments administered: (choice=Sarilumab (Kevzara))',
 'Treatments administered: (choice=Stem cells)',
 'Treatments administered: (choice=Systematic corticosteroid)',
 'Treatments administered: (choice=Tocilizumab (Actemra))',
'Ventilatory support:'
]
lab_results=[
'Albumin (LOWEST value)',
'Albumin:',
 'At the time of collection, FiO2:',
 'At the time of collection, SpO2 on oxygen:',
 'At the time of collection, is the participant receiving oxygen ?',
'ACE inhibitor or Angiotensin Receptor Blocker?',
 'ALT (HIGHEST value)',
 'ALT:',
 'APTT (activated partial thromboplastin time) (HIGHEST value)',
 'APTT (activated partial thromboplastin time):',
 'AVPU Scale:',
 'Baseline creatinine:',
 'Basophil (relative value) (HIGHEST value)',
 'Basophil (relative value):',
 'Basophil (x 10^9/L):',
 'C-reactive protein (CRP) (HIGHEST value)',
 'C-reactive protein (CRP):',
 'Creatinine (HIGHEST value)',
 'Creatinine:',
 'D-Dimer (HIGHEST value)',
 'D-Dimer:',
 'Diastolic BP:',
 'Diastolic BP:.1',
 'Eosinophil (relative value)',
 'Eosinophil (relative value) (HIGHEST value)',
 'Eosinophil (x 10^9/L):',
 'FiO2 (associated with the previous SpO2):',
 'Glasgow Coma Scale (GCS) - lowest value:',
 'Glucose (HIGHEST value)',
 'Glucose:',
 'Haemoglobin (LOWEST value)',
 'Haemoglobin :',
 'Heart rate (associated with BP above):',
 'Heart rate (associated with BP above):.1',
 'Immunosupressed state?',
 'International Normalized Ratio (INR) (HIGHEST value)',
 'International Normalized Ratio (INR):',
 'LDH (HIGHEST value)',
 'LDH:',
 'Lymphocyte (relative value) (LOWEST value)',
 'Lymphocyte (relative value):',
 'Lymphocyte (x 10^9/L):',
 'Monocyte (relative valeur) (HIGHEST value)',
 'Monocyte (relative value):',
 'Monocyte (x 10^9/L):',
 'Neutrophil (relative value) (HIGHEST value)',
 'Neutrophil (x 10^9/L):',
 'Neutrophils (relative value):',
 'O2 saturation at room air :',
 'O2 saturation at room air :.1',
 'On arrival, SpO2 on oxygen:',
 'Platelet (LOWEST value)',
 'Platelets:',
'Positive bacterial culture documented during hospitalization?',
 'Positive viral infection documented during hospitalization:',
 'Potassium K+ (HIGHEST value)',
 'Potassium K+:',
 'Procalcitonin (PCT):',
 'Respiratory rate (associated with BP above):',
 'Respiratory rate (associated with BP above):.1',
 'Sodium Na+ (HIGHEST value)',
 'Sodium Na+:',
 'SpO2 (the lowest associated with the highest support):',
 'Systolic BP:',
 'Systolic BP:.1',
 'Temperature:',
 'Temperature:.1',
 'Total Bilirubin:',
 'Total WBC count (HIGHEST value) ',
 'Total WBC count:',
 'Total bilirubin (HIGHEST value)',
 'Urea (HIGHEST value)',
 'Urea:'
]
symptom_list=[
    'Asymptomatic?',
    'Joint pain (Arthralgia) ?',
    'Confusion / altered mental status ?',
    'Red eye (Conjunctivitis) ?',
    'Seizure ?',
    'Diarrhea ?',
    'Abdominal pain ?',
    'Chest pain ?',
    'Shortness of breath (Dyspnea) ?',
    'Dizziness ?',
    'Extremity weakness or numbness ?',
    'Fatigue ?',
    'Fever (?38.0 Celcius) ?',
    'Hemoptysis / Bloody sputum ?',
    'Loss of appetite ?',
    'Ear pain ?',
    'Sore throat ?',
    'Headache ?',
    'Muscle aches (Myalgia) ?',
    'Nausea / vomiting ?',
    'Leg swelling (Edema) ?',
    'Loss of taste / lost of smell ?',
    'Skin rash ?',
    'Runny nose (Rhinorrhea) ?',
    'Wheezing or stridor ?',
    'Cough ?',
    'Trouble speaking (Aphasia / Dysphasia) ?',
]
followup_symptom_list=[
    'Joint pain (Arthralgia) ?.1',
    'Confusion / altered mental status ?.1',
    'Red eye (Conjunctivitis) ?.1',
    'Seizure ?.1',
    'Diarrhea ?.1',
    'Abdominal pain ?.1',
    'Chest pain ?.1',
    'Shortness of breath (Dyspnea) ?.1',
    'Dizziness ?.1',
    'Extremity weakness or numbness ?.1',
    'Fatigue ?.1',
    'Fever (?38.0 Celcius) ?.1',
    'Hemoptysis / Bloody sputum ?.1',
    'Loss of appetite ?.1',
    'Ear pain ?.1',
    'Sore throat ?.1',
    'Headache ?.1',
    'Muscle aches (Myalgia) ?.1',
    'Nausea / vomiting ?.1',
    'Leg swelling (Edema) ?.1',
    'Loss of taste / lost of smell ?.1',
    'Skin rash ?.1',
    'Runny nose (Rhinorrhea) ?.1',
    'Wheezing or stridor ?.1',
    'Cough ?.1',
    'Trouble speaking (Aphasia / Dysphasia) ?.1'
]
comorbidity_list=[
    'Prior transient ischemic attack (TIA) ?',
    'Asthma ?',
    'Other chronic cardiac disease ?',
    'Other chronic neurological disorder (other than stroke/TIA) ?',
    'Other chronic lung disease ? ',
    'Prior stroke ? ',
    'Malignant neoplasm ?',
    'Dementia ? ',
    'Diabetes ?',
    'Atrial fibrillation or flutter ?',
    'HIV or AIDS ?',
    'Arterial Hypertension ?',
    'Pulmonary hypertension ?',
    'Immunosupressed state?',
    'Prior myocardial infarction ?',
    'Heart failure ?',
    'Coronary artery disease ?',
    'Chronic hematologic disease ?',
    'Liver disease ?',
    'Malnutrition ?',
    'COPD (emphysema, chronic bronchitis) ?',
    'Obesity ?',
    'Psychiatric disease?',
    'Chronic kidney disease ?',
    'Rheumatologic disease ?',
    'Does the patient have other comorbidities?',
    'Acute Respiratory Distress Syndrome (ARDS)?',
'Acute kidney injury?',
'Anemia?',
'Anxiety and depression:',
'Bacteremia?',
'Bacterial pneumonia?',
'Breathlessness:',
'Bronchiolitis?',
'Cardiac arrest?',
'Coronary angiography (Cardiac catheterization)?',
'Cryptogenic organizing pneumonia (COP)?',
'Decompensated heart failure?',
'Deep vein thrombosis (DVT)?',
'Disseminated intravascular coagulation (DIC)?',
'Endocarditis? ',
'Gastrointestinal haemorrhage?',
'Liver dysfunction?',
'Malignant neoplasm - actively receiving treatment?',
'Malignant neoplasm - metastatic?',
'Meningitis or encephalitis?',
    'Myocarditis?',
'New atrial fibrillation or flutter (AF)?',
'Non-ST-elevation myocardial infarction (NSTEMI)? ',
'Number of comorbidities: ',
'Number of other comorbidities: ',
'Number of other complications: ',
'Other cardiac arrhythmia?',
'Other immunosuppressive medications?',
'Pancreatitis?',
'Pericarditis?',
'Pleural effusion?',
'Pneumothorax?',
'Rhabdomyolysis or myositis?',
'ST-elevation myocardial infarction (STEMI)?',
'Has the participant had any new disease and/or worsening and/or deterioration of a pre-existing disease?',
'Hyperglycemia?',
'Hypoglycemia?',
'Seizure?',
'Severity of COPD:',
'Stroke?',
'TIA?',
'Ventricular tachycardia or fibrillation (VT/VF)?',
'Viral pneumonia/pneumonitis?'
]
others=[
    'Ability to self-care at discharge versus pre-COVID:',
'Disposition:',
'Does the participant report persistent symptoms related to SARS-CoV-2 infection?',
'Duration of hospitalization:',
'Emergency visit only?',
'How many times have you fallen in the past year?',
'How much difficulty do you have climbing a flight of 10 stairs?',
'How much difficulty do you have lifting or carrying 10 lbs?',
'How much difficulty do you have transferring from a chair to a bed?',
'How much difficulty do you have walking across a room?',
'How would you rate your current level of functioning? See options above.',
'ICU admission?',
'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?',
'If yes, specify virus: (choice=Adenovirus)',
'If yes, specify virus: (choice=Influenza)',
'If yes, specify virus: (choice=Metapneumovirus)',
'If yes, specify virus: (choice=Other, specify)',
'If yes, specify virus: (choice=Parainfluenza)',
'If yes, specify virus: (choice=RSV)',
'If yes, specify virus: (choice=Rhinovirus/enterovirus)',
'Level of care (final):',
'Long Covid',
'Mobility',
'Pain and discomfort:',
'Self-care',
'Usual activities, including work, study, housework, family or leisure activities:',
'Vital status at discharge:',
'Vital status:'
]


#G = nx.read_gpickle("koinetwork.gpickle")
G1 = pd.read_pickle("sev_cov_nx.pickle")
severity = 'If a screening test for SARS-CoV-2 by PCR was performed, what is the most severe severity level (according to WHO) achieved?'
canvas_button1 = dbc.Button(
                    "Customize layout", id="open-offcanvas1", n_clicks=0, color='dark'
                )

stylesheet11 = []
for x in G1.nodes:
    if x in symptom_list:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    elif x in followup_symptom_list:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    elif x in comorbidity_list:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    elif x == severity:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'width' : 10,
                    'height' : 10,
                    'background-color': 'yellow',
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'pentagon'
                }
            }
        )
    elif x in demographic:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    elif x in treatment:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    elif x in lab_results:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )
    else:
        stylesheet11.append(
            {
                'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node',
                'style': {
                    'background-color': 'blue',
                    'width': 10,
                    'height': 10,
                    'background-opacity': 0.8,
                    'border-width': 0.5,
                    'shape': 'circle'
                }
            }
        )


for x in G1.edges:
    stylesheet11.append(
        {
            'selector': '.' + re.sub(r'[^a-zA-Z0-9]', '', x[0]) + re.sub(r'[^a-zA-Z0-9]', '', x[1]) + 'Edge',
            'style': {
                'width': 0.5,
                'line-color': 'gray',
                'line-opacity': 0.8,
                'target-arrow-shape': 'triangle',
                'target-arrow-color' : 'gray',
                'arrow-scale' : 1
            }
        }
    )

stylesheet11.append({
    'selector' : 'node',
    'style' : {
        'font-weight' : 'bolder',
        #'font-size' : 6,
        'text-wrap' : 'ellipsis',
        'text-max-width' : 500,
        'text-background-color' : 'blue'
    }
})

stylesheet11.append({
                'selector': 'edge',
                'style': {
                    # The default curve style does not work with certain arrows
                    'curve-style': 'bezier'
                }
            })

node_elements1 = []
for x in G1.nodes:
    if x in symptom_list:
        node_elements1.append({'data': {'id': x, 'label': 'symptom_list'}, 'selectable': False, 'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x in followup_symptom_list:
        node_elements1.append({'data': {'id': x, 'label': 'followup_symptom_list'}, 'selectable': False,'classes' : re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x in comorbidity_list:
        node_elements1.append({'data': {'id': x, 'label': 'comorbidity_list'}, 'selectable': False, 'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x == severity:
        node_elements1.append({'data': {'id': x, 'label': 'severity'}, 'selectable': False, 'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x in demographic:
        node_elements1.append({'data': {'id': x, 'label': 'demographic'}, 'selectable': False,'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x in treatment:
        node_elements1.append({'data': {'id': x, 'label': 'treatment'}, 'selectable': False,'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    elif x in lab_results:
        node_elements1.append({'data': {'id': x, 'label': 'lab_results'}, 'selectable': False,'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})
    else:
        node_elements1.append({'data': {'id': x, 'label': 'others'}, 'selectable': False,'classes': re.sub(r'[^a-zA-Z0-9]', '', x) + 'Node'})


edge_elements1 = [
                    # Edge elements
                    {'data': {'id':re.sub(r'[^a-zA-Z0-9]', '', x[0]) + re.sub(r'[^a-zA-Z0-9]', '', x[1]) + 'Edge','source': x[0], 'target': x[1]},'selectable': False, 'classes' : re.sub(r'[^a-zA-Z0-9]', '', x[0]) + re.sub(r'[^a-zA-Z0-9]', '', x[1]) + 'Edge'} for x in G1.edges
]


graph_path1 = {}
for node in G1.nodes:
    graph_path1[node] = []
    for edge in G1.edges:
        if edge[0] == node:
            graph_path1[node].append(edge[1])



def shortest_path1(graph, node1, node2):
    path_list = [[node1]]
    path_index = 0
    # To keep track of previously visited nodes
    previous_nodes = {node1}
    if node1 == node2:
        return path_list[0]

    while path_index < len(path_list):
        current_path = path_list[path_index]
        last_node = current_path[-1]
        next_nodes = graph[last_node]
        # Search goal node
        if node2 in next_nodes:
            current_path.append(node2)
            return current_path
        # Add new paths
        for next_node in next_nodes:
            if not next_node in previous_nodes:
                new_path = current_path[:]
                new_path.append(next_node)
                path_list.append(new_path)
                # To avoid backtracking
                previous_nodes.add(next_node)
        # Continue to next path in list
        path_index += 1
    # No path is found
    return []

graph1 = cyto.Cytoscape(
            id='org-chart1',
            autoungrabify=False,
            minZoom=0.5,
            maxZoom=4,
            #zoom= 1,
            zoomingEnabled=True,
            userZoomingEnabled=True,
            style={'width': '95%', 'height': '1000px'},
            userPanningEnabled= False,
            #layout={'name': 'cola','fit':True},
            stylesheet= stylesheet11,
            elements= node_elements1 + edge_elements1
            )

layout = html.Div([canvas_button1,graph1])

stylesheet_copy1 = copy.deepcopy(stylesheet11)
stylesheet_hover1 = copy.deepcopy(stylesheet11)
#print(stylesheet_hover)


@app.callback(Output('org-chart1', 'stylesheet'),
              Input('submit-button-state1', 'n_clicks'),
              Input('customize-button-state11', 'n_clicks'),
              Input('org-chart1', 'mouseoverNodeData'),
              State('choose-inference11', 'value'),
               State('choose-color11', 'value'),
               State('choose-shape11', 'value'),
               State('dropdown1', 'value')
              )
def update_stylesheet(n_clicks,n_clicks1,hover,type1,color1,shape1,dropdown):
        button_id = dash.callback_context.triggered[0]['prop_id'].split('.')[0]
        if button_id ==  'submit-button-state1' and n_clicks:
            stylesheet_copy_copy1 = copy.deepcopy(stylesheet_copy1)
            for selector in stylesheet_hover1:
                if 'line-color' in selector['style'] and selector['style']['line-color'] == 'orange':
                    selector['style']['target-arrow-color'] = 'gray'
                    selector['style']['line-color'] = 'gray'
                elif 'background-color' in selector['style'] and 'shape' in selector['style'] and selector['style']['background-color'] == 'orange' and selector['style']['shape'] == 'pentagon' and selector['selector'] != '.' + re.sub(r'[^a-zA-Z0-9]', '', severity) + 'Node':
                    for selector1 in stylesheet_copy_copy1:
                        if selector1['selector'] == selector['selector']:
                            selector['style']['background-color'] = selector1['style']['background-color']
                            selector['style']['shape'] = selector1['style']['shape']
            path = shortest_path1(graph_path1, str(dropdown), severity)
            for idx, node in enumerate(path):
                if idx < len(path) - 1:
                    for edge in edge_elements1:
                        if edge['data']['source'] == node and edge['data']['target'] == path[idx + 1]:
                            for selector in stylesheet_copy_copy1:
                                if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', node) + re.sub(r'[^a-zA-Z0-9]','', path[idx + 1]) + 'Edge':
                                    selector['style']['line-color'] = 'orange'
                                    selector['style']['target-arrow-color'] = 'orange'
                            for selector in stylesheet_hover1:
                                if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', node) + re.sub(r'[^a-zA-Z0-9]','', path[idx + 1]) + 'Edge':
                                    selector['style']['line-color'] = 'orange'
                                    selector['style']['target-arrow-color'] = 'orange'
                for node1 in node_elements1:
                    if node1['data']['id'] == node:
                        id = node1['data']['id']
                        for selector in stylesheet_copy_copy1:
                            if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                                selector['style']['background-color'] = 'orange'
                                selector['style']['shape'] = 'pentagon'
                        for selector in stylesheet_hover1:
                            if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                                selector['style']['background-color'] = 'orange'
                                selector['style']['shape'] = 'pentagon'

            return stylesheet_copy_copy1
        elif button_id ==  'customize-button-state11' and n_clicks1:
            for selector in stylesheet_hover1:
                if 'line-color' in selector['style'] and selector['style']['line-color'] == 'orange':
                    selector['style']['line-color'] = 'gray'
                    selector['style']['target-arrow-color'] = 'gray'
                elif 'background-color' in selector['style'] and 'shape' in selector['style'] and selector['style']['background-color'] == 'orange' and selector['style']['shape'] == 'pentagon' and selector['selector'] != '.' + re.sub(r'[^a-zA-Z0-9]', '', severity) + 'Node':
                    for selector1 in stylesheet_copy1:
                        if selector1['selector'] == selector['selector']:
                            selector['style']['background-color'] = selector1['style']['background-color']
                            selector['style']['shape'] = selector1['style']['shape']
            for node in node_elements1:
                if node['data']['label'] == type1:
                    id = node['data']['id']
                    for selector in stylesheet_copy1:
                        if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                            selector['style']['background-color'] = color1
                            selector['style']['shape'] = shape1
                    for selector in stylesheet_hover1:
                        if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                            selector['style']['background-color'] = color1
                            selector['style']['shape'] = shape1
            return stylesheet_copy1
        elif hover:
            stylesheet_copy_copy1 = copy.deepcopy(stylesheet_hover1)
            id =  hover['id']
            for selector in stylesheet_copy_copy1:
                if selector['selector'] == '.' + re.sub(r'[^a-zA-Z0-9]', '', id) + 'Node':
                    if id == severity:
                        selector['style']['label'] = 'severity'
                    else:
                        selector['style']['label'] = id
            return stylesheet_copy_copy1
        else:
            return stylesheet_copy1

'''
@app.callback(
    Output(component_id='my_output1-1', component_property='children'),
    Input('submit-button-state1', 'n_clicks'),
    State('dropdown1', 'value'))
def update_probability(n_clicks,dropdown):   
    
    p = random.randint(0,1)
    return f'Probability: {p}'
'''
'''
@app.callback(
    Output('dropdown1', 'value'),
    [Input('clear-button-state', "n_clicks")])
def clear(n_clicks):
    return []
'''

@app.callback(
    Output('org-chart1','layout'),
    Input('customize-button-state21','n_clicks'),
    State('choose-layout','value')
)
def update_layout(n_clicks,value):
    return {'name': value,'fit':True,'animate': True}