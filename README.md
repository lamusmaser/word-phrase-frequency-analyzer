# word-phrase-frequency-analyzer
A word and phrase frequency analysis tool



# Running Container
```
docker run --rm --pull always -v input:/app/input -v output:/app/output lamusmaser/word-phrase-frequency-analyzer:latest
```

Inside the `input` directory, you need to have all `input.txt` files and an `exceptions.txt`.
The analysis will be outputed into the `output` directory, one for each `input.txt`.