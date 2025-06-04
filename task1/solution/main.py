def strict(func):
    """
    A decorator for people who like their arguments like they like their types — strict.

    Checks that all positional arguments match the function's type annotations.
    If someone tries to sneak in the wrong type, it throws a glorious TypeError
    and makes sure they feel bad about it.

    Only works with:
        - annotated types: bool, int, float, str (nothing fancy, keep it vanilla)

    Args:
        func (Callable): The function to be wrapped in judgment.

    Returns:
        Callable: The wrapped function that now has trust issues.
    """
    annotations = func.__annotations__
    arg_names = [key for key in annotations.keys() if key != 'return']

    def wrapper(*args, **kwargs):
        for name, value in list(zip(arg_names, args)) + list(kwargs.items()):
            expect = annotations[name]

            if not isinstance(value, expect):
                raise TypeError(f"Argument '{name}' must be {expect.__name__}, got {type(value).__name__}")

        return func(*args, **kwargs)

    return wrapper


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


if __name__ == '__main__':
    print(sum_two(1, 2))
    print(sum_two(1, b=2.4))
