# word-phrase-frequency-analyzer
A word and phrase frequency analysis tool


# Running Container

```
docker run --rm --pull always -v "input.txt":/app/input.txt -v "output.txt":/app/word_frequency_analysis.txt -v "exceptions.txt":/app/exceptions.txt lamusmaser/word-phrase-frequency-analyzer:latest
```