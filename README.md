# Doodling Data Cards

Repo supporting the Doodling Data Cards project ([twitter](https://twitter.com/DoodleDatCard), [Instagram](https://www.instagram.com/doodledatcard/)), code and data used for the cards here. Also contains some work that has not gone into cards (yet?) but is discussed here and there (blog posts usually).


## Common

This just a collection of functions to help with workflow in the notebooks/scripts.

-----

## EU

Data about the European Union.

### Eurostat population age structure

Having a look at the data retrieved from Eurostat about the population totals and age structure in the European Union in the years.
This has been mainly done to produce a data card, the notebook is meant for manipulating/reformatting the data.

### Population area

Data on area (surface) and population of european countries, retrieved from Wikipedia.

### Employment rates by gender

Only data, from Eurostat, used for a card

-----

## Food & Drinks

Data regarding food & drinks.
* cocktails - data on the IBA cocktails

-----

## Linguistics

### Quantifying natural languages

Can we measure natural language, can we quantify it? Can we also compare different natural languages, say English and Spanish?

-----

## Culture

### Literature
Some data over literary texts.

* fleming - all of Fleming's series on Bond

### TV shows

-----

## Nature
Data about nature.
* animals - contains the list of mammals by population, from Wikipedia
* plants - plant taxonomy datasets and exploration, from the [GBIF](https://www.gbif.org/)
* virus - data about the [ICTV virus classification/taxonomy](https://talk.ictvonline.org/taxonomy/) with notebook analysis of families and species

-----

## Public Health
Some data on public health.
* epidemics - timeline of epidemics from Wikipedia

-----

## Society

### Births

Number of births each month in some countries, UN database data. For a data card.

### Human Progress
Data collected as part of the reading of S. Pinker's book "Enlightenment now".

### Racism
Police response at the 2020 protests after George Floyd's death.

-----

## Sport
Data about some sports. Whether stuff I've done or someone else or international events.

### EMF2019
Edinburgh's Marathon 2019 - which I partake to.

### Football

#### World Cup

Data and work about the FIFA world cups.

#### Team stats

Mainly for a data card, looks at the number of matches played and cards obtained by players in the Football World Cup, over all editions.

#### History stats

Stats in time.

#### Players

Data for the players who played in the 2018 Russia World Cup, about their 2017/2018 season. See details in folder.



## Stack Overflow tags

If we fetch some data about question tags on Stack Overflow, what patterns do we see?



## Travel

Data about travelling to places.

### Instagram

Contains data taken from Instagram about places/cities etc.

#### cities hashtags

Number of posts per city, with city name in different languages, to proxy how visited they are (not just tourism clearly, will be also work travels) - used EN, IT, FR, DE, ES, PT as languages and some important in Europe (to avoid missing data, cities from other languages are not there); data taken 6/11/2018

Also, sometimes there is hashtag like #london:<uk-flag>, these have also taken, see the file. Sure there will be other possibilities but weren't considered. ALso note hashtags are not case-sensitive. Also note that posts can be tagged with multiple hashtags so there is the possibility that counts are duplicated

All data is manually taken, was too much of a pain to do via APIs & stuff for such a small thing. Obvs we know that there'll be loads of spurious posts not depicting the city and tagged with hashtag, that's why this is rough.
