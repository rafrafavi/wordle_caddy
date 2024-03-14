# Quick overview
Use an interactive *console* to search for words in the 'original' Wordle word bank. 

For example, suppose you want to find all words starting with `f` and ending with `e`, enter:
```
(wordle ) find f...e
```
:warning: `find` always searches **all** words and resets previous searches
> **tip**: always enter lowercase characters.

To search within the previous result:
```
(wordle ) sub .a...
```
If you want to search within those results for words not containing certain characters (e.g. `x` and `y`),  then enter:
```
(wordle ) not xy
```
If you want to search within those results for words  containing certain characters (e.g. `a` and `e`), but you don't know where in the word they are (i.e. yellow clue), then enter:
```
(wordle ) contains ae
```
If you want to search within previous results for words not containing a given character in a given position  (e.g. no `e` as the second character), then enter:
```
(wordle ) sub .[^e]...
```
> yes, all python regex syntax supported

One last (free form) feature is the ability to to do a sub search but *not* store it as the previous search. 

For example, suppose you want help picking a guess starting with `r`, but you don't know for sure that the target word contains an `r`, then enter:
```
(wordle ) suggest r....
```

Finally, there is an intelligent searcher that finds all constraints from a given wordle output (🔴 **beta**).

It takes a textual representation of the clues (green, gray, yellow) and provides the most constrained list of words possible.

For example, suppose you guessed `crane` and got an exact match (`+` or `x`) and a partial hit (`?` or `o`), with the rest misses (`-` or `.` or `_`), enter:

```
(wordle ) ipick crane:+-?-- 
```
>meaning given the guess **crane**, the Wordle target word contains `c` in the same position as the guess, `a` in the wrong position, and does not contain `r`, `n`, `e`

:warning: pay attention to the colon between the guess and the score

#### Sample output:
```
(wordle ) ipick other:o--xx
['boxer', 'buyer', 'defer', 'ember', 'fewer', 'foyer', 'joker', 'mower', 'odder', 'offer', 'poker', 'poser', 'power', 'purer', 'queer', 'refer', 'roger', 'rower', 'ruder', 'sewer', 'sober', 'sower', 'super', 'surer', 'udder', 'upper', 'wooer'] 27
```
> lists words matching the search (and all previous searches) followed by the count of matching words.

> **Note:**  `ipick` may perform multiple searches while seeking the best matches.