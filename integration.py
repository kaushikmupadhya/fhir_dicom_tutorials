import pydicom
from fhir.resources.imagingstudy import ImagingStudy, ImagingStudySeries, ImagingStudySeriesInstance
from fhir.resources.reference import Reference
import json
import os

def integrate_dicom_to_fhir(dicom_path, patient_id):
    """
    Industrial Approach: Linking DICOM to FHIR.
    This creates an 'ImagingStudy' resource which acts as the 'bridge' 
    between the clinical record (FHIR) and the image data (DICOM).
    """
    
    # 1. Read the DICOM file to get IDs
    ds = pydicom.dcmread(dicom_path)
    study_instance_uid = getattr(ds, 'StudyInstanceUID', '1.2.3.4.5')
    series_instance_uid = getattr(ds, 'SeriesInstanceUID', '1.2.3.4.5.1')
    sop_instance_uid = getattr(ds, 'SOPInstanceUID', '1.2.3.4.5.1.1')
    modality = ds.Modality

    # 2. Create the FHIR ImagingStudy Resource
    study = ImagingStudy()
    study.status = "available"
    study.subject = Reference(reference=f"Patient/{patient_id}")
    
    # Link the Study Instance UID (Global Unique ID for the scan)
    study.identifier = [{"system": "urn:dicom:uid", "value": f"urn:oid:{study_instance_uid}"}]
    
    # 3. Create a Series
    series = ImagingStudySeries()
    series.uid = series_instance_uid
    series.modality = {"code": modality}
    series.number = 1
    
    # 4. Create an Instance (The specific file)
    instance = ImagingStudySeriesInstance()
    instance.uid = sop_instance_uid
    instance.sopClass = {"code": "urn:oid:1.2.840.10008.5.1.4.1.1.2"} # CT Image Storage
    instance.number = 1
    
    series.instance = [instance]
    study.series = [series]
    
    # 5. Transcode to JSON
    study_json = study.json(indent=2)
    
    print(f"--- FHIR ImagingStudy for {modality} ---")
    print(study_json)
    
    output_path = f"examples/imaging_study_{modality.lower()}.json"
    with open(output_path, "w") as f:
        f.write(study_json)
    print(f"\n[SUCCESS] Linked DICOM to FHIR: {output_path}")

if __name__ == "__main__":
    # Integration Test: Link our created CT to Patient 12345
    ct_path = "examples/sample_ct.dcm"
    if os.path.exists(ct_path):
        integrate_dicom_to_fhir(ct_path, "12345")
    else:
        print("[ERROR] Run dicom_basics.py first to generate the sample image!")
