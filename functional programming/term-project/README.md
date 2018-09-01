# BLG 458E Course Term Project

# Uğur Uysal 150140012
# Trie implemantation


## Main.hs is same as code I uploaded to ninova.
## Main2.hs is unorganized version of my work.
## Trie.hs is the first draft of my work.
## I committed all my works here I tried to code tire with cpp first.
## Words.txt for testing my Trie


## What a lovely piece of code.
```haskell
getWords'::Trie->[String]
getWords' (Trie e c)
    | e         = ("" :) $ concat $ map (\(k,t) -> map (k:) $ getWords t) (Map.toList c)
    | otherwise =  concat $ map (\(k,t) -> map (k:) $ getWords t) (Map.toList c)
```