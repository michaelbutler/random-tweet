# random-tweet

Get a random tweet from Twitter based on an input keyword.

## Prerequisites:

- Python 3.x (developed on 3.4.3+)
- Some pip libraries, installable with the command below
- File named `credentials` in same directory, containing twitter key & secret separated by line break (\n)

Run `pip install -r requirements.txt` to install these dependencies.

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


## Tests

To run basic tests,

```
./run_tests.sh
```

## License

MIT License
