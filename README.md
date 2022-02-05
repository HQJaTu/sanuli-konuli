# sanuli-konuli
Solver for Finnish Wordly, Sanuli.

Code is generic and will work on any language. See class _KotusDictionary_
on how Finnish dictionary is handled.

# Workflow

## Import a dictionary (once)
As this works best with [Sanuli](https://sanuli.fi), there is an importer for
Finnish word list from Kotus. This dictionary can be downloaded and used freely
with LGPL-license at https://kaino.kotus.fi/sanat/nykysuomi/.

Utility `kotus-5-letter-words.py` will read the XML-file, parse it,
extract words from it and save all 5 letter words having no special characters.

```bash
usage: kotus-5-letter-words.py [-h] [--output-file OUTPUT_FILE] [--debug]
KOTUS-SANALISTA-V1-XML-FILE

Kotus word-list converter

positional arguments:
  KOTUS-SANALISTA-V1-XML-FILE
                        Finnish wordlist

optional arguments:
  -h, --help            show this help message and exit
  --output-file OUTPUT_FILE
                        Processed 5-letter words file. Default: kotus-
                        sanalista_v1.dat
  --debug               Make logging use DEBUG instead of default INFO.

```

This is a one-time task, resulting `.dat` file will be needed in later operations.

## Pick an initial word randomly

As there are no clues for the word, any word will do.

For best results, this code maximizes the attempt's footprint by selecting
a word with unique letters. To further optimize the initial attempt, in
save dictionary there is a set of "bad" letters which should never exist in an
initial word.

```bash
usage: get-initial-word.py [-h] [--debug]
                           PROCESSED-WORDS-DAT-FILE [EXCLUDED-LETTERS]

Get initial word from saved dictionary

positional arguments:
  PROCESSED-WORDS-DAT-FILE
                        Processed 5-letter words file.
  EXCLUDED-LETTERS      Set of letters the word must not have

optional arguments:
  -h, --help            show this help message and exit
  --debug               Make logging use DEBUG instead of default INFO.
```

An optional list of excluded letters can be given. This is for scenario where
your previous initial word didn't match anything, then your next initial word
must not have any of the excluded letters.

Note: When excluding a lot of letters, it is possible for zero initial words
to result. If this happens, a retry is done without "bad" letters and using
only given excluded letters.

## Match the results

```bash
usage: find-matching-word.py [-h] [--debug]
                             PROCESSED-WORDS-DAT-FILE MATCH-MASK
                             EXCLUDED-LETTERS [KNOWN-LETTERS]

Match clues from Wordly/Sanuli with a dictionary

positional arguments:
  PROCESSED-WORDS-DAT-FILE
                        Processed 5-letter words file.
  MATCH-MASK            5-letter match mask of known letters
  EXCLUDED-LETTERS      Set of letters the word must not have
  KNOWN-LETTERS         List of letters word must have

optional arguments:
  -h, --help            show this help message and exit
  --debug               Make logging use DEBUG instead of default INFO.
```

# Example Wordly game:
TBD

Lacking good English dictionary.

# Example Sanuli game:

Note: This sample game didn't produce any yellow clues.

## Round 1:
```bash
get-initial-word.py words/kotus-sanalista_v1.dat
```
**Initial word**: _HALKO_

**Result**: H and A are on green (correct letter, correct position),
L, K and O are on grey (word does not have those letters).

## Round 2:
Command to reflect Round 1 clues:
```bash
find-matching-word.py words/kotus-sanalista_v1.dat "ha..." "lko" "....."
```
**Attempt**: _HAIMA_

**Result**: H and both A are on green,
I and M are on grey.

## Round 3:
Command to reflect Round 2 clues:
```bash
find-matching-word.py words/kotus-sanalista_v1.dat "ha..a" "lkoim" "....."
```
**Attempt**: _HAUTA_

**Result**: H, U and both A are on green,
T is on grey.

## Round 4:
Command to reflect Round 3 clues:
```bash
find-matching-word.py words/kotus-sanalista_v1.dat "hau.a" "lkoimt" "....."
```
**Attempt**: _HAUVA_

**Result**: WIN!
