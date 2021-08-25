import os
import sys
import pandas as pd
from difflib import SequenceMatcher
from typing import List
import importlib
import pathlib

cologne = importlib.import_module("cologne_phonetics")


#_MYPATH = '/home/alexsmc/poca/'
#_MYPATH = '/Users/nicolasperez/PycharmProjects/app_poca/'
#_MYPATH = 'C:/Users/pen/PycharmProjects/poca_app/'
# _MYPATH = 'C:/Users/pen/PycharmProjects/poca_app/'

# IN PROD PATH
localpath = pathlib.Path().resolve()
_MYPATH = str(localpath) + '/'
print(_MYPATH)

def orthographic_comparison(searched_string, element_list, option):
    if option == 'SequenceMatcher':
        ratio = SequenceMatcher(None, searched_string, element_list).ratio()
    return ratio


def phonetic_comparison(searched_string, element_list, option):
    '''
    drug_testname = searched_string
    drug_found = element_list

    This function takes a "searched_string" which is the name that we interested in and compares it
    against the "element_list" which are the names that are pulled from the large datasets. Short said,
    we are interested for example in the name "MAVIX", and compare again the entire list one by one

    :param searched_string: medicament name that we are interested in
    :param element_list: medicament names from the databases
    :param option: given phonetic technic for comparison
    :return: phonetic_score: which is the estimation of the phonetic matching
    '''
    ratio = -1
    if option == 'Kolner':
        drug_interest = cologne.encode(searched_string.upper())[0][1]
        drug_in_our_list = cologne.encode(element_list.upper())[0][1]
        ratio = SequenceMatcher(None, drug_interest, drug_in_our_list).ratio()

        phonetic_score = float(round(ratio, 2))

    return phonetic_score


def match_seq_against_list(datamatched, database: List, name_source: str, searched_string, threshold):

    for each in database:
        ratio = orthographic_comparison(searched_string, each, 'SequenceMatcher')

        ratio_phonetic = phonetic_comparison(searched_string, each, 'Kolner')

        print('this is threshold')
        print(threshold)
        if ratio >= (float(threshold) / 100) or ratio_phonetic >= (float(threshold) / 100) :
            datamatched.append([each, round(ratio * 100), round(ratio_phonetic * 100), name_source])

    return datamatched


def collapse_sources(df_drugs_identified):
        '''
        Function joins sources when medicamente is identified multiple times

        :return: dataframe with deduplicated rows
        '''
        # Concatenate string
        df_drugs_identified['dataset'] = df_drugs_identified.groupby(
            ['name'])[['dataset']].transform(lambda x: ', '.join(x))
        # drop duplicate data
        df_drugs_identified = df_drugs_identified.drop_duplicates()

        return df_drugs_identified


def read_medicament_file(chosen_sources):
    print(f'The current directory is {os.listdir()}')
    print(f'Here...')
    print(pathlib.Path().resolve())
    print(f'The current directory static is {os.listdir("/static/")}')
    """
    To read file from any of the four sources ['fda','rxnorm','usan','swissmedic']

    Input:
    chosen_sources: List with any number out of the possible sources ['fda','rxnorm','usan','swissmedic']
    Return:
    File: read individual file for that specific source.
    """
    print('The chosen sources are: {}'.format(chosen_sources))
    if chosen_sources == 'fda':
        # Read file for comparison
        filepath = _MYPATH + 'static/drugsatfda_20210527.csv'
        data = pd.read_csv(filepath, header=None, delimiter="|")
        name = pd.Series(data.iloc[:, [1, 4]].to_numpy().flatten())
        name = name.drop_duplicates()
        name = name.dropna().to_list()
        print("Number of drugs at the FDA database: ", len(name))

    if chosen_sources == 'usan':
        filepath = _MYPATH+'static/drugs_usan_20210227.csv'
        data = pd.read_csv(filepath, header='infer', delimiter="|")
        name = data.EXAMPLE.to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna()
        name = name.to_list()
        print("Number of drugs USAN database: ", len(name))

    if chosen_sources == 'rxnorm':
        filepath = _MYPATH+'static/drugs_rxnorm_20210510.csv'
        data = pd.read_csv(filepath, header=None, delimiter="|")
        name = data.iloc[:, 1].to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna().to_numpy()
        list_output = [drug.upper() for drug in name]
        print("Number of drugs at the RxNorm database: ", len(list_output))
        return list_output

    if chosen_sources == 'swissmedic':
        filepath = _MYPATH+'static/Swissmedic_20191012_import.csv'
        data = pd.read_csv(filepath, header=None, delimiter="|", encoding='latin1')
        name = data.iloc[:, 1].to_numpy().flatten()
        name = pd.Series(name).drop_duplicates()
        name = name.dropna().to_numpy()
        list_output = [drug.upper() for drug in name]
        print("Number of drugs at the Swissmedic database: ", len(list_output))

        return list_output

    return name


def search(searched_string: str, sources, threshold: str = "0.5") -> pd.DataFrame:

    # Write word in caps
    searched_string = str(searched_string).upper()
    print("Drug under evaluation: ", searched_string)

    # Initialize 'data_matched'
    data_matched = []

    print('These are the sources we want to look through: {}'.format(sources))
    for source_name in sources:
        read_list = read_medicament_file(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_string, threshold)

    print('Data is already matched')
    res = pd.DataFrame(data_matched, columns=["name", "grammatik", "phonetik", "dataset"])
    res = res.sort_values(by='grammatik', ascending=False)
    res['combined'] = res[['grammatik', 'phonetik']].mean(axis=1)
    print('Flag: Data is already sorted')

    print(res.head(5))

    # Collapse sources, and de-dup
    res = collapse_sources(res)

    print(res.head(15))

    res.to_csv(_MYPATH+'output/result_'+searched_string+'.csv', header=None)
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1:
        searched_string = sys.argv[1]
    else:
        searched_string = "ibuprofen"

    search(searched_string)
