#This code is used to sort json files based on the output of the sam model
#It will read the json files and extract the labels used in the segmentation
#Then it will create folders for each label and copy the json files into the corresponding folders
#If a json file has multiple labels it will be copied into each corresponding folder
#Created by Samuel Storey 2025

import os
import json
import shutil
from pathlib import Path

#This method will read the json file output of sam
def load_json(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

#This method will take the json data from the files like the segmentation and get the labels used
def extract_labels_from_json(json_data):
    objects = json_data.get("objects", [])
    labels = set()

    for obj in objects:
        category = obj.get("category")
        if category:
            labels.add(category.lower())  # Normalize to lowercase

    return labels if labels else {"unlabeled"}

#Based on the label given this will make a copy of the json file input in a file that contains the label name
def categorize_json_file(json_path, output_base="categorized"):
    try:
        json_data = load_json(json_path)  # reads json file
        labels = extract_labels_from_json(json_data)  # extracts labels

        for label in labels:
            label_dir = Path(output_base) / label
            label_dir.mkdir(parents=True, exist_ok=True)  # make label folder

            destination = label_dir / Path(json_path).name
            shutil.copy(json_path, destination)

    except Exception as e:
        folder = Path(json_path).parent
        print(f"Failed to process file: {json_path} at Folder: {folder}")


#access a given folder of json files to sort
def process_all_folders(base_path=".", output_base="categorized"):
    base_dir = Path(base_path).resolve()

    for folder in base_dir.iterdir():
        if folder.is_dir() and folder.name != output_base:
            print(f"\nProcessing folder: {folder}")
            process_directory(folder, output_base)

def process_directory(json_folder, output_base="categorized"):
    json_files = Path(json_folder).rglob("*.json")
    for json_file in json_files:
        categorize_json_file(json_file, output_base)

def main():
    script_dir = Path(__file__).parent
    output_folder = script_dir / "categorized"

    process_all_folders(script_dir, output_folder)

if __name__ == "__main__":
    main()
