from pathlib import Path

ROOT_PATH = str(Path(__file__).parents[1]) + '/'

FDA_FILEPATH = ROOT_PATH + 'static/drugsatfda_20210527.csv'
USAN_FILEPATH = ROOT_PATH + 'static/data/20211125_USAN_stem_list_cumulative_csv_2.csv'
RXNORM_FILEPATH = ROOT_PATH + 'static/drugs_rxnorm_20210510.csv'
SWISSMEDIC_FILEPATH = ROOT_PATH + 'static/swissmedic_zugelassene_arzneimittel_20230531_public.xlsx'
