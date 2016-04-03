# pageview-api
[![Build Status](https://travis-ci.org/Commonists/pageview-api.svg?branch=master)](https://travis-ci.org/Commonists/pageview-api)
[![Code Health](https://landscape.io/github/Commonists/pageview-api/master/landscape.svg?style=flat)](https://landscape.io/github/Commonists/pageview-api/master)
[![License](http://img.shields.io/badge/license-MIT-orange.svg?style=flat)](http://opensource.org/licenses/MIT)

Wikimedia Pageview API client

Installation
------------
In order to install system wide on system using sudo you can use:
```sh
pip install git+https://github.com/Commonists/pageview-api.git
```

Examples
--------

Number of view on English Wikipedia of article Paris from November 6th to November 20th 2015

```python
import pageviewapi
pageviewapi.per_article('en.wikipedia', 'Paris', '20151106', '20151120',
                        access='all-access', agent='all-agents', granularity='daily')
```

Aggregation: Get a daily pageview count timeseries of all projects for the month of October 2015
```python
import pageviewapi
pageviewapi.aggregate('fr.wikipedia', '2015100100', '2015103100', access='all-access',
                      agent='all-agents', granularity='daily')
```

Most viewed articles on French Wikipedia on November 14th, 2015
```python
import pageviewapi
pageviewapi.top('fr.wikipedia', 2015, 11, 14, access='all-access')
```

Sum (resp. average) of view during last 30 days
```python
import pageviewapi.period
pageviewapi.period.sum_last('fr.wikipedia', 'Paris', last=30,
                            access='all-access', agent='all-agents')

pageviewapi.period.avg_last('fr.wikipedia', 'Paris', last=30)
```
