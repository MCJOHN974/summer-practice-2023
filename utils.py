import glob
import os
import pandas as pd


def cleanup_dataset(image_dir, dataset_file, dry_run=True):
    image_paths = glob.glob(image_dir + '/*')
    good_images = set(pd.read_csv(dataset_file)['images'].tolist())

    for image_path in image_paths:
        filename = os.path.basename(image_path)
        if filename not in good_images:
            if dry_run:
                print(f"BAAAAANG! Would have deleted {filename}")
            else:
                print(f"Deleting {filename}")
                os.remove(image_path)


if __name__ == "__main__":
    cleanup_dataset(
        'result_images',
        'image_formula_mapping.csv'
    )