from fhir.resources.patient import Patient
from fhir.resources.humanname import HumanName
from fhir.resources.identifier import Identifier
import json

def create_patient():
    """
    Industrial Approach: Creating a FHIR Patient Resource.
    This demonstrates how healthcare data is structured into 'Resources'.
    """
    
    # 1. Initialize the Patient Resource
    patient = Patient()
    
    # 2. Add an Identifier (Industrial systems use MRN - Medical Record Number)
    identifier = Identifier()
    identifier.system = "http://hospital.org/fhir/mrn"
    identifier.value = "12345"
    patient.identifier = [identifier]
    
    # 3. Add a Name
    name = HumanName()
    name.family = "Doe"
    name.given = ["John", "Quincy"]
    name.use = "official"
    patient.name = [name]
    
    # 4. Set Gender and Birth Date
    patient.gender = "male"
    patient.birthDate = "1990-01-01"
    
    # 5. Multimodal/Metadata Context
    # In an industrial pipeline, we often tag resources with metadata
    # to indicate which system or 'modality' they originated from.
    if not patient.meta:
        from fhir.resources.meta import Meta
        patient.meta = Meta()
    patient.meta.lastUpdated = "2026-03-09T15:37:00Z"
    
    # 6. Transcoding to JSON (The standard exchange format)
    # This is 'Transcoding' from a Python Object to a JSON String
    patient_json = patient.json(indent=2)
    
    print("--- FHIR Patient Resource (JSON) ---")
    print(patient_json)
    
    # Save to file for the repo
    with open("examples/sample_patient.json", "w") as f:
        f.write(patient_json)
    print("\n[SUCCESS] Saved to examples/sample_patient.json")

if __name__ == "__main__":
    create_patient()
