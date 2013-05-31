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
- data options for a post method
- add hook options
- Overflow feature optional (zmq dependence)
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
