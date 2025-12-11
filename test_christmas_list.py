import os, pytest, pickle
from christmas_list import ChristmasList

@pytest.fixture
def test_file():
    filename = "test_christmas_list.db"
    # Ensure a clean file
    if os.path.exists(filename):
        os.remove(filename)
    yield filename
    # Cleanup after test
    if os.path.exists(filename):
        os.remove(filename)

@pytest.fixture
def prefilled_file(test_file):
    data = [{"exists": "existing"}]
    with open(test_file, "wb") as f:
        pickle.dump(data, f)
    return test_file

@pytest.fixture
def real_item_file(test_file):
    data = [{"name": "FPV Drone", "purchased": False}]
    with open(test_file, "wb") as f:
        pickle.dump(data, f)
    return test_file

def describe_init_method():

    def it_creates_file_if_missing(test_file):
        assert not os.path.exists(test_file)
        list = ChristmasList(test_file)
        assert os.path.exists(test_file)
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == []

    def it_keeps_existing_file_and_sets_fname(prefilled_file):
        list = ChristmasList(prefilled_file)
        assert list.fname == prefilled_file
        with open(prefilled_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"exists": "existing"}]

def describe_loadItems():

    def it_loads_empty_file(test_file):
        list = ChristmasList(test_file)
        assert list.loadItems() == []

    def it_loads_file_with_one_item(prefilled_file):
        list = ChristmasList(prefilled_file)
        assert list.loadItems() == [{"exists": "existing"}]

    def it_loads_file_with_multiple_items(test_file):
        items = [{"A": "a", "B": "b", "C": "c"}]
        with open(test_file, "wb") as f:
            pickle.dump(items, f)
        list = ChristmasList(test_file)
        assert list.loadItems() == items

def describe_saveItems():

    def it_saves_empty_list(test_file):
        list = ChristmasList(test_file)
        list.saveItems([])
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == []

    def it_saves_single_item(test_file):
        list = ChristmasList(test_file)
        list.saveItems([{"one": 1}])
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"one": 1}]

    def it_saves_multiple_items(test_file):
        list = ChristmasList(test_file)
        items = [{"one": 1}, {"two": 2}, {"three": 3}]
        list.saveItems(items)
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == items

    def it_overwrites_existing_data(prefilled_file):
        list = ChristmasList(prefilled_file)
        list.saveItems([{"New": "new"}])
        with open(prefilled_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"New": "new"}]
                        
def describe_add():

    def it_saves_to_empty_file(test_file):
        list = ChristmasList(test_file)
        list.add("test")
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"name": 'test', "purchased": False}]

    def it_appends_to_existing_data(prefilled_file):
        list = ChristmasList(prefilled_file)
        list.add("test")
        with open(prefilled_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"exists": "existing"}, {"name": "test", "purchased": False}]

    def it_saves_multiple_strings_sequentially(test_file):
        list = ChristmasList(test_file)
        list.add("Cool Thing")
        list.add("Cool Object")
        list.add("Cool Stuff")
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"name": "Cool Thing", "purchased": False}, {"name": "Cool Object", "purchased": False}, {"name": "Cool Stuff", "purchased": False}]

    def it_saves_empty_string(test_file):
        list = ChristmasList(test_file)
        list.add("")
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"name": "", "purchased": False}]

    def it_saves_strings_with_special_characters(test_file):
        list = ChristmasList(test_file)
        list.add("!@#")
        list.add("123")
        list.add("abc")
        with open(test_file, "rb") as f:
            data = pickle.load(f)
        assert data == [{"name": "!@#", "purchased": False}, {"name": "123", "purchased": False}, {"name": "abc", "purchased": False}]

def describe_check_off():

    def it_checks_off_item_correctly(real_item_file):
        list = ChristmasList(real_item_file)
        list.check_off("FPV Drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": True}]

    def it_checks_off_only_correct_item_correctly(real_item_file):
        list = ChristmasList(real_item_file)
        list.add("NotCheckedThing")
        list.check_off("FPV Drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": True}, {"name": "NotCheckedThing", "purchased": False}]

    def it_will_not_check_off_if_name_is_wrong(real_item_file):
        list = ChristmasList(real_item_file)
        list.check_off("fpv drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": False}]

    def it_will_not_check_off_if_name_is_wrong_multiple_items(real_item_file):
        list = ChristmasList(real_item_file)
        list.add("NotCheckedThing")
        list.check_off("fpv drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": False}, {"name": "NotCheckedThing", "purchased": False}]

