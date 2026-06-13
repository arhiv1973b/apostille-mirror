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
                "manufacturer": str(ds.get("Manufacturer", "MISSING")),
                "institution_name": str(ds.get("InstitutionName", "MISSING"))
            }

            # Identity Fraud Check (Rule: Galina Marcova 28.02.1953)
            subject_name = "MARCOVA" # Base search
            expected_birth = "19530228"
            
            if subject_name.upper() not in metadata["patient_name"].upper():
                if "TIMOFEI" in metadata["patient_name"].upper() or "MACAROVA" in metadata["patient_name"].upper():
                    self.anomalies.append({
                        "type": "IDENTITY_SUBSTITUTION_RISK",
                        "file": file_path,
                        "found_name": metadata["patient_name"],
                        "expected": "MARCOVA GALINA"
                    })
            
            if metadata["birth_date"] != expected_birth and metadata["birth_date"] != "MISSING":
                self.anomalies.append({
                    "type": "BIRTH_DATE_DISCREPANCY",
                    "file": file_path,
                    "found_birth": metadata["birth_date"],
                    "expected": expected_birth
                })

            # Physical Marker Check (Laparotomy/Metallic Implants)
            # Note: Deep pixel-level analysis for '3 metallic bolts' would require advanced CV, 
            # here we check for surgical metadata or series notes first.
            if "LAPAROTOMY" in metadata["series_description"].upper() or "BOLT" in metadata["series_description"].upper():
                metadata["marker_found"] = True
            
            self.results.append(metadata)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def scan_directory(self, root_dir):
        """Recursively scans for DICOM/IMA files."""
        for root, _, files in os.walk(root_dir):
            for file in files:
                if file.lower().endswith(('.dcm', '.ima')):
                    full_path = os.path.join(root, file)
                    self.analyze_file(full_path)

    def generate_report(self, output_path):
        report = {
            "timestamp": datetime.now().isoformat(),
            "config_project": self.config["investigation_project"],
            "total_files_analyzed": len(self.results),
            "anomalies_detected": len(self.anomalies),
            "anomalies": self.anomalies,
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
