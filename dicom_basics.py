import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import datetime
import numpy as np
from PIL import Image
import os

def create_dummy_dicom(filename, modality="CT"):
    """
    Industrial Approach: Creating a DICOM file from scratch.
    This demonstrates Multimodal Input (modality parameter) and 
    the internal structure of a medical image.
    """
    
    # 1. Create File Meta Information
    file_meta = Dataset()
    file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.2' # CT Image Storage
    file_meta.MediaStorageSOPInstanceUID = "1.2.3"
    file_meta.ImplementationClassUID = "1.2.3.4"
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian # Initial Transfer Syntax

    # 2. Create the Dataset
    ds = FileDataset(filename, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # 3. Add Patient/Study Tags (The 'Metadata')
    ds.PatientName = "Doe^John"
    ds.PatientID = "12345" # Matches our FHIR record!
    ds.ContentDate = datetime.datetime.now().strftime('%Y%m%d')
    ds.ContentTime = datetime.datetime.now().strftime('%H%M%S.%f')
    
    # MODALITY: This is where we handle 'Multimodal Input'
    ds.Modality = modality 
    
    # 4. Image Pixel Data (16-bit industrial grade)
    # We create a simple gradient image
    pixel_data = np.arange(10000, dtype=np.uint16).reshape((100, 100))
    ds.Rows = 100
    ds.Columns = 100
    ds.BitsAllocated = 16
    ds.BitsStored = 16
    ds.HighBit = 15
    ds.PixelRepresentation = 0 # unsigned
    ds.SamplesPerPixel = 1
    ds.PixelData = pixel_data.tobytes()

    ds.save_as(filename)
    print(f"[SUCCESS] Created {modality} DICOM: {filename}")
    return ds

def transcode_dicom(input_filename, output_filename):
    """
    Industrial Approach: DICOM Transcoding.
    Converting between different Transfer Syntaxes (encodings).
    """
    ds = pydicom.dcmread(input_filename)
    
    # For this tutorial, we 'simulate' a transcoding step 
    # In a real app, you might compress the PixelData here
    print(f"--- Transcoding {input_filename} ---")
    print(f"Original Transfer Syntax: {ds.file_meta.TransferSyntaxUID.name}")
    
    # Save with a specific syntax (Transcoding)
    ds.is_little_endian = True
    ds.is_explicit_vr = True
    ds.save_as(output_filename)
    print(f"Transcoded to: {output_filename}")

if __name__ == "__main__":
    if not os.path.exists("examples"):
        os.makedirs("examples")
        
    # 1. Create Multimodal Inputs
    create_dummy_dicom("examples/sample_ct.dcm", modality="CT")
    create_dummy_dicom("examples/sample_mri.dcm", modality="MR")
    
    # 2. Test Transcoding
    transcode_dicom("examples/sample_ct.dcm", "examples/transcoded_ct.dcm")
