import pytest
from solution.main import strict


@strict
def add(a: int, b: int) -> int:
    return a + b


@strict
def greet(name: str, excited: bool) -> str:
    return f"Hello, {name}{'!' if excited else '.'}"


@strict
def divide(a: float, b: float) -> float:
    return a / b


@strict
def describe(age: int, *, height: float, nickname: str) -> str:
    return f"{nickname} is {age} years old and {height}m tall."


@strict
def untyped(a, b):
    return a + b


def test_add_valid():
    assert add(3, 4) == 7


def test_greet_valid():
    assert greet("Alice", True) == "Hello, Alice!"


def test_divide_valid():
    assert divide(10.0, 2.0) == 5.0


def test_describe_valid():
    assert "Shorty is 30 years old and 1.75m tall" in describe(30, height=1.75, nickname="Shorty")


def test_add_wrong_type():
    with pytest.raises(TypeError):
        add("3", 4)


def test_greet_wrong_type_bool():
    with pytest.raises(TypeError):
        greet("Alice", "yes")


def test_divide_wrong_type():
    with pytest.raises(TypeError):
        divide("10", 2.0)


def test_describe_wrong_keyword_type():
    with pytest.raises(TypeError):
        describe(30, height="tall", nickname="Shorty")


def test_describe_missing_kwarg():
    with pytest.raises(TypeError):
        describe(25, nickname="Smol")


def test_untyped():
    assert untyped("1", "2") == "12"
