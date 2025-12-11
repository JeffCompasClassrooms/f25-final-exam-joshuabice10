import pytest
from brute import Brute
from unittest.mock import Mock
import hashlib

@pytest.fixture
def easy_brute():
    return Brute("B")

@pytest.fixture
def brute_with_nums():
    return Brute("Basic2139")

@pytest.fixture
def brute_with_nums_and_special():
    return Brute("!Basic2139@")

def describe_init_method():

    def it_initializes_the_same_for_easy_brute(easy_brute):
        brute1 = easy_brute
        brute2 = Brute("B")

        assert brute1.target == brute2.target

    def it_initializes_the_same_for_brute_with_nums(brute_with_nums):
        brute1 = brute_with_nums
        brute2 = Brute("Basic2139")

        assert brute1.target == brute2.target

    def it_initializes_the_same_for_brute_with_nums_and_special(brute_with_nums_and_special):
        brute1 = brute_with_nums_and_special
        brute2 = Brute("!Basic2139@")

        assert brute1.target == brute2.target

def describe_hash_method():

    def it_uses_hash_method_correctly_to_hash_easy(easy_brute):
        brute = easy_brute
        hash_string = hashlib.sha512(bytes("B", "utf-8")).hexdigest()

        assert brute.target == hash_string
    
    def it_uses_hash_method_correctly_to_hash_with_nums(brute_with_nums):
        brute = brute_with_nums
        hash_string = hashlib.sha512(bytes("Basic2139", "utf-8")).hexdigest()

        assert brute.target == hash_string

    def it_uses_hash_method_correctly_to_hash_with_nums_and_special(brute_with_nums_and_special):
        brute = brute_with_nums_and_special
        hash_string = hashlib.sha512(bytes("!Basic2139@", "utf-8")).hexdigest()

        assert brute.target == hash_string

def describe_random_guess_method():

    def it_gives_random_guess_every_time_for_two_guesses(easy_brute):
        brute = easy_brute

        guess1 = brute.randomGuess()
        guess2 = brute.randomGuess()

        assert guess1 != guess2
    
    def it_gives_random_guess_every_time_for_multiple_guesses(easy_brute):
        brute = easy_brute

        guess1 = brute.randomGuess()
        guess2 = brute.randomGuess()
        guess3 = brute.randomGuess()

        assert guess1 != guess2 and guess1 != guess3 and guess2 != guess3

def describe_brute_once_method():

    def it_returns_true_when_same_string_given_easy(easy_brute):
        brute = easy_brute

        result = brute.bruteOnce("B") 

        assert result

    def it_returns_false_when_different_string_given_easy(easy_brute):
        brute = easy_brute

        result = brute.bruteOnce("Q") 

        assert not result
    
    def it_returns_true_when_same_string_given_with_nums(brute_with_nums):
        brute = brute_with_nums

        result = brute.bruteOnce("Basic2139") 

        assert result

    def it_returns_false_when_different_string_given_with_nums(brute_with_nums):
        brute = brute_with_nums

        result = brute.bruteOnce("Zuko8763") 

        assert not result

    def it_returns_true_when_same_string_given_with_nums_and_special(brute_with_nums_and_special):
        brute = brute_with_nums_and_special

        result = brute.bruteOnce("!Basic2139@") 

        assert result

    def it_returns_false_when_different_string_given_with_nums_and_special(brute_with_nums_and_special):
        brute = brute_with_nums_and_special

        result = brute.bruteOnce("$Zuko8763%") 

        assert not result

    def it_returns_false_with_wrong_capitalization_letter(easy_brute):
        brute = easy_brute

        result = brute.bruteOnce("b")

        assert not result

    def it_returns_false_with_wrong_capitalization_word(brute_with_nums):
        brute = brute_with_nums

        result = brute.bruteOnce("basic2139")

        assert not result

        result2 = brute.bruteOnce("BASIC2139")

        assert not result

def describe_brute_many_method():

    def it_can_crack_easy_brute(easy_brute):
        brute = easy_brute

        result = brute.bruteMany()

        assert result != -1

    def it_can_crack_brute_with_nums(brute_with_nums, mocker):
        brute = brute_with_nums
        mock_random_guesses = mocker.patch.object(Brute, "randomGuess", return_value="Basic2139")

        result = brute.bruteMany()

        mock_random_guesses.assert_called_once()
        assert result != -1

    def it_calls_mock_random_guess(mocker, easy_brute):
        brute = easy_brute
        mock_random_guesses = mocker.patch.object(Brute, "randomGuess", return_value="B")

        result = brute.bruteMany()

        mock_random_guesses.assert_called_once()

    def it_calls_hash_method(mocker, easy_brute):
        brute = easy_brute

        mock_random_guesses = mocker.patch.object(Brute, "randomGuess", return_value="B")
        mock_hash = mocker.patch.object(Brute, "hash", return_value=hashlib.sha512(bytes("B", "utf-8")).hexdigest())

        result = brute.bruteMany()

        mock_hash.assert_called_once()




        