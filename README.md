# pageview-api
Wikimedia Pageview API client

Examples
--------

Number of view on English Wikipedia of article Paris from November 6th to November 20th 2015

```python
import pageviewapi
pageviewapi.per_article('en.wikipedia', 'Paris', '20151106', '20151120')
```

Most viewed articles on French Wikipedia on November 14th, 2015
```python
import pageviewapi
pageviewapi.top('fr.wikipedia', 2015, 11, 14)
```
