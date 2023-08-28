import glob
import hashlib
import os
from multiprocessing import Pool
from subprocess import call

import pandas as pd
from tqdm import tqdm

from formula2image import formula_to_image_simplified

THREADS = 16
IMAGE_DIR = "formula_images_multiple"
DATASET_FILE = 'image_mapping.csv'


def generate_images(path_to_formula_file):
    os.makedirs(IMAGE_DIR, exist_ok=True)
    [os.makedirs(IMAGE_DIR + f'/images_{i}', exist_ok=True) for i in range(10)]

    with open(path_to_formula_file, 'r') as f:
        formulas = f.read().split("\n")
    os.makedirs(IMAGE_DIR, exist_ok=True)
    if not IMAGE_DIR in os.getcwd():
        os.chdir(IMAGE_DIR)

    print("Turning formulas into images...")

    # Change to image dir because textogif doesn't seem to work otherwise...
    oldcwd = os.getcwd()
    # Check we are not in image dir yet (avoid exceptions)
    if not IMAGE_DIR in os.getcwd():
        os.chdir(IMAGE_DIR)

    pool = Pool(THREADS)
    names = list(tqdm(pool.imap_unordered(formula_to_image_simplified, formulas), total=len(formulas)))


def gather_all_images(paths_to_images, target_image_folder):
    for path in paths_to_images:
        call(['cp', '-a', path + '/.', target_image_folder])


def make_dataset_file(formulas_file, image_folder, dataset_filename):
    with open(formulas_file, 'r') as f:
        formulas = f.read().split("\n")
    formula_hashes = [hashlib.sha1(f.encode('utf-8')).hexdigest()[:15] for f in formulas]
    formulas_dict = dict(zip(formula_hashes, formulas))

    images = [os.path.basename(x) for x in glob.glob(image_folder + '/*')]
    image_hashes = [x.split('_')[0] for x in images]

    res = []
    for i in range(len(image_hashes)):
        if image_hashes[i] in formulas_dict:
            res.append((formulas_dict[image_hashes[i]], images[i]))

    print("Images:  ", len(set(image_hashes)))
    print("Formulas:", len(set(formula_hashes)))
    print("Intersection:", len(res))

    df = pd.DataFrame.from_records(res, columns=['formulas', 'images'])
    print(df)

    df.to_csv(dataset_filename, index=False)


def draw_length_distribution(dataset_filename):
    df = pd.read_csv(dataset_filename)
    df['token_count'] = df['formulas'].apply(lambda x: len(x.split()))
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.histplot(data=df[df['token_count'] < 200], x='token_count')
    plt.show()


if __name__ == "__main__":
    # generate_images('data/concat_outp.txt')
    # gather_all_images(
    #     [
    #         'formula_images_multiple/images_0',
    #         'formula_images_multiple/images_1',
    #         'formula_images_multiple/images_2',
    #         'formula_images_multiple/images_3',
    #         'formula_images_multiple/images_4',
    #         'formula_images_multiple/images_5',
    #         'formula_images_multiple/images_6',
    #         'formula_images_multiple/images_7',
    #         'formula_images_multiple/images_8',
    #         'formula_images_multiple/images_9',
    #     ],
    #     'result_images'
    # )
    # make_dataset_file(
    #     'data/concat_outp.txt',
    #     'result_images',
    #     'image_formula_mapping.csv'
    # )
    draw_length_distribution('image_formula_mapping.csv')
