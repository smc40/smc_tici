#########################
# TESTING
#########################
import os
import pandas as pd
from search import read_medicament_file
from search import orthographic_comparison
from search import phonetic_comparison

_MYPATH = 'C:/Users/pen/PycharmProjects/poca_app/'

def read_test_files():
    '''
    To read a test file
    '''
    # Read file for comparison
    data = pd.read_csv(_MYPATH + 'static/test_fda_mavix.csv', header='infer', delimiter=",")
    print(data.head(3).T)

    return data


def match_orthographic(drug_testname, drug_found, list_sources):
    '''
    This function takes a "drug_testname" which is the name that we look up in the FDA POCA
    implementation, and compares it agains the "drug_found" which are the names that were
    found manually in the FDA POCA implementation.

    Short said, we are interested for example in
    the name "MAVIX", which lead to 10 top matches in the FDA implementation: match_1, ...,
    match_10. We search those 10 matches in our internal database, and compare only those that we
    indeed find OURSELVES.

    :param drug_testname:medicament name that we are interested in
    :param drug_found: medicament names found manually in the fda database
    :param list_sources: medicament list that we have in our hands.
    :return: phonetic_score: which is the estimation of the phonetic matching
    '''
    ratio = -1
    ratio = [orthographic_comparison(drug_testname, drug_found, 'SequenceMatcher') for elem in list_sources if elem==drug_found]

    sequence_matcher_score = round(ratio, 2)*100

    return sequence_matcher_score


def match_phonetic(drug_testname, drug_found, list_sources):
    '''
    This function takes a "drug_testname" which is the name that we look up in the FDA POCA
    implementation, and compares it agains the "drug_found" which are the names that were
    found manually in the FDA POCA implementation. Short said, we are interested for example in
    the name "MAVIX", which lead to 10 top matches in the FDA implementation: match_1, ...,
    match_10. We search those 10 matches in our internal database, and compare only those that we
    indeed find OURSELVES.

    :param drug_testname:medicament name that we are interested in
    :param drug_found: medicament names found manually in the fda database
    :param list_sources: medicament list that we have in our hands.
    :return: phonetic_score: which is the estimation of the phonetic matching
    '''

    phonetic_score = -1
    if drug_found in list_sources:
        phonetic_score = [phonetic_comparison(drug_testname, drug_found, 'Kolner') for elem in list_sources if drug_found==elem]

    phonetic_score = int(round(phonetic_score, 2) * 100)
    print('phonetic score')
    print(phonetic_score)

    return phonetic_score


def calc_diff_cols(ortho_us, ortho):
    '''
    calc_diff_cols calculates the difference between two columns
    in order to estimate how well we are doing
    '''
    if ortho_us != -100:
        diff = ortho - ortho_us
    elif ortho_us == -100:
        diff = -100
    return diff

#def experiment_compare_list_fda(df_test, threshold: str = "0.5") -> pd.DataFrame:
def experiments() -> pd.DataFrame:
    '''
    compare_list_fda generates three columns named ortho_us, phonet_us
    and combined_us which add the scores calculated by us

    :param df_test: drug_found column is the Medicament found by the FDA algorithm
    :param threshold:
    :return: a dataframe with all columns to compare scores
    '''

    # Read all available files to test
    test_files = [file for file in os.listdir('./static') if file[0:4] == 'test']

    sources = ['fda','rxnorm','usan','swissmedic']

    list_all_sources = []
    for source_name in sources:
        list_all_sources.extend(read_medicament_file(source_name))

    # NOW WE GO EXPERIMENT PER EXPERIMENT
    if False:
        for file in test_files:
            print(file)
            current_df = pd.read_csv("./static/"+file)

            # Make sure that all names are in CAPS
            current_df['drug_found'] = current_df['drug_found'].apply(lambda x: x.upper())
            current_df['drug_name'] = current_df['drug_name'].apply(lambda x: x.upper())

            # add new columns to add our own scores

            current_df['ortho_us'] = current_df.apply(lambda x: match_orthographic(
                                                    x['drug_name'], x['drug_found'], list_all_sources), axis=1)

            current_df['phonetic_us'] = current_df.apply(lambda x: match_phonetic(
                                                    x['drug_name'], x['drug_found'], list_all_sources), axis=1)

            current_df['combined_us'] = current_df.apply(lambda x: (x['ortho_us']+x['phonetic_us'])/2, axis=1)

            current_df['ortho_diff'] = current_df.apply(lambda x: calc_diff_cols(x['ortho_us'], x['orthographic']), axis=1)
            current_df['phonetic_diff'] = current_df.apply(lambda x: calc_diff_cols(x['phonetic_us'], x['phonetic']), axis=1)
            current_df['combined_diff'] = current_df.apply(lambda x: calc_diff_cols(x['combined_us'], x['combined']), axis=1)
            print('DONE')
            print(current_df.T)

    current_df = current_df = pd.read_csv("./static/"+test_files[0])
    return current_df.T

#
# if __name__ == '__main__':
#     # if len(sys.argv) > 1:
#     #     searched_string = sys.argv[1]
#     # else:
#     #     searched_string = "ibuprofen"
#
#     experiment_compare_list_fda()
