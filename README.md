# What is SLASH?

__Slash__ is a testing framework written in Python.

Unlike many other testing frameworks out there, Slash focuses on building in-house testing solutions for large projects.

It provides facilities and best practices for testing complete products, and not only unit tests for individual modules.

- [Get Started](#get-started)
- [Running test](#running-test)
- [Test fixture](#test-fixture)
- [Test coverage](#test-coverage)
- [.slashrc](#slashrc)
- [Hooks](#hooks)
- [Tags](#tags)
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

1. __Run the test:__
```bash
slash run test_addition.py
```

2. __Debugging:__ You can debug failing tests using the `--pdb` flag, which automatically runs the best available debugger on exceptions. You can also filter the exceptions which run the debugger by using `--pdb-filter` in addition to the `--pdb` flag.

3. __Assertions and Errors:__ Tests make sure things are like they expect with `assert` keyword.
```python
# test_addition.

def test_addition():
    assert 2 + 2 == 4
```

4. __Test Parameters:__ Slash tests can be parametrized, iterating parameter values and __creating separate cases__ for each value:
```python
@slash.parametrize('x', [1, 2, 3])
def test_something(x):
    # use x here
```
- For boolean values, a shortcut exists for __toggling between True and False__:
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

5. __Logging:__ Slash uses [Logbook](https://logbook.readthedocs.io/en/stable/) for logging and exposes __a global logger__:
```python
import slash

def test_1():
    slash.logger.debug("Hello!")
```
- By default logs above WARNING get emitted to the console when slash run is executed. You can use `-v`/`-q` to increase/decrease console verbosity accordingly.

- By default logs are not saved anywhere. This is easily changed with the `-l` flag to `slash run`. Point this flag to a directory, and Slash will organize logs inside, in subdirectories according to the session and test run (e.g. `/path/to/logdir/session_id/test_id/debug.log`).

6. __Cleanups:__ Adding cleanups is done with `slash.add_cleanup()`.
```python
def test_product_power_on_sequence():
    product = ...
    product.plug_to_outlet()
    slash.add_cleanup(product.plug_out_of_outlet)
    product.press_power()
    slash.add_cleanup(product.wait_until_off)
    slash.add_cleanup(product.press_power)
    slash.add_cleanup(product.pack_for_shipping, success_only=True)
    product.wait_until_on()
```

7. __Skips:__ We can skip tests by raising the `SkipTest` exception, or by simply calling `slash.skip_test()` function.
```python
def test_microwave_has_supercool_feature():
    if microwave.model() == "Microtech Shitbox":
        slash.skip_test("Microwave model too old")
```
- Slash also provides `slash.skipped()`, which is a decorator to skip specific tests:
```python
@slash.skipped("reason")
def test_1():
    # ...

@slash.skipped # no reason
def test_2():
    # ...
```
- In some cases you may want to register a custom exception to be recognized as a skip. You can do this by registering your exception type first with `slash.register_skip_exception()`.

8. __Requirements:__
```python
def is_some_condition_met():
    return True

@slash.requires(is_some_condition_met)
def test_something():
    ...

@slash.requires(is_some_condition_met, message='My condition is not met!')
def test_something():
    ...
```

9. __Storing Additional Test Details:__ Store some objects that may help investigation in cause of failure.
```python
def test_one():
    slash.set_test_detail('log', '/var/log/foo.log')
    slash.set_error("Some condition is not met!")

def test_two():
    # Every test has its own unique storage, so it's possible to use the same key in multiple tests
    slash.set_test_detail('log', '/var/log/bar.log')
```

10. __Tests Repeat:__
```python
@slash.repeat(5)
def test_probabilistic():
    assert still_works()
```
- You can also use the `--repeat-each=X` argument to slash run, causing it to repeat each test being loaded a specified amount of times, or `--repeat-all=X` to repeat the entire suite several times.

# Running test
[References](https://slash.readthedocs.io/en/master/slash_run.html#slash-run)

1. __Default:__
```bash
slash run /path/to/tests
```

Stopping at the __first unsuccessful test__ with the`-x` flag.

2. __Loading Tests from Files:__
```bash
slash run -f file1.txt -f file2.txt
```
Lines in suite files can optionally contain filters and repeat directive.

Filter allows restricting the tests actually loaded from them:
```
# my_suite_file.txt

# this is the first test file
/path/to/tests.py

# when running the following file, tests with "dangerous" in their name will not be loaded
/path/to/other_tests.py # filter: not dangerous
```
Repeat allows to repeat a line:
```
# my_suite_file.txt

# the next line will be repeated twice
/path/to/other_tests.py # repeat: 2

# you can use filter and repeat together
/path/to/other_tests.py # filter: not dangerous, repeat: 2
```

3. __Running Interactively:__ If we need to interact with the program in an interactive IPython shell.
```bash
slash run -i /path/to/tests
```

4. __Including and Excluding Tests:__
Only run tests containing the substring in their names:
```bash
slash run -k substr /path/to/tests
```
Use `not X` to exclude any test containing `X` in their names:
```bash
slash run -k 'not failing_' /path/to/tests
```
Use a more complex expression involving or and and:
```bash
slash run -k 'not failing_ and components' /path/to/tests
```

5. __Overriding Configuration:__
```bash
slash run -o path.to.config.value=20 ...
```

6. __Resuming Previous Sessions:__
```bash
slash resume -vv session_id
```

7. __Rerunning Previous Sessions:__
```bash
slash rerun -vv session_id
```

# Test fixture

In testing, a __fixture__ provides a defined, reliable and consistent context for the tests. This could include __environment__ (for example a database configured with known parameters) or __content__ (such as a dataset).

- Return fixture: the fixture will return the value for the testing.
- Support to add the interable parameters for the fixture
- Setup and Teardown: the fixture support the feature to init at the begin of the tests and it also support to execute a function after the test finished.

__Slash Fixture Scope:__ We say that fixtures, by default, have a __scope of a single test__, or __test scope__. Slash also supports __session__ and __module__ scoped fixtures. Session fixtures live from the moment of their activation until the end of the test session, while module fixtures live until the last test of the module that needed them finished execution.
```python
@slash.fixture(scope='session')
def some_session_fixture(this):
    @this.add_cleanup
    def cleanup():
        print('Hurray! the session has ended')


@slash.fixture(scope='module')
def some_module_fixture(this):
    @this.add_cleanup
    def cleanup():
        print('Hurray! We are finished with this module')
```
Test Start/End for Widely Scoped Fixtures done via the `this.test_start` and `this.test_end` callbacks, which are specific to the current fixture.
```python
@slash.fixture(scope='module')
def background_process(this):
    process = SomeComplexBackgroundProcess()

    @this.test_start
    def on_test_start():
        process.make_sure_still_running()

    @this.test_end
    def on_test_end():
        process.make_sure_no_errors()

    process.start()

    this.add_cleanup(process.stop)
```

__Listing Available Fixtures:__
```bash
slash list –only-fixtures path/to/tests
```

# Test coverage
Slash has a built-in plugin to report coverage, using [Coverage.py](https://coverage.readthedocs.io/en/7.2.7/).

To use it, run Slash with `--with-coverage`, and optionally specify modules to cover:
```bash
slash run --with-coverage --cov mypackage --cov-report html
```

_See also: [Other Built-in Plugins](https://slash.readthedocs.io/en/master/builtin_plugins.html)._

# .slashrc
Slash loads the `.slashrc` file when it loads.

`.slashrc` file has to be placed at the root directory of the repo or the project.

Slash uses a hierarchical configuration structure provided by confetti.

In `.slashrc` file, we can set value for the slash config value, extend config and provide our own config.

The config is located in `slash.config` object and all slash config is under `slash.config.root`.

```python
# Example of .slashrc file

import os
import slash
from confetti import Config
import plugin

slash.config.root.log.root = os.path.join(os.path.dirname(__file__), 'log')
slash.config.root.run.default_sources = ['feature_one', 'feature_two']
# slash.config.root.log.show_raw_param_values = True
slash.config.root.log.unified_session_log = True

slash.config.extend(
    Config(
        {'cluster': {'ip': "10.0.0.4", "username": "root"}}
    )
)

```

_See: [List of Available Configuration Values](https://slash.readthedocs.io/en/master/configuration.html#configuration)_

# Hooks
__Hooks__ are endpoints to which you can register callbacks to be called in specific points in a test session lifetime.

All built-in hooks are all kept as globals in the `slash.hooks` module

To register a method to be executed in specific point:
- The method has to be decorated as `@slash.hooks.hook_nmae.register`

_See: [Available Hooks](https://slash.readthedocs.io/en/master/configuration.html#configuration)_

# Tags
Slash supports organizing test by tagging them:
```python
@slash.tag('dangerous')
def test_something:
    ...
```

You can also make alias for tags:
```python
dangerous = slash.tag('dangerous')

@dangerous
def test_something:
    ...
```

Tags can also have values:
```python
@slash.tag('covers', 'requirement_1294')
def test_something:
    ...
```

Running tests filtered by tags:
```bash
slash run /path/to/tests -k 'not tag:dangerous'
```
```bash
slash run /path/to/tests -k 'tag:covers=requirement_1294'
```

# Some notable knowledge
- [Logging](https://slash.readthedocs.io/en/master/logging.html#logging) (Logs timestamps, color, highlights,... )
- [Assertions, Exceptions and Errors](https://slash.readthedocs.io/en/master/errors.html#errors)
- [Handling and Debugging Exceptions](https://slash.readthedocs.io/en/master/errors.html#exceptions)
- [Test Parametrization](https://slash.readthedocs.io/en/master/parameters.html#parameters)
- [KeyboardInterrupt](https://slash.readthedocs.io/en/master/errors.html#keyboardinterrupt)
