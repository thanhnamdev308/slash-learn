# What is SLASH?

__Slash__ is a testing framework written in Python.

Unlike many other testing frameworks out there, Slash focuses on building in-house testing solutions for large projects.

It provides facilities and best practices for testing complete products, and not only unit tests for individual modules.

- [Get Started](#get-started)
- [Running test](#running-test)
- [Test fixture](#test-fixture)
- [Test report](#test-report)
- [Some notable knowledge](#some-notable-knowledge)

# Get Started

Create a simple test file named `test_addition.py`
```python
# test_addition.py

import slash

def test_addition():
    pass
```
Functions starting with the prefix `test_` are assumed to be runnable tests.

__Run the test:__
```bash
slash run test_addition.py
```

__Debugging:__ You can debug failing tests using the `--pdb` flag, which automatically runs the best available debugger on exceptions. You can also filter the exceptions which run the debugger by using `--pdb-filter` in addition to the `--pdb` flag.

__Assertions and Errors:__ Tests make sure things are like they expect with `assert` keyword.
```python
# test_addition.

def test_addition():
    assert 2 + 2 == 4
```

__Test Parameters:__ Slash tests can be parametrized, iterating parameter values and __creating separate cases__ for each value:
```python
@slash.parametrize('x', [1, 2, 3])
def test_something(x):
    # use x here
```
For boolean values, a shortcut exists for __toggling between True and False__:
```python
@slash.parameters.toggle('with_power_operator')
def test_power_of_two(with_power_operator):
    num = 2
    if with_power_operator:
        result = num ** 2
    else:
        result = num * num
    assert result == 4
```

__Logging:__ Slash uses [Logbook](https://logbook.readthedocs.io/en/stable/) for logging and exposes __a global logger__:
```python
import slash

def test_1():
    slash.logger.debug("Hello!")
```
By default logs above WARNING get emitted to the console when slash run is executed. You can use `-v`/`-q` to increase/decrease console verbosity accordingly.

By default logs are not saved anywhere. This is easily changed with the `-l` flag to `slash run`. Point this flag to a directory, and Slash will organize logs inside, in subdirectories according to the session and test run (e.g. /path/to/logdir/<session id>/<test id>/debug.log).

# Running test


# Test fixture

In testing, a __fixture__ provides a defined, reliable and consistent context for the tests. This could include __environment__ (for example a database configured with known parameters) or __content__ (such as a dataset).

- Return fixture: the fixture will return the value for the testing.
- Support to add the interable parameters for the fixture
- Setup and Teardown: the fixture support the feature to init at the begin of the tests and it also support to execute a function after the test finished.


# Test report


# Some notable knowledge

