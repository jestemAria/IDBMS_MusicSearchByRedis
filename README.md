# IDBMS_MusicSearchByRedis
IDBMS Course - Making platform for upload and search for music

Database Implementation Course.  
Professor D. MohammadPour.  
Jul 30, 2021  

## Summary
This project is a platform for Upload-And-Search music.  
It is Created with Python and Redis database about October 10, 2020  
It is NOT completed yet!  


## How to install
1. At first, clone the Project.
2. Then, you should download Redis if you don't have it.  
> For downloading Redis just use the following commands:  

```shell
mkdir redis && cd redis
$ curl -O http://download.redis.io/redis-stable.tar.gz
$ tar xzvf redis-stable.tar.gz
$ cd redis-stable
$ make
$ make test
$ sudo make install
```

3. Install required libraries using following command:
```shell
$ pip install -r requirements.txt
```
4. For starting Redis, use the following code:
```shell
$ redis-server
```
> this would start redis server to accept connections.
