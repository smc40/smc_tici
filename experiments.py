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
    print(data.head(1).T)

    return data


def match_orthographic(drug_testname, drug_found, list_sources):
    """
    This function takes a "drug_testname" which is the name that we look up in the FDA POCA
    implementation, and compares it against the "drug_found" which are the names that were
    found manually in the FDA POCA implementation.

    Short said, we are interested for example in the name "MAVIX", which leads to 10 top matches in the
    FDA implementation: match_1, ..., match_10. We search those 10 matches in our internal database,
    and compare only those that we indeed find OURSELVES.

    :param drug_testname:medicament name that we are interested in
    :param drug_found: medicament names found manually in the fda database
    :param list_sources: medicament list that we have in our hands.
    :return: phonetic_score: which is the estimation of the phonetic matching
    """

    # ORTHOGRAPHIC COMPARISON is the official function I wrote to calculate this in the app (search.py).
    ratio = [orthographic_comparison(drug_testname, drug_found, 'SequenceMatcher') for elem in list_sources if elem==drug_found]
    if not ratio:
        ratio = [-1]

    # This ratio could be a list with multiple values, as it could be found for example, in RxNORM and FDA.
    sequence_matcher_score = round(ratio[0], 2) * 100

    return sequence_matcher_score


def match_phonetic(drug_testname, drug_found, list_sources):
    """
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
    """
    phonetic_score = [-1]
    if drug_found in list_sources:
        phonetic_score = [phonetic_comparison(drug_testname, drug_found, 'Kolner') for elem in list_sources if drug_found==elem]

    phonetic_score = int(round(phonetic_score[0], 2) * 100)

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
    return round(diff, 2)


def run_experiments() -> pd.DataFrame:
    """
    run_experiments does not need input variables since it works from test files loaded in the server.
    run experiments reads test files, and obtains three columns named 'ortho_us', 'phonet_us', and 'combined_us'
    and proceeds to add the scores calculated by us

    # :param df_test: drug_found column is the Medicament found by the FDA algorithm
    # :param threshold:
    :return: a dataframe with all columns to compare scores
    """

    # Read all available files to test
    test_files = [file for file in os.listdir('./static') if file[0:4] == 'test']

    sources = ['fda', 'rxnorm', 'usan', 'swissmedic']

    all_sources = []
    for source_name in sources:
        all_sources.extend(read_medicament_file(source_name))

    # NOW WE GO EXPERIMENT PER EXPERIMENT
    all_experiments = []
    orthographic_diff_agg = []
    phonetic_diff_agg = []

    for file in test_files:
        exp_df = pd.read_csv("./static/"+file)

        # Make sure that all names are in CAPS
        exp_df['drug_found'] = exp_df['drug_found'].apply(lambda x: x.upper())
        exp_df['drug_name'] = exp_df['drug_name'].apply(lambda x: x.upper())

        # add new columns to add our own scores

        exp_df['ortho_us'] = exp_df.apply(lambda x: match_orthographic(x['drug_name'], x['drug_found'], all_sources), axis=1)
        exp_df['phonetic_us'] = exp_df.apply(lambda x: match_phonetic(x['drug_name'], x['drug_found'], all_sources), axis=1)
        exp_df['combined_us'] = exp_df.apply(lambda x: (x['ortho_us']+x['phonetic_us'])/2, axis=1)

        exp_df['ortho_diff'] = exp_df.apply(lambda x: calc_diff_cols(x['ortho_us'], x['orthographic']), axis=1)
        exp_df['phonetic_diff'] = exp_df.apply(lambda x: calc_diff_cols(x['phonetic_us'], x['phonetic']), axis=1)
        exp_df['combined_diff'] = exp_df.apply(lambda x: calc_diff_cols(x['combined_us'], x['combined']), axis=1)

        preserved_columns = ['drug_name', 'drug_found', 'source', 'orthographic', 'phonetic',
                             'combined', 'ortho_diff', 'phonetic_diff', 'combined_diff']

        exp_df = exp_df[preserved_columns]

        ortho_avg_diff = [int(elem) for elem in exp_df['ortho_diff'].values if int(elem) != -100]
        ortho_avg_diff = round( sum(ortho_avg_diff)/len(ortho_avg_diff) , 2)
        orthographic_diff_agg.append(ortho_avg_diff)

        phonetic_avg_diff = [int(elem) for elem in exp_df['phonetic_diff'].values if int(elem) != -100]
        phonetic_avg_diff = round( sum(phonetic_avg_diff)/len(phonetic_avg_diff) , 2)
        phonetic_diff_agg.append(phonetic_avg_diff)

        all_experiments.append(exp_df)

    return all_experiments, orthographic_diff_agg, phonetic_diff_agg

#
# if __name__ == '__main__':
#     # if len(sys.argv) > 1:
#     #     searched_string = sys.argv[1]
#     # else:
#     #     searched_string = "ibuprofen"
#
#     experiment_compare_list_fda()
