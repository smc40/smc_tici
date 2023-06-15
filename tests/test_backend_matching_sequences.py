import pandas as pd
from ..backend.load_files import read_medicament_file_as_list
from ..backend.matching_sequences import match_seq_against_list


def test_match_seq_agains_list_given_known_word_returns_true():
    searched_word = 'OXYCODONE'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)

    top_item = res['name'].values[0]
    assert top_item == 'OXYCODONE'


def test_match_seq_agains_list_given_known_word_rivaroxaban_returns_true():
    searched_word = 'RIVAROXABAN'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)
    print(res.head(3))

    top_item = res['name'].values[0]
    assert top_item == 'RIVAROXABAN'


def test_match_seq_agains_list_given_known_word_vildagliptin_returns_true():
    searched_word = 'VILDAGLIPTIN'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)
    print(res.head(3))

    top_item = res['name'].values[0]
    assert top_item == 'VILDAGLIPTIN'


def test_match_seq_agains_list_given_known_word_cabazitaxel_returns_true():
    searched_word = 'CABAZITAXEL'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)
    print(res.head(3))

    top_item = res['name'].values[0]
    assert top_item == 'CABAZITAXEL'


def test_match_seq_agains_list_given_known_word_flumol_returns_true():
    searched_word = 'FLUMOL'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)
    print(res.head(3))

    top_item = res['name'].values[0]
    assert top_item == 'FLUMOL'


def test_match_seq_agains_list_given_known_word_amoxicillin_returns_true():
    searched_word = 'AMOXICILLIN'
    sources = ['swissmedic']
    threshold = 50

    data_matched = []
    for source_name in sources:
        read_list = read_medicament_file_as_list(source_name)
        data_matched = match_seq_against_list(data_matched, read_list, source_name, searched_word, float(threshold))

    res = pd.DataFrame(data_matched, columns=['name', 'gram', 'phon-de', 'phon-fr', 'dataset'])

    # COMBINATION SCORE GERMAN
    res['comb'] = res[['gram', 'phon-de']].mean(axis=1)
    res = res.sort_values(by='comb', ascending=False)
    print(res.head(3))

    top_item = res['name'].values[0]
    assert top_item == 'AMOXICILLIN'


