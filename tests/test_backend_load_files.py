from ..backend.load_files import read_medicament_file_as_list


def test_read_medicament_file_as_list_given_empty_list_returns():
    chosen_sources = []
    returned_value = read_medicament_file_as_list(chosen_sources)
    print(f'this is the returned value: {returned_value}')
    assert not returned_value


