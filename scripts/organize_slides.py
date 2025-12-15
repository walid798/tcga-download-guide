import json
import os
import openpyxl
from openpyxl import Workbook

# Read the JSON file
with open('Metadata_TCGA-KIRP.json', 'r') as f:
    data = json.load(f)

# Create a lookup dictionary for faster searching
file_id_lookup = {item['file_id']: item for item in data}

folder_path = r'slides\raw'
dest_dir = r'organized'
os.makedirs(dest_dir, exist_ok=True)

# Create workbook for Excel
wb = Workbook()
ws = wb.active
ws.title = "Cases"
ws.append(["Case Number", "Label"])

# Iterate through folders in raw directory
for folder_name in os.listdir(folder_path):
    folder = os.path.join(folder_path, folder_name)
    
    if not os.path.isdir(folder):
        continue
    
    # Search for this folder_name (file_id) in JSON
    if folder_name in file_id_lookup:
        item = file_id_lookup[folder_name]
        file_name = item['file_name']
        entity_submitter_id = item['associated_entities'][0]['entity_submitter_id'].replace('-01Z-00-DX1','')
        entity_folder = os.path.join(dest_dir, entity_submitter_id)
        
        # Create a new folder for the entity_submitter_id if it doesn't exist
        os.makedirs(entity_folder, exist_ok=True)
        
        source_file = os.path.join(folder, file_name)
        
        if os.path.exists(source_file):
            dest_file = os.path.join(entity_folder, file_name)
            os.rename(source_file, dest_file)
            print(f"Moved: {file_name} to {entity_folder}")
            # Add to Excel
            ws.append([entity_submitter_id, "KIRP"])
        else:
            print(f"File {file_name} not found in {folder}")
    else:
        print(f"Folder {folder_name} not found in JSON")

# Save Excel file
excel_path = r'...cases.xlsx'
wb.save(excel_path)
print(f"Excel file saved to {excel_path}")
