# test_addition.py

import slash


def test_addition():
    pass


@slash.parameters.toggle('with_power_operator')
def test_power_of_two(with_power_operator):
    num = 2
    if with_power_operator:
        result = num ** 2
    else:
        result = num * num
    assert result == 4


@slash.parametrize('x', [1, 2, 3])
def test_something(x):
    slash.logger.warning(f"Running test {x}")
    assert True
