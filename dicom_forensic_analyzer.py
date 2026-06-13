import os
import json
import pydicom
import hashlib
from datetime import datetime

def get_file_sha256(file_path):
    """Calculates SHA256 hash of a file for integrity verification."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

class DicomForensicAnalyzer:
    def __init__(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self.config = json.load(f)
        self.results = []
        self.anomalies = []
        self.discrepancy_table = []

    def analyze_file(self, file_path):
        """Analyzes a single DICOM file against forensic markers."""
        try:
            ds = pydicom.dcmread(file_path)
            
            # Extract core identification metadata
            metadata = {
                "file_path": file_path,
                "sha256": get_file_sha256(file_path),
                "patient_name": str(ds.get("PatientName", "MISSING")),
                "patient_id": str(ds.get("PatientID", "MISSING")),
                "birth_date": str(ds.get("PatientBirthDate", "MISSING")),
                "study_date": str(ds.get("StudyDate", "MISSING")),
                "series_description": str(ds.get("SeriesDescription", "MISSING")),
                "body_part_examined": str(ds.get("BodyPartExamined", "MISSING")),
                "modality": str(ds.get("Modality", "MISSING")),
                "image_position": str(ds.get("ImagePositionPatient", "MISSING")),
                "image_orientation": str(ds.get("ImageOrientationPatient", "MISSING")),
                "slice_location": str(ds.get("SliceLocation", "MISSING"))
            }

            # Identity Fraud Check (Marcova vs Macarova/Timofei)
            subject_name = "MARCOVA"
            if subject_name.upper() not in metadata["patient_name"].upper():
                if "TIMOFEI" in metadata["patient_name"].upper() or "MACAROVA" in metadata["patient_name"].upper():
                    self.anomalies.append({
                        "type": "IDENTITY_SUBSTITUTION_RISK",
                        "file": file_path,
                        "found_name": metadata["patient_name"]
                    })

            # Anatomical Alignment Check (January vs March 2022)
            study_date = metadata["study_date"]
            if study_date.startswith("202201") or study_date.startswith("202203"):
                # Track position to ensure 'in-focus' area comparison
                metadata["forensic_alignment_eligible"] = True

            # Detect high-density objects (Metallic Bolts) in PixelData
            # Note: This is a thresholding heuristic for metallic density in HU
            # (Requires pixel_array access which is computationally heavy for mass audit)
            # Placeholder for metadata-based surgical marker detection:
            if "BOLT" in metadata["series_description"].upper() or "METAL" in metadata["series_description"].upper():
                metadata["implant_detected"] = True

            self.results.append(metadata)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def build_discrepancy_table(self):
        """Synthesizes findings into the final Discrepancy Table."""
        jan_scans = [r for r in self.results if r["study_date"].startswith("202201")]
        mar_scans = [r for r in self.results if r["study_date"].startswith("202203")]
        
        for jan in jan_scans:
            # Match by slice location or anatomical position to ensure same FOV
            for mar in mar_scans:
                if jan["slice_location"] == mar["slice_location"] and jan["slice_location"] != "MISSING":
                    self.discrepancy_table.append({
                        "january_scan": jan["file_path"],
                        "march_scan": mar["file_path"],
                        "location": jan["slice_location"],
                        "jan_implant_detected": jan.get("implant_detected", False),
                        "mar_implant_detected": mar.get("implant_detected", False),
                        "status": "DISCREPANCY_FOUND" if jan.get("implant_detected") != mar.get("implant_detected") else "CONSISTENT"
                    })

    def generate_report(self, output_path):
        self.build_discrepancy_table()
        report = {
            "timestamp": datetime.now().isoformat(),
            "config_project": self.config["investigation_project"],
            "total_files_analyzed": len(self.results),
            "anomalies": self.anomalies,
            "discrepancy_table": self.discrepancy_table,
            "detailed_results": self.results
        }
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=4, ensure_ascii=False)
        print(f"Forensic report generated: {output_path}")

if __name__ == "__main__":
    # Standard paths for the A©tor environment
    CONFIG_FILE = "forensic_config/investigation_config.json"
    SCAN_DIR = "H:/ACTOR_DEV_ENV/apostille-mirror/DICOM_Archive_Local" # Placeholder path
    OUTPUT_REPORT = "forensic_reports/dicom_audit_result_20260613.json"

    if not os.path.exists("forensic_reports"):
        os.makedirs("forensic_reports")

    analyzer = DicomForensicAnalyzer(CONFIG_FILE)
    
    # Check if target directory exists, otherwise scan current mirrors/
    if os.path.exists(SCAN_DIR):
        analyzer.scan_directory(SCAN_DIR)
    else:
        print(f"Path {SCAN_DIR} not found. Scanning 'mirrors/' and 'case_macheret_repo/' for assets...")
        analyzer.scan_directory("mirrors/")
        analyzer.scan_directory("case_macheret_repo/")

    analyzer.generate_report(OUTPUT_REPORT)
