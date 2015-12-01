# pageview-api
Wikimedia Pageview API client

Installation
------------
In order to install system wide on system using sudo you can use:
```sh
pip install attrdict
git clone https://github.com/Commonists/pageview-api
cd pageview-api
sudo python pageview-api install
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

Sum of view during last 30, 60, 90 days
```python
import pageviewapi.last
pageviewapi.last.last30('en.wikipedia', 'Paris', access='all-access', agent='all-agents')
```
