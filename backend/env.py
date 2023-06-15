from pathlib import Path


def process_folder_path():
    resolved_path = Path().resolve()
    folder_name = str(resolved_path)#.name
    print(f'This is the folder name: {folder_name}')

    if folder_name.endswith("smc_tici") and not folder_name.endswith("smc_tici/smc_tici"):
        index = folder_name.rfind("smc_tici")
        truncated_name = folder_name[:index]
        new_folder_name = truncated_name + "smc_tici/smc_tici"
        print(f'\nThis is the new_folder_name: {new_folder_name}')

        #new_path = resolved_path.with_name(new_folder_name)
        return str(new_folder_name)
    elif folder_name.endswith("smc_tici/smc_tici"):
        return str(folder_name)
    else:
        return str(folder_name)

    return None


path_extracted = process_folder_path()
if type(path_extracted) == str:
    _MYPATH = path_extracted + '/'


FDA_FILEPATH = _MYPATH + 'static/drugsatfda_20210527.csv'
USAN_FILEPATH = _MYPATH + 'static/data/20211125_USAN_stem_list_cumulative_csv_2.csv'
RXNORM_FILEPATH = _MYPATH + 'static/drugs_rxnorm_20210510.csv'
SWISSMEDIC_FILEPATH = _MYPATH + 'static/swissmedic_zugelassene_arzneimittel_20230531_public.xlsx'


