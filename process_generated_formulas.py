import random
import re
from im2latex_utils import tokenize_formula, remove_invisible, normalize_formula


def preprocess_formulas(formula):
    formula = normalize_formula(formula)
    formula = remove_invisible(formula)
    return ' '.join(tokenize_formula(formula))


def fix_numbered_list(formulas_list):
    pattern = '[0-9]+\. (.*)'

    res = []
    for el in formulas_list:
        el = el.strip()
        s = re.search(pattern, el)
        if s:
            res.append(s.group(1))
        else:
            res.append(el)
    return res


def concat_and_process_files(files_to_read, dir_path):
    all_data = []
    for file_to_read in files_to_read:
        with open(file_to_read, 'r') as f:
            d = f.read()
            d = d.split('\n')
            all_data.extend(d)

    all_data = fix_numbered_list(all_data)
    all_data = [preprocess_formulas(x) for x in all_data]

    print(f"sample:\n {all_data[:10]}")
    print('len all:', len(all_data))
    print('len unique:', len(set(all_data)))

    with open(dir_path + '/outp.txt', 'w') as f:
        for el in set(all_data):
            f.write(el + '\n')


def concat_outp_files(file_paths, outp_path):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r') as f:
            data.extend(f.read().split('\n'))
    print("Concatenated len:", len(data))
    data = list(set(data))
    print("Unique len:", len(data))
    random.shuffle(data)

    with open(outp_path, 'w') as f:
        f.write('\n'.join(data))


if __name__ == "__main__":
    concat_outp_files(
        [
            'data/article_prompts/outp.txt',
            'data/article_prompts_big/outp.txt',
            'data/const_prompt/outp.txt',
            'data/variable_prompts/outp.txt',
        ],
        'data/concat_outp.txt'
    )