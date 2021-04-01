<img src="https://raw.githubusercontent.com/colav/colav.github.io/master/img/Logo.png"/>

# Inti
Capture system from non scrapping data sources

# Description
Package to download data and process datasets, not related to scrapping, like Microsoft Academic MAG and Scielo.
For MAG, this package allows to download the data from azure and in parallel, dumps the data to MongDB collections.
This allows too, create indexes for ElasticSearch database to perform search using the title of the document.

# Installation

## Dependencies
* Install MongoDB:
    * Debian Based systems: `apt install mongodb`
    * RedHat Based systems: [here](https://docs.mongodb.com/manual/tutorial/install-mongodb-on-red-hat/)
* Install ElasticSearch: [here](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
* The other dependecies can be installed with pip installing this package.

## Package
`pip install inti`

# Usage
## Exaple running save MAG in MongoDB
`
inti_mamagloader --mag_dir=/storage/colav/mag_sample/ --db=MA
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
thread_pool.write.queue_size: 10000
`

# MongoDB optimizations
increase the index creation memory to 6G of RAM to improve the performance(use this with caution)
`
db.adminCommand({getParameter: 1, maxIndexBuildMemoryUsageMegabytes: 1})
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
