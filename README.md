# random-tweet

Get a random tweet from Twitter based on an input keyword.

## Prerequisites:

- Python 3.x
- httplib2==0.9.2
- requests==2.9.1
- urllib3==1.14
- File named "credentials" in same directory, containing twitter key & secret separated by line break (\n)

Use pip install -r requirements.txt to install dependencies.

Example credentials file:

```
anbckdfiiettddv
NBD120fkdfipODeffNBDf334kdfipODe554ff
```

Visit https://apps.twitter.com/ to get your API key and secret strings.

## Usage:

```
python random_tweet.py <search_term>
```

## Example:

```
python random_tweet.py apple
```

## Example Output:

```
@username_here: An apple a day #try2 #crashed (@ 11 Penn Plaza in New York, NY) https://t.co/yyy https://t.co/zzz
media: https://pbs.twimg.com/media/Cb1eILsWAAAXmDj.jpg
```

## License

MIT License