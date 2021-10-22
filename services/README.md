# MongoDB service

The mongodb.service for systemd supports numa and 140k max opened files
install it on  /lib/systemd/system/mongodb.service 

# MongoDB conf 

Add the next options for xfs and bind ip in any network interface in the file /etc/mongodb.conf

`

dbpath=/xfs/lib/mongodb

logpath=/xfs/log/mongodb/mongodb.log

bind_ip = 0.0.0.0

`

# ElasticSearch

Added the next options at the end of the file /etc/elasticsearch/elasticsearch.yml

`
thread_pool.get.queue_size: 10000 
thread_pool.write.queue_size: 10000

transport.host: localhost 
transport.tcp.port: 9300 
http.port: 9200
network.host: 0.0.0.0
`