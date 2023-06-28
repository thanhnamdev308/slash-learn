# What is SLASH?

__Slash__ is a testing framework written in Python.

Unlike many other testing frameworks out there, Slash focuses on building in-house testing solutions for large projects.

It provides facilities and best practices for testing complete products, and not only unit tests for individual modules.

- [Get Started](#get-started)
- [How to invoke pytest](#how-to-invoke-pytest)
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

Run the test:
```bash
slash run test_addition.py
```

# How to invoke pytest


# Test fixture

In testing, a __fixture__ provides a defined, reliable and consistent context for the tests. This could include __environment__ (for example a database configured with known parameters) or __content__ (such as a dataset).

- Return fixture: the fixture will return the value for the testing.
- Support to add the interable parameters for the fixture
- Setup and Teardown: the fixture support the feature to init at the begin of the tests and it also support to execute a function after the test finished.


# Test report


# Some notable knowledge

