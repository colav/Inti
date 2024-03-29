<img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/>

# Inti
Capture system from non scrapping data sources

# Description
Package to download data and process datasets, not related to scrapping, like Microsoft Academic MAG and Scielo.
For MAG, this package allows to download the data from azure and in parallel, dumps the data to MongDB collections.
This allows too, create indexes for ElasticSearch database to perform search using the title of the document.

# Azure account
https://docs.microsoft.com/en-us/academic-services/graph/get-started-setup-provisioning

# Installation

## Dependencies
* Install MongoDB:
    * Debian Based systems: `apt install mongodb`
    * RedHat Based systems: [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)
* Install ElasticSearch: [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
* The other dependecies can be installed with pip installing this package.

## Package
`pip install inti`

## MongoDB requirement
Very importan for MA, other way it won't work.
https://docs.mongodb.com/manual/reference/ulimit/
max opened files have to be updated.

# Usage
## Exaple running save MAG in MongoDB
`
inti_maloader --ma_dir=/storage/colav/mag_sample/ --db=MA --all
`

## Exaple running save MAG in ElasticSearch
`
 inti_maesloader --mag_dir=/home/colav/mag/ --col_name=Papers --field_name=PaperTitle --index_name=mag 
`

# MongoDB Options requirement
There is a special requirement for mongodb server to allow run multithread sessions
To avoid the error 
`
ok" : 0,
 "errmsg" : "cannot add session into the cache",
 "code" : 261,
 "codeName" : "TooManyLogicalSessions",
`

you need to start the server with the option

`
mongod --setParameter maxSessions=10000000 --config /etc/mongodb.conf
`
# ElasticSearch Options requirement
in the file /etc/elasticsearch/elasticsearch.yml add

`
thread_pool.get.queue_size: 10000
`

`
thread_pool.write.queue_size: 10000
`

## ElasticSearch disk options
With low disk space, this error can appear 

`
('1 document(s) failed to index.', [{'index': {'_index': 'mag', '_type': '_doc', '_id': '9915517', 'status': 429, 'error': {'type': 'cluster_block_exception', 'reason': 'index [mag] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block];'}, 'data': {'PaperTitle': '...'}}}])
`

solver it with this.

`
curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
`

`
curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'
`



# MongoDB optimizations
increase the index creation memory to 6G of RAM to improve the performance(use this with caution)

`
db.adminCommand({getParameter: 1, maxIndexBuildMemoryUsageMegabytes: 1})
`

`
db.adminCommand({setParameter: 1, maxIndexBuildMemoryUsageMegabytes: 6144})
`

## Final notes
Be aware that running this package, mongodb producess a huge amount of informtation in the logs,
please clean the file /var/log/mongodb.log (it could be more that 65G)

**This is required to perform massive insertions in parallel!**

# License
BSD-3-Clause License 

# Links
http://colav.udea.edu.co/
