pcapEater
=========

pcapEater is a small and lazily written tool to extract, deduplicate and group HTTP GET/POST requests out from a supplied pcap file and dumps the requests to an output file.  

Can't you do this with tshark?
------------------------------

Yes, with a one-liner for the de-dupe. This was put together as a bolt-on for a larger framework of automation and just became its own thing - of course in an automation push you could still invoke tshark, but putting things altogether in python seemed cleaner. This is offered as something quick for one job and the dpkt usage can be easily extended to do whatever you want with. Go forth and improve it for your needs!  

Usage
-----

`python pcapEater.py -i $file.pcap [-p $port1,$port2] [-o $output_filename]`  

Dependencies
------------

+ argparse  
+ dpkt  

TODO
----

+ Re-write the whole thing sensibly. Code from over a year ago is always horrifying to review.  
+ Add the other HTTP methods, easy enough if not lazy.
