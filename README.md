# FHIR & DICOM in Python

This repository serves as a pedagogical resource for healthcare data interoperability, focusing on the two most critical standards in modern health informatics: **FHIR** and **DICOM**.

---

## 🏥 1. FHIR (Fast Healthcare Interoperability Resources)

### Overview
**FHIR** (pronounced "fire") is a standard developed by HL7 (Health Level Seven International). It is designed to facilitate the exchange of electronic health records (EHR) using modern web technologies.

### Key Concepts
- **Resources**: The fundamental unit of FHIR. Everything is a resource (e.g., `Patient`, `Observation`, `MedicationRequest`).
- **RESTful API**: FHIR is built on top of HTTP. You use standard verbs (`GET`, `POST`, `PUT`, `DELETE`) to interact with data.
- **Serialization**: Data is typically represented in **JSON** or **XML**.
- **Extensions**: A standard way to add custom data fields without breaking compatibility.

### 🔄 FHIR Transcoding & Mapping
In an industrial setting, data often arrives in legacy formats (like HL7 v2 or custom CSVs). **Transcoding** in FHIR refers to the process of mapping these legacy structures into valid FHIR resources, ensuring semantic consistency across systems.

### 🚥 Multimodal Input in FHIR
FHIR handles multimodal clinical data through various resource types. For example:
- **Observation**: For lab results, vitals, or imaging metadata.
- **DiagnosticReport**: For summarizing complex clinical findings.
- **DocumentReference**: For linking to external files (like PDFs or DICOM images).

---

## 📸 2. DICOM (Digital Imaging and Communications in Medicine)

### Overview
**DICOM** is the universal standard for medical imaging. From X-rays to MRI scans, almost every medical image captured globally follows this standard.

### Anatomy of a DICOM File
Unlike a simple JPEG, a DICOM file (`.dcm`) is a "container" that includes:
- **Pixel Data**: The raw image data (often high-bit depth, e.g., 16-bit).
- **Metadata (Tags)**: Information about the Patient, the Study, the Series, and the Equipment (Modality).
- **Transfer Syntax**: Defines how the data is encoded (compressed vs. uncompressed, little-endian vs. big-endian).

### 🎞️ DICOM Transcoding
**Transcoding** in DICOM is the process of changing the **Transfer Syntax**. For example, converting a raw, uncompressed DICOM image into a JPEG Lossless compressed DICOM to save storage space while maintaining medical grade quality.

### 🌈 Multimodal Input (Imaging Modalities)
DICOM is inherently multimodal. The **Modality** tag (0008,0060) defines the type of equipment used:
- `CT`: Computed Tomography
- `MR`: Magnetic Resonance
- `US`: Ultrasound
- `DX`: Digital Radiography

---

## 🛠️ Industrial Setup: Step-by-Step

We follow an industry-standard workflow:
1. **Virtual Environments**: Using `fhirdicomvenv` to isolate dependencies.
2. **Git Workflow**: Developing in feature branches (`feature/topic-name`) and using "Pull Requests" for review.
3. **Python Stack**: Leveraging `pydicom` for imaging and `fhir.resources` for clinical data.

---

## 📘 Tutorial 1: FHIR Patient Basics (Input & Output)

In this first exercise, we demonstrate how to create a structured healthcare record from scratch.

### 📥 The Input (Python)
We use the `fhir.resources` library, which provides strictly validated models. 
- **Patient()**: The core class for patient data.
- **Identifier()**: Used for Medical Record Numbers (MRN). In a real hospital, this is how you link records across different databases.
- **HumanName()**: Handles complex name structures (official, nickname, maiden names).

### 📤 The Output (Standardized JSON)
When we call `patient.json()`, we are **Transcoding** our Python logic into a machine-readable format that any FHIR-compliant server (like Epic, Cerner, or HAPI FHIR) can understand.

#### Key JSON Fields:
- `"resourceType"`: Tells the receiving system that this is a Patient record.
- `"meta"`: Contains technical metadata (e.g., when the record was last touched).
- `"identifier"`: A list of IDs. Note that hospitals use **Systems** (URLs) to define the context of an ID.

---

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any changes.

## Contact
If you have any questions or suggestions, feel free to contact me at [Kaushik Manjunatha](https://www.linkedin.com/in/kaushik-manjunatha/)