def describe_remove():

    def it_will_remove_the_correct_item(real_item_file):
        list = ChristmasList(real_item_file)
        list.remove("FPV Drone")

        assert list.loadItems() == []

    def it_wont_remove_item_if_name_wrong(real_item_file):
        list = ChristmasList(real_item_file)
        list.remove("fpv drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": False}]

    def it_will_remove_correct_item_when_multiple_exist(real_item_file):
        list = ChristmasList(real_item_file)
        list.add("NotCheckedThing")
        list.remove("FPV Drone")

        assert list.loadItems() == [{"name": "NotCheckedThing", "purchased": False}]

    def it_will_remove_multiple_items_in_correct_order(real_item_file):
        list = ChristmasList(real_item_file)
        list.add("NotCheckedThing")
        list.remove("FPV Drone")

        assert list.loadItems() == [{"name": "NotCheckedThing", "purchased": False}]

        list.remove("NotCheckedThing")

        assert list.loadItems() == []

    def it_will_remove_empty_item_correctly(test_file):
        list = ChristmasList(test_file)
        list.add("")
        
        assert list.loadItems() == [{"name": "", "purchased": False}]

        list.remove("")

        assert list.loadItems() == []

    def it_will_remove_checked_item_correctly(real_item_file):
        list = ChristmasList(real_item_file)
        list.check_off("FPV Drone")

        assert list.loadItems() == [{"name": "FPV Drone", "purchased": True}]

        list.remove("FPV Drone")

        assert list.loadItems() == []

def describe_print_list():

    def it_prints_off_item_correctly(capsys, real_item_file):
        list = ChristmasList(real_item_file)
        list.print_list()

        captured = capsys.readouterr()
        assert captured.out == "[_] FPV Drone\n"
    
    def it_prints_off_checked_item_correctly(capsys, real_item_file):
        list = ChristmasList(real_item_file)
        list.check_off("FPV Drone")
        list.print_list()

        captured = capsys.readouterr()
        assert captured.out == "[x] FPV Drone\n"

    def it_prints_off_multiple_items_correctly(capsys, real_item_file):
        list = ChristmasList(real_item_file)
        list.add("Foundry")
        list.print_list()

        captured = capsys.readouterr()
        assert captured.out == "[_] FPV Drone\n[_] Foundry\n"

    def it_prints_off_multiple_checked_items_correctly(capsys, real_item_file):
        list = ChristmasList(real_item_file)
        list.add("Foundry")
        list.check_off("FPV Drone")
        list.check_off("Foundry")
        list.print_list()

        captured = capsys.readouterr()
        assert captured.out == "[x] FPV Drone\n[x] Foundry\n"

    def it_prints_off_item_with_no_name(capsys, test_file):
        list = ChristmasList(test_file)
        list.add("")

        assert list.loadItems() == [{"name": "", "purchased": False}]

        list.print_list()
        captured = capsys.readouterr()
        assert captured.out == "[_] \n" 

    def it_prints_off_item_with_no_name_when_checked(capsys, test_file):
        list = ChristmasList(test_file)
        list.add("")

        assert list.loadItems() == [{"name": "", "purchased": False}]
        list.check_off("")

        list.print_list()
        captured = capsys.readouterr()
        assert captured.out == "[x] \n"

    def it_prints_off_item_with_no_name_with_another_item(capsys, test_file):
        list = ChristmasList(test_file)
        list.add("")
        list.add("AnotherItem")

        assert list.loadItems() == [{"name": "", "purchased": False}, {"name": "AnotherItem", "purchased": False}]

        list.print_list()
        captured = capsys.readouterr()
        assert captured.out == "[_] \n[_] AnotherItem\n"