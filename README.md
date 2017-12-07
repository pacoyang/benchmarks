# Network Server Performance Benchmarking

Reference to [toolbench](https://github.com/MagicStack/vmbench). I create my own tool to benchmark the performance of HTTP protocol of a variety of server frameworks.

## Environment
- Python 3.6
- Node 8.7.0
- PHP 7.2

Macbook Pro 2.6 GHz Intel Core i5, only run one process

# Result
wrk -t12 -c300 -d30s

Framework | Req/s
---- | ---
aiohttp | 3342.28
aiohttp + uvloop | 5432.48
tornado | 1666.53
node.js | 17961.25
express | 10343.15
swoole | 54802.21

