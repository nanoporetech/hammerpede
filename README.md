Apps Python Package Boilerplate
===============================

Python package boilerplate based on a cleaned up version of the [auAdreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage) Cookiecutter template. Also incorporating bits and pieces from [tang](https://git.oxfordnanolabs.local/research/tang), [untangled](https://git.oxfordnanolabs.local/resdev/untangled) and [metrichor-bio/seed](https://git.oxfordnanolabs.local/metrichor-bio/seed).

Installation
------------

Install the package:

```
python setup.py install
```

Install the package in developer mode:

```
python setup.py develop
```

Run the tests:

```
make test
```

Build the documentation:

```
make docs
```

Issue `make help` to get a list of `make` targets.

Documentation
-------------

Documentation can be found at: https://apps.git.oxfordnanolabs.local/apps-pypackage-boilerplate

Contributing
------------

- Please fork the repository and create a merge request to contribute.
- Please respect the structure outlined in `scripts/_template_script.py` from command line tools so documentation can be generated automatically.
- Use [bumpversion](http://bit.ly/2cSUryt) to manage package versioning.
- The code should be [PEP8](https://www.python.org/dev/peps/pep-0008) compliant, which can be tested by `make lint`.
- For more guidance regarding coding style please refer to the [Tao of Tang](https://git.oxfordnanolabs.local/research/tang/blob/master/tao.md).

TODO
----
