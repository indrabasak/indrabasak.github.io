---
layout: post
title: XML Processing with Hive XML SerDe
published: true
comments: true
tags: [Hadoop, Hive, XML]
image: /images/entry/hive.png
---

[Hive XML SerDe](https://github.com/dvasilen/Hive-XML-SerDe) is an XML processing library based on Hive 
[SerDe](https://cwiki.apache.org/confluence/display/Hive/SerDe)  (serializer / deserializer) framework. It relies 
on `XmlInputFormat` from Apache Mahout project to shred the input file into XML fragments based on specific start 
and end tags. You can find more about `XmlInputFormat` in "Hadoop in Practice". The XML SerDe queries the XML fragments
with XPath Processor to populate Hive tables. You can find the inner workings of this library 
[here](http://www.enggjournals.com/ijcse/doc/IJCSE14-06-09-012.pdf). In this posting, I will go over an example of 
XML processing in Hive using XML SerDe library. In our example, we will use the ebay data downloaded from University 
of Washington's [XML Data Repository](http://www.cs.washington.edu/research/xmldatasets/) site. 
Download the _ebay.xml_ file found [here](http://www.cs.washington.edu/research/xmldatasets/data/auctions/ebay.xml.gz); 
extract and store the file in a folder of your choice.

### Example

*   Download the latest version of _hivexmlserde.jar_ from [here](https://github.com/dvasilen/Hive-XML-SerDe/wiki/XML-data-sources) 
and copy it to your `/lib` folder.
*   In our example, the XML fragments are based on  and as the start and end tags respectively in 
the _ebay.xml_ file. Let's create the `ebay_listing` Hive table by executing the following CREATE TABLE 
Hive statement: 

{% gist b44b35d3619dce458df8aed7e11a4105 %}

*   If the table creation is successful, load the previously downloaded _ebay.xml_ file into the newly created Hive 
table by executing the following command (Note that the _ebay.xml_ is located in `C:/data/directory` in my example. 
You have to change the location accordingly):
```sql
LOAD DATA LOCAL INPATH 'C:/data/ebay.xml'
OVERWRITE INTO TABLE ebay_listing;
```

*   Once the data is loaded successfully, you can query the data.
```sql
SELECT seller_name, bidder_name, location, bid_history["highest_bid_amount"], item_info["cpu"]
FROM ebay_listing LIMIT 1;
```

### Comments

*   Though it's relatively easy to use, the table definition may take some time in getting used to.
*   I haven't checked the performance against a large XML file yet. I will update my post once I have the performance numbers.