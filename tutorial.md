## Introduction

This is a short description of python library to access ecfeed online service. For the latest and full documentation
of the ecfeed module, please refer to the docstring of the ecfeed module or check the sources directly at 
[github](https://github.com/ecfeed/ecfeed.python).

## Requirements

The module was developed and tested against python 3.6. In theory it should work with earlier versions of python as well.

## Installation

EcFeed module is hosted at pypi.org and can be simply downloaded with `pip` command:

```bash
pip install ecfeed
```
## Some examples 
The examples assume that the user has a valid keystore downloaded to '.ecfeed' folder ('ecfeed' in Windows) in his home directory and the accessed model contains called methods. The method should be available in a welcome model created at registration at ecfeed.com. If the model is not there it can be imported from here [TODO - add link to a welocme model].
```python
>>> from ecfeed import TestProvider, DataSource, TemplateType
>>> ecfeed = TestProvider(model='0168-4412-8644-9433-6380')#change model id to your model
>>> for line in ecfeed.nwise(method='QuickStart.test', n=3, template=TemplateType.Gherkin, coverage=10):
...		print(line)
...
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
for line in ecfeed.pairwise(method='QuickStart.test', template=TemplateType.XML, coverage=10):
	print(line)
```
```python
for line in ecfeed.cartesian(method='QuickStart.test', coverage=40, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
	print(line)
 ```
```python
for line in ecfeed.random(method='TestClass.method', length=5, duplicates=True, adaptive=True, template=TemplateType.CSV):
	print(line) 
```
```python
for line in ecfeed.static_suite(method='TestClass.method', test_suites=['suite1'], template=TemplateType.XML):
	print(line) ```
```
```python
for line in ecfeed.cartesian(method='QuickStart.test', coverage=40, choices={'arg1':['choice1'], 'arg3':['choice2', 'choice4']}): #No template!
 print(line)
 ```
 
 ## pytest
 Pytest is one of most popular testing frameworks for python, and luckily it supports parameterized tests. Even more luckily, the format returned by ecfeed's TestProvider generators (called with no templates) is directly usable for pydoc tests. And by some crazy coincidence, the util functions in TestProvider class can be used in pydoc's decorator to provide argument names:

```python
class TestedClass:
	@pytest.mark.parametrize(ecfeed.method_arg_names(method_name='QuickStart.test'), ecfeed.random(method='QuickStart.test', length=5))
	def test_method_1(self, arg1, arg2, arg3):
		print('method(' + str(arg1) + ', ' + str(arg2) + ', ' + str(arg3) + ')')
```

 
## TestProvider class API

The ecfeed python module provides connectivity with the ecFeed online test generation servide using the class TestProvider. The class needs a keystore generated at ecfeed.com page to authenticate and identify the user at the gen service. 

### Constructor

_TestProvider_ constructor takes 4 optional arguments:

_genserver_- The url to the ecfeed generator service. By default it is _gen,ecfeed.com_ and this should be fine with most cases.
_keystore_path_ - The path to a keystore downloaded from ecfeed.com (the Settings->Security page). The keystore contains user's certificate that is used to identify and authenticate the user at the generator service. Also, it contains generator's public key to validate the generator. By default the constructor looks for the keystore in `~/.ecfeed/security.p12`, except for Windows, where the default path is `$HOME/ecfeed/security.p12`
_password_ - Keystore password. The default value is 'changeit' and this is the password used to encrypt the keystore downloaded from ecfeed.com, so if it wasn't changed, the default value should be fine.
_model_ - The model id. The model id is a 20 digit number (grouped by 4) that can be found in the _My projects_ page at ecfeed.com under each model. It is also in an url of the mdoel editor page opened on a mdoel. By default it is `None`.

The gen service url, keystore location and password are constant and can't be changed in object's lifetime. The model id is accessible and mutable at any time. Also, the model id can be provided explicitly to a generation function each time. 

An example call to construct a TestProvider object can look like this:
```python
import ecfeed

ecfeed = TestProvider(model='0168-4412-8644-9433-6380')
```
### Generator calls

TestProvider provides 5 generator functions to access ecfeed generator service. The function `generate` contains the actual code doing the call, but it is rather cumbersome in use, so the 4 other functions wrap it and should be used in the code.i Nonetheless we will document this function as well. All the generators yield
different types depending on the value of the `template` parameter. If it is ommitted (or set to `None`), the generators yield tuples of arguments casted to their types in the model. Otherwise the functions yield lines of text, exported by the ecfeed service according to the chosen template. The only required parameter for all the generators is the _method_ parameter that must be a full name of the method used for the generation (full means including full class name).

#### nwise(method, **kwargs)
A convenient way to call nwise generator. 
_method_ - Full name (including full class path) of the method that will be used for generation. Method parameters are not required. If parameters are not provided, the generator will generate data from the first method it finds with that name

_n_ - The 'N' in NWise. Default is 2

_coverage_ - The percent of N-tuples that the generator will try to cover. Default is 100%

_template_ - Template to be used when exporting data to text. If set to `None` data will be casted to arument type. Templates are defined by _TemplateType_ enum (supported values are CSV, JSON, Gherkin and XML). Check the docstring for ecfeed.TemplateType (`pydoc.doc(ecfeed.TemplateType)`) to check all supported export templates. Default is 'CSV'.

_choices_ - Dictionary. The keys are names of method parameters. The values define list of choices that will be used for these parameters in the generation. If an argument is skipped in the dictionary, all defined choices will be used. For example: `choices={'arg1' : [choice1, choice2], 'arg2' : [choice3]}`.

_constraints_ - List of constraints used for the generation. If not provided, all constraints will be used. For example: `constraints=['constraint1',  'constraint2']`.

_model_ - The id of the model used for generation. If not provided, the model set for the TestProvider object will be used.

If a template was not provided, the function yields tuples of values casted to types defined by the signature of the function used for the generation. If a template was provided, the function yields lines of the exported data according to the template.

If the generator service resposes with error, the function raises _EcFeedError_ exception.


#### pairwise(method, **kwargs)

Calls nwise with n=2. For people that like being explicit. Uses the same arguments that _nwise_, excluding 'n'.

#### cartesian(method, **kwargs)
Gerenates all possible combinations of parameters (considering constraints). Uses the same parameters that _nwise_, except 'n'.

#### random(method, **kwargs)
Generates random combinations of method choices.
_method_ - see '_nwise_'.
_template_ - see '_nwise_'.
_choices_ see '_nwise_'.
_constraints_ - see '_nwise_'.
_model_ - see '_nwise_'.
_length_ - number of tests to be generated (1 by default).
_duplicates_ - If two identical tests are allowed to be generated. If set to false, the generator will stop after all allowed combinations are generated.
_adaptive_ - If set to true, the generator will try to provide tests that are farthest (in Hamming distance) from the ones already generated.

### Other functions
Some other functions are provided to facilitate using TestProvider directly as data source in test frameworks like pytest.

#### method_info(method, model=None)
Queries generator service for information about the method. Returns a dictionary with following entries:
'_package_name_' - the package of the method, eg. 'com.example',
'_class_name_' - full name of the class, where the method is defined, e.g 'com.example.TestClass',
'_method_nam_' - full name of the method. Repeated from the argument,
'_args_' - a list of tuples containing type and name of arguments, eg. '[[int, arg1], [String, arg2]]'.

#### method_arg_names(method_info=None, method_name=None)
Returns list of argument names of the method.

_method_info_  - If provided, the method parses this dictionary for names of the methid arguments.
_method_name_ - If method_info not provided, this function first calls method_info(method_name), and then recursively calls itself with the result.

#### method_arg_types(self, method_info=None, method_name=None):
Returns list of argument types of the method.
_method_info_ - see _method_arg_names_.
_method_name_ - see _method_arg_names_.
sively calls itself with the result


