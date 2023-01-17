# ShodanWizard
This Shodan search wizard intends to improve your Shodan search with this simple yet helpfull python script that helps building queries and having results saved to a file.

Using this script you'll learn how to build the most effective Shodan queries for what you realy want as output. You can also learn how the Shodan API works with the official Shodan library for Python. 

## How to build better queries for your Shodan searches
By exploring the Shodan facets in this wizard, you'll be able to notice nuances that can fine tune your search and making a better usage of your API quota. You'll be able to add filters like country, city, domain, port, OS, ISP, product, version and even vulnerabilities through the facets options and testing the output before actually searching and spending your query credits.

## Usage
```
git clone https://github.com/rcbonz/ShodanWizard.git
```
```
cd ShodanWizard
```

```
pip install -r requirements.txt
```

```
python3 shodanSearch.py
```
Now you just answer the questions and boom. Done.



## Shodan

_"Shodan is a search engine that lets users search for various types of servers connected to the internet using a variety of filters. Some have also described it as a search engine of service banners, which are metadata that the server sends back to the client."_

Source: [Wikipedia](https://en.wikipedia.org/wiki/Shodan_(website))

You can buy a Shodan [membership](https://account.shodan.io/billing/member) for $49 (one-time payment) and it'll give you:
```
Query credits (per month) 	100
Scan credits (per month) 	100
Monitored IPs			16
Available search filters 	All except vuln and tag
Number of users 		1
Shodan Search pages 		20
```
Every 100 query result consumes 1 query credit and that was considered when this code was writen: you can choose the result count before proceeding with the search.

Check all options [here](https://account.shodan.io/billing)



## Screenshots of ShodanWizard working

![](https://github.com/rcbonz/ShodanWizard/blob/main/intro.png)

![](https://github.com/rcbonz/ShodanWizard/blob/main/facets.png)

![](https://github.com/rcbonz/ShodanWizard/blob/main/shared.png)

![](https://github.com/rcbonz/ShodanWizard/blob/main/output.png)

# DO NOT make the script angry. Or else it'll delete itself.

![](https://github.com/rcbonz/ShodanWizard/blob/main/badmofo.png)

