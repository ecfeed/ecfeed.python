# ecfeed.python
This library provides API to access ecfeed service from python code. Additionally it contains a command line 
utility to eccfedd ecfeed from a console. 

## Introduction
EcFeed online service provides REST API so that odels defined in the online tool can be accessed 
and used for test generation. Also tests that are generated in the online tool and stored in the 
model can be downloaded and used for tests locally. This library provides user friendly way to access 
the generated data from python code.

## Requirements
EcFeed library is built and tested with Python 3.6, althought it should work with earlier versions of Python 3. 
The only dependency is pyopenssl

## Installation
```
pip3 install ecfeed
```
## Keystore
EcFeed service identifies the user using a certificate provided by user. The certificate can be created at ecfeed.com (_account settings->Security_).

## Quick start
For complete API documentation see docstring content of the ecfeed package, here we will just show the basic functionality
provided by the package. We will use the default model that is created for new users at ecfeed.com. By default it is named 'Tutorial'

### Using the API

 Type in your python console:
```
import ecfeed
import pydoc
pydoc.doc(ecfeed)
pydoc.doc(ecfeed.TestProvider)
pydoc.doc(ecfeed.TestProvider.nwise)
```

First we need to create TestProvider object. In most cases it should work fine with default parameters. We can however 
provide it with the model we want to access, so we do not have to do it explicitly each time we want to use a generator function. The model it can be found on the _My Models_ section of the ecfeed.comm on the page. The code for instantiating the TestProvider will look like this:

```python
>>> from ecfeed import TestProvider, TemplateType, DataSource #TemplateType, DataSource will be used later

>>> provider = TestProvider(model='0168-4412-8644-9433-6380')
```
Requesting data from the ecfeed service can be done using one of four generator functions provided by TestProvider class:
_cartesian_, _nwise_, _random_ and _static_suite_. Each of them requests different type of generation. By default, the
genrator will return a tuple of values, casted to a type defined in the model (_int_, _float_, _string_ or _boolean_).

```python
>>> for line in provider.cartesian(method='com.example.test.QuickStart.test'):
...     print(str(line))

[0, 0, 0]
[0, 0, 1]
[0, 1, 0]
[0, 1, 1]
[1, 0, 0]
[1, 0, 1]
[1, 1, 0]
[1, 1, 1]

```

The other format how the data can be returned is test, according to a predefined template. We will generate pairwise combinations from 10^10 function (10 parameters of 10 possible values), that cover 10% of all pairs:

```python

>>>for line in provider.nwise(method='com.example.test.Playground.size_10x10', n=2, coverage=10, template=TemplateType.CSV):
...     print(str(line))
...
a,b,c,d,e,f,g,h,i,j
a1,b0,c4,d4,e8,f8,g0,h4,i7,j0
a6,b3,c2,d9,e6,f6,g7,h3,i4,j5
a7,b4,c5,d5,e8,f0,g9,h7,i3,j7
a1,b5,c2,d6,e3,f5,g1,h6,i3,j2
a2,b8,c3,d8,e4,f5,g5,h0,i6,j0
a1,b8,c6,d9,e0,f0,g8,h9,i0,j1
a7,b0,c8,d2,e0,f3,g4,h1,i8,j3
a4,b9,c9,d7,e1,f8,g2,h7,i9,j6
a5,b6,c0,d6,e4,f1,g7,h4,i2,j1
a5,b4,c4,d1,e1,f9,g6,h8,i1,j3
```

By default all choices and all constraints we defined for the method in the model will be considered during generation. 
We can restrict that. In this example we will generate 4 random combinations of parameters of the method
`com.example.test.LoanDecisionTest1.generateCustomerData`. We will tel the generator to use only some of the choices for certain parameters and some of the constraints we defined for the method in the model.

```python
for line in provider.random(method='com.example.test.LoanDecisionTest1.generateCustomerData', length=4, template=TemplateType.XML, constraints=['gender'], choices={'gender':['male']}):
...   print(str(line))
...
<TestCases>
	<TestCase testSuite="" familyName="Mendhelsson-Bartholdy" firstName="Alexander" gender="MALE" age="35" documentSerialNumber="[A-Z]{2}[0-9]{9}" documentType="DRIVERS_LICENSE" />
	<TestCase testSuite="" familyName="Rockefeller" firstName="Jean Pierre" gender="MALE" age="87" documentSerialNumber="B9819484" documentType="PASSPORT" />
	<TestCase testSuite="" familyName="Rockefeller" firstName="John" gender="MALE" age="40" documentSerialNumber="WNZ379009" documentType="PERSONAL_ID" />
	<TestCase testSuite="" familyName="van der Sar" firstName="John" gender="MALE" age="80" documentSerialNumber="[A-Z]{2}[0-9]{9}" documentType="PERSONAL_ID" />
</TestCases>
```









