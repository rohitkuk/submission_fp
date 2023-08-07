# Imports
import os
import random
import shutil
import yaml


def create_subfolders(root_folder, subfolders):
    """
    Create subfolders within the specified root folder.

    Args:
        root_folder (str): The root folder where subfolders will be created.
        subfolders (list): List of subfolder paths to be created under the root folder.
    """
    for folder in subfolders:
        folder_path = os.path.join(root_folder, folder)
        os.makedirs(folder_path, exist_ok=True)
    print("Directories created sucessfully")


def split_and_copy_files(source_folder, destination_folders, split_ratio, filter_ext):
    """
    Split and copy files from the source folder to destination folders based on the given split ratios.

    Args:
        source_folder (str): The folder containing source files to be split and copied.
        destination_folders (list): List of destination folders for the split files.
        split_ratio (list): List of split ratios for train, test, and validation sets.
    """
    #Listing the Files
    file_list = os.listdir(source_folder)
    
    #Filtering the files to only contain .tif files
    file_list = [file_ for file_ in file_list if filter_ext in file_]
    
    #Randomly Shuffling the Files
    random.shuffle(file_list)

    # Creating split indexs beased on the split ratios
    split_index1 = int(len(file_list) * split_ratio[0])
    split_index2 = split_index1 + int(len(file_list) * split_ratio[1])

    # Slicing the Lists based in the splits index created above
    train_files = file_list[:split_index1]
    test_files = file_list[split_index1:split_index2]
    valid_files = file_list[split_index2:]

    # Looping over each file and copy to the destination folders
    print(f"Copying {len(train_files)} files to {destination_folders[0]}")
    for file_name in train_files:
        src_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(destination_folders[0], file_name)
        shutil.copy(src_path, dest_path)
        
    print(f"Copying {len(test_files)} files to {destination_folders[1]}")
    for file_name in test_files:
        src_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(destination_folders[1], file_name)
        shutil.copy(src_path, dest_path)
        
    print(f"Copying {len(valid_files)} files to {destination_folders[2]}")
    for file_name in valid_files:
        src_path = os.path.join(source_folder, file_name)
        dest_path = os.path.join(destination_folders[2], file_name)
        shutil.copy(src_path, dest_path)


def create_data_yaml(path):
    """
    Creating a data YAML file with information about the dataset splits.

    Args:
        path (str): The path where the YAML file will be created.
    """
    data = {
        "train": "../splits/train/images",
        "val": "../splits/valid/images",
        "test": "../splits/test/images",
        "nc": 1,
        "names": ["fingerprint"],
    }

    # Convert the data to YAML format
    yaml_content = yaml.dump(data, default_flow_style=None, sort_keys=False)

    # Save the YAML content to a file
    with open(path, "w") as yaml_file:
        yaml_file.write(yaml_content)
    
    print(f"{path} created sucessfully")


if __name__ == "__main__":
    # Folder containing the Tiff Images
    source_folder = "images"
    # Folder will contain split datasets
    root_output_folder = "splits"
    #Subfolders for train test and valid
    subfolders = ["train/images", "test/images", "valid/images"]
    # Splitration of test train and valid
    split_ratio = [0.8, 0.1, 0.1]
    # Creating Subfolders
    create_subfolders(root_output_folder, subfolders)
    # Splitting the Files in to train test and Valid
    split_and_copy_files(
        source_folder,
        [os.path.join(root_output_folder, folder) for folder in subfolders],
        split_ratio,
        ".tif"
    )
    # Creating a data yaml file for Yolov5
    create_data_yaml(path="data_fp.yaml")
