import pydicom
import json
from fhir.resources.imagingstudy import ImagingStudy
import os

def extract_study_to_fhir(dicom_path):
    """
    Extracts StudyInstanceUID from a DICOM file and outputs a FHIR ImagingStudy skeleton.
    """
    if not os.path.exists(dicom_path):
        print(f"[ERROR] Connection failed: {dicom_path} not found.")
        return

    # 1. Read DICOM
    if os.path.exists(dicom_path):
        ds = pydicom.dcmread(dicom_path)
    else:
        print(f"[ERROR] File {dicom_path} does not exist.")
        return
    
    # 2. Extract Key IDs
    study_uid = getattr(ds, 'StudyInstanceUID', 'UNKNOWN')
    patient_id = getattr(ds, 'PatientID', 'UNKNOWN')
    modality = getattr(ds, 'Modality', 'UNKNOWN')

    # 3. Create FHIR Skeleton
    # Industrial Tip: Some FHIR versions/libraries require 'status' and 'subject' upfront
    study = ImagingStudy(
        status="available",
        subject={"reference": f"Patient/{patient_id}"}
    )
    
    study.identifier = [{"system": "urn:dicom:uid", "value": f"urn:oid:{study_uid}"}]
    
    # Simple JSON Transcoding
    res_json = study.json(indent=2)
    
    print(f"--- Extracted FHIR Identity for {modality} ---")
    print(res_json)
    
    return res_json

if __name__ == "__main__":
    # Test with our previously created CT
    extract_study_to_fhir("examples/sample_ct.dcm")
