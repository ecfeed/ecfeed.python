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

## API documentation

For complete API documentation see docstring content of the ecfeed package. For example
```
import ecfeed
import pydoc
pydoc.doc(ecfeed)
pydoc.doc(ecfeed.TestProvider)
pydoc.doc(ecfeed.TestProvider.nwise)
```

