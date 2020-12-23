[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cbe9dad067f94b799d4b5d79ab913a4e)](https://www.codacy.com/gh/colav/Inti?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=colav/Inti&amp;utm_campaign=Badge_Grade)

# Inti
Capture system from non scrapping data sources

# Exaple running save MAG in MongoDB
`
python3 run_mamagloader.py --mag_dir=/storage/colav/mag_sample/ --db=MA
`

# DB Options requirement
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