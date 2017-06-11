# get-yahoo-quotes-python

A Python script to download Yahoo quotes which works with the new cookie authorized page.

This repo has an associated blog post available here:

[http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/](http://blog.bradlucas.com/posts/2017-06-03-yahoo-finance-quote-download-python/)


## Create a virtual environment

```
$ virtualenv env
$ source ./env/bin/activiate
$ pip install requests
```

## Usage

Run the script with the symbol you'd like as a parameter. The script will download to a cvs file named with the symbol.

```
python get-yahoo-quotes.py SYMBOL
```
