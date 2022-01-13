import sys
import pandas as pd
from pandas import DataFrame
from typing import List

from backend.comparison_utils import orthographic_comparison, phonetic_comparison
from backend.load_files import read_medicament_file, _MYPATH


def match_seq_against_list(datamatched, database: List, name_source: str, searched_word, threshold: float):

    for each in database:
        ratio = orthographic_comparison(searched_word, each, 'SequenceMatcher')

        ratio_phonetic = phonetic_comparison(searched_word, each, 'Kolner')

        ratio_fr_phonetic_fonem = phonetic_comparison(searched_word, each, 'fr-fonem')

        ratio_fr_phonetic_henry = phonetic_comparison(searched_word, each, 'fr-henry')

        ratio_combined = (ratio + ratio_phonetic) / 2
        if ratio_combined >= (float(threshold)/100):
            datamatched.append([each,
                                round(ratio * 100),
                                round(ratio_phonetic * 100),
                                round(ratio_fr_phonetic_fonem * 100),
                                round(ratio_fr_phonetic_henry * 100),
                                name_source])

    return datamatched


def collapse_sources(df_drugs_identified):
    """
    Function joins sources when a medicament is identified multiple times

    :return: dataframe with deduplicated rows
    """
    # Concatenate string
    df_drugs_identified['dataset'] = df_drugs_identified.groupby(
                                                    ['name'])[['dataset']].transform(lambda x: ', '.join(x))
    # drop duplicate data
    df_drugs_identified = df_drugs_identified.drop_duplicates()
    return df_drugs_identified


def verify_dataframe_has_items(results: DataFrame):
    if len(results) > 0:
        return results
    else:
        results = results.append({'name': 'No object found',
                                  'gram': 0,
                                  'phon': 0,
                                  'phon-fr-1': 0,
                                  'phon-fr-2': 0,
                                  'dataset': 'none',
                                  'comb': 0}, ignore_index=True)
        return results


def search(searched_word: str, sources, threshold: float = 50) -> pd.DataFrame:
    """
    Main Search Function

    """

    # UPPERCASE SEARCHED WORD
    searched_word = str(searched_word).upper()

    # INITIALIZE 'data_matched' VARIABLE
    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon', 'phon-fr-1', 'phon-fr-2', 'dataset'])
    res['comb'] = res[['gram', 'phon']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)

    # VERIFY IT IS EMPTY
    print(res)
    res = verify_dataframe_has_items(res)
    print(res)

    # COLLAPSE SOURCES AND DEDUPLICATE
    res = collapse_sources(res)

    res.to_csv(_MYPATH+'output/result_' + searched_word + '.csv', header=None)
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1:
        searched_string = sys.argv[1]
    else:
        searched_string = "ibuprofen"

    search(searched_string)
