import sys
import pandas as pd
from pandas import DataFrame
from backend.load_files import read_medicament_file_as_list
# from backend.env import OUTPUT_PATH
from backend.matching_sequences import match_seq_against_list


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

    # UPPERCASE SEARCHED WORD, WHERE SEARCHED_WORD IS STRING SUBMITTED BY USER.
    searched_word = str(searched_word).upper()

    # INITIALIZE 'data_matched' VARIABLE. LIST WITH MATCHES THAT IS LATER READ AS DATAFRAME.
    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)

    # COMBINATION SCORE FRENCH
    res['comb-fr'] = res[['gram', 'phon-fr']].mean(axis=1)

    # VERIFY IT IS EMPTY
    print(res)
    res = verify_dataframe_has_items(res)
    print(res)

    # COLLAPSE SOURCES AND DEDUPLICATE
    res = collapse_sources(res)

    # res.to_csv(OUTPUT_PATH / 'result_' + searched_word + '.csv', header=None)
    return res


if __name__ == '__main__':
    if len(sys.argv) > 1:
        searched_string = sys.argv[1]
    else:
        searched_string = "ibuprofen"

    search(searched_string)
