# Integration with Python

## Introduction

This is a short description of the Python library to access the ecFeed online service. For the latest and full documentation of the ecfeed module, please refer to the docstring of the ecfeed module or check the sources directly at [github](https://github.com/ecfeed/ecfeed.python).  

Note, that the following introduction does not cover the ecFeed basics. Therefore, if you want to learn how to create a sample model and generate a personal keystore, visit the tutorial section on our [webpage](https://ecfeed.com/tutorials).

## Requirements

The module was developed and tested against Python 3.6. In theory, it should work with earlier versions of Python as well.

Prerequisites:
- Install [Python](https://www.python.org/downloads/).
- Download an IDE. For example [VSCode](https://code.visualstudio.com/).
- Create a test model on the ecFeed webpage (or use the default one).
- Generate a personal keystore named 'security.p12' and put it in the \~/.ecfeed/
 directory (Linux users) or in the \~/ecfeed/ directory (Windows users).  

## Installation

EcFeed module is hosted at the [PyPI](https://pypi.org/) repository and can be downloaded with the `pip` command:

```bash
pip install ecfeed
```

## Examples 

The examples assume that the user has a valid keystore downloaded to the '.ecfeed' folder ('ecfeed' in Windows) in his home directory and the accessed model contains called methods. The methods are available in a welcome model created at registration at the 'ecfeed.com' webpage. If the model is not there, it can be imported from [here](https://s3-eu-west-1.amazonaws.com/resources.ecfeed.com/repo/tutorial/Welcome.ect).

```python
from ecfeed import TestProvider, DataSource, TemplateType
ecfeed = TestProvider(model="XXXX-XXXX-XXXX-XXXX-XXXX")                                                         # The model ID.
for line in ecfeed.export_nwise(method='QuickStart.test', n=3, template=TemplateType.Gherkin, coverage=10):     # The name of the method.
   print(line)
```
```
Scenario: executing test
	Given the value of arg1 is <arg1>
	And the value of arg2 is <arg2>
	And the value of arg3 is <arg3>
	When test is executed

Examples:
| <arg1> | <arg2> | <arg3> | 
|      4 |      3 |      3 | 
|      1 |      3 |      4 | 
|      3 |      4 |      2 | 
|      3 |      3 |      1 | 
|      3 |      1 |      1 | 
|      2 |      1 |      1 | 
|      1 |      2 |      3 | 

```

Try and experiment with following:

```python
for line in ecfeed.export_pairwise(method='QuickStart.test', template=TemplateType.XML, coverage=10):
	print(line)
```
```python
for line in ecfeed.export_random(method='TestClass.method', length=5, duplicates=True, adaptive=True, template=TemplateType.CSV):
	print(line) 
```
```python
for line in ecfeed.export_static_suite(method='TestClass.method', test_suites=['suite1'], template=TemplateType.XML):
	print(line) 
```

Don't hesitate to modify the welcome model. It can be recreated easily and there is no better way to learn than hands-on exercises.  

However, have in mind that the ID of every model (including the welcome model) is unique. If you want to copy and paste the example, be sure to update it accordingly.  
 
## pytest

Pytest is one of most popular testing frameworks for Python, and luckily, it supports parameterized tests. Even more luckily, the format returned by ecFeed's TestProvider generators is directly usable for pydoc tests. And by some crazy coincidence, the util functions in TestProvider class can be used in pydoc's decorator to provide argument names:

```python
class TestedClass:
	@pytest.mark.parametrize(ecfeed.method_arg_names(method_name='QuickStart.test'), ecfeed.generate_random(method='QuickStart.test', length=5))
	def test_method_1(self, arg1, arg2, arg3):
		print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ')')
```

## Feedback

To send feedback, you need to have a BASIC account type or be a member of a TEAM.  

An example looks as follows:
```python
ecfeed = TestProvider(model='XXXX-XXXX-XXXX-XXXX-XXXX')
method = 'QuickStart.test'

@pytest.mark.parametrize(ecfeed.test_header(method, feedback=True), ecfeed.random(method=method, length=20, feedback=True))
def test_method_1b(arg1, arg2, arg3, test_handle):
    assert arg1 < 2, test_handle.add_feedback(False)
    test_handle.add_feedback(True)
```

To the 'test_header' method an additional argument, i.e. 'feedback=True', must be added. The same applies to any of the generation methods. Afterwards, in the parameter list, the 'test_handle' class must be included. It consists of one public method, namely 'add_feedback'. The required argument denotes the result of the test, everything else is optional.

```python
test_handle.add_feedback(True, comment='Passed', duration=1000 , custom={'key1': 'value1'})
```

_status_ - The result of the test.
_duration_ - The optional execution time in milliseconds.
_comment_ - The optional description of the execution.
_custom_ - The optional object of custom key-value pairs.

Additionally, to the test generation method one optional argument can be added, namely 'label'. It provides a short description of the generated test suite.  

Note, that each test must return a feedback, regardless whether it has passed or failed.  

# TestProvider class API

The ecFeed Python module provides connectivity with the ecFeed online test generation service using the class TestProvider. The class needs a keystore generated at the 'ecfeed.com' page to authenticate and identify the user at the generator service. 

## Constructor

The 'TestProvider' constructor takes one required and three optional arguments.

- *model (required)* - The model ID. The model ID is a 20 digit number (grouped by 4) that can be found in the *My projects* page at ecfeed.com under each model. It is also in an url of the model editor page opened on a model. By default it is `None`.
- *genserver* - The URL of the ecfeed generator service. By default it is 'gen.ecfeed.com'.
- *keystore_path* - The path to the keystore downloaded from 'ecfeed.com' webpage ('Settings' -> 'Security'). The keystore contains the user certificate which is needed to authenticate the user at the generator service. By default, the constructor looks for the keystore in \~/.ecfeed/security.p12, except for Windows, where the default path is \~/ecfeed/security.p12.
- *password* - The password to the keystore. The default value is 'changeit'.

An example call to construct a TestProvider object can look like this:
```python
import ecfeed

ecfeed = TestProvider(model='XXXX-XXXX-XXXX-XXXX-XXXX')
```
## Generator calls

TestProvider provides 11 generator functions to access ecfeed generator service. The function `generate` contains the actual code doing the call, but it is rather cumbersome in use, so the 10 other functions wrap it and should be used in the code. Nonetheless we will document this function as well. If a function name starts with the prefix `generate_`, the generator yields tuples of arguments casted to their types in the model. Otherwise (the prefix is `export_`) the functions yield lines of text, exported by the ecfeed service according to the chosen template. The only required parameter for all the generators is the _method_ parameter which must be a full name of the method used for the generation (full means including full class name).

### export_nwise(method, **kwargs) / generate_nwise(method, **kwargs)

A convenient way to call the nwise generator. 

- *method (required)* - Full name (including full class path) of the method that will be used for generation. Method parameters are not required. If parameters are not provided, the generator will generate data from the first method it finds with that name.
- *model* - The ID of the model used for generation. If not provided, the model set for the TestProvider object will be used.
- *n* - The 'N' in NWise. Default is 2
- *coverage* - The percent of N-tuples that the generator will try to cover. Default is 100%
- *template* - Template to be used when exporting data to text. If a function with the prefix `generate_` is invoked, data is always casted to argument type (regardless of the value of the template). Templates are defined by _TemplateType_ enum (supported values are RAW, CSV, JSON, Gherkin and XML). Check the docstring for ecFeed TemplateType (`pydoc.doc(ecfeed.TemplateType)`) to check all supported export templates. Default is 'CSV'.
- *choices* - Dictionary. The keys are names of method parameters. The values define list of choices that will be used for these parameters in the generation. If an argument is skipped in the dictionary, all defined choices will be used. For example: `choices={'arg1' : [choice1, choice2], 'arg2' : [choice3]}`.
- *constraints* - List of constraints used for the generation. If not provided, all constraints will be used. For example: `constraints=['constraint1',  'constraint2']`.

If a template is not provided, the function yields tuples of values casted to types defined by the signature of the function used for the generation. If a template is provided, the function yields lines of the exported data according to the template.

If the generator service responses with error, the function raises an _EcFeedError_ exception.

### export_pairwise(method, **kwargs) / generate_pairwise(method, **kwargs)

Calls _nwise_ with n=2. For people that like being explicit. Uses the same arguments as _nwise_, excluding 'n'.

### export_cartesian(method, **kwargs) / generate_cartesian(method, **kwargs)

Generates all possible combinations of parameters (considering constraints). Uses the same parameters as _nwise_, except 'n'.

### export_random(method, **kwargs) / generate_random(method, **kwargs)

Generates random combinations of method choices.

- *method* - See '_nwise_'.
- *template* - See '_nwise_'.
- *choices* - See '_nwise_'.
- *constraints* - See '_nwise_'.
- *model* - See '_nwise_'.
- *length* - Number of tests to be generated (1 by default).
- *duplicates* - If two identical tests are allowed to be generated. If set to false, the generator will stop after all allowed combinations are generated.
- *adaptive* - If set to true, the generator will try to provide tests that are farthest (in Hamming distance) from the ones already generated.

### export_static_suite(method, **kwargs) / generate_static_suite(method, **kwargs)

Downloads generated test cases (does not start the generator).

- *method* - See '_nwise_'.
- *template* - See '_nwise_'.
- *model* - See '_nwise_'.
- *test_suites* - A list of test case names to be downloaded.

## Other functions

Some other functions are provided to facilitate using TestProvider directly as data source in test frameworks like pytest.

### validate()

Verifies if the connection settings (including the keystore) are correct. If something is wrong, an exception is thrown.

### method_info(method, model=None)

Queries generator service for information about the method. Returns a dictionary with following entries:

- *package_name* - The package of the method, eg. 'com.example',
- *class_name* - Full name of the class, where the method is defined, e.g 'com.example.TestClass',
- *method_name* - full name of the method. Repeated from the argument,
- *args* - A list of tuples containing type and name of arguments, e.g. '[[int, arg1], [String, arg2]]'.

### method_arg_names(method_info=None, method_name=None)

Returns list of argument names of the method.

- *method_info*  - If provided, the method parses this dictionary for names of the method arguments.
- *method_name* - If method_info not provided, this function first calls method_info(method_name), and then recursively calls itself with the result.

### method_arg_types(self, method_info=None, method_name=None):

Returns list of argument types of the method.

*method_info* - See _method_arg_names_.
*method_name* - See _method_arg_names_.

## CLI

The generator can also be accessed from the command line, for example:

```bash
ecfeed --model XXXX-XXXX-XXXX-XXXX-XXXX --method QuickStart.test --cartesian
```

### Required arguments

These arguments must be always provided when invoking an ecfeed command.

- '*--model MODEL*' - ID of the accessed model.
- '*--method METHOD*' - Full name of the method used for generation tests. If the model contains only one method with this name, the argument types may be skipped. For example "--method com.test.TestClass.testMethod", or "--method com.test.TestClass.TestMethod(int, String)".
- '*--pairwise*' - Use pairwise generator. Equal to '*--nwise -n 2*'.
- '*--nwise*' - Use NWise generator.
- '*--cartesian*' - Use cartesian generator.
- '*--random*' - Use random generator.
- '*--static*' - Fetch pre generated tests from the server.

### Connection arguments 

Arguments related to connection and authorization to ecFeed server. In most cases the default option will be fine.

- '*--keystore KEYSTORE*' - Path of the keystore file. Default is "~/.ecfeed/security.p12".
- '*--password PASSWORD*' - Password to keystore. Default is "changeit".
- '*--genserver GENSERVER*' - Address of the ecfeed service. Default is "gen.ecfeed.com".

### NWise generator arguments

These arguments are valid only with the NWise generator.

- '*-n*' N - n in nwise.

### Random generator arguments

These arguments are valid only with the random generator.

- '*--length LENGTH*' -  Number of test cases to generate.
- '*--duplicates*' - If used, the same test can appear more than once in the generated suite.
- '*--adaptive*' - If used, the generator will try to generate tests that are furthest possible from already generated once (in Hamming distance).

### Static data arguments

These arguments are valid only with the '--static' option.

- '*--suites SUITES*' - list of test suites that will be fetched from the ecFeed service. If skipped, all test suites will be fetched.

### Other optional arguments

These arguments are valid with all or only some data sources.

- '*--template {CSV,XML,Gherkin,JSON}*' - Format for generated data. If not used, the data will be generated in CSV format.
- '*--choices CHOICES*' - Map of choices used for generation, for example {'arg1':['c1', 'c2'], 'arg2':['c3', 'abs:c4']}. Skipped arguments will use all defined choices. This argument is ignored for static generator.
- '*--constraints CONSTRAINTS*' - List of constraints used for generation, for example ['constraint1', 'constraint2']. If skipped, all constraints will be used. This argument is ignored for static generator.
- '*--coverage COVERAGE*' - Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered. Valid for pairwise, nwise and cartesian generators.
- '*--output OUTPUT, -o OUTPUT*' - Output file. If omitted, the standard output will be used.
- '*--url*' - Show the endpoint URL instead of generating test cases.