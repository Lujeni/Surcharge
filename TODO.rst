====
TODO
====

Overflow
--------
- check a communication between master <--> worker (bad worker, empty list of workers)
- display stats from the master. Hidden output for a worker
- comments in english
- unittesting

Surcharge
---------
- add hook options
- remove gevent dependence, use subprocess
- write an API
- python 3.0

Bug
---
- AttributeError: 'Greenlet' object has no attribute '_run'

Others
------
- gentoo package
- rewrite in C (Overflow and Surcharge)

Done
----
- improve the surcharge code (context processor) 0.7
- add Overflow feature 0.7
- error httpgevent.dns.DNSError in resolve function 0.7
- data options for a post method 0.7.2
- Overflow feature optional (zmq dependence) 0.7.2
- add Travis support 0.7.2

