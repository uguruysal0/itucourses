module Kod where 

import qualified Data.Map as Map
import qualified Data.Char as Char

type MyWord = String
type Sentence = [MyWord]
type Count = Map.Map Char Integer



concatMaps::[Count] -> Count -> Count
concatMaps [] a = a
concatMaps (x:xs) a = concatMaps xs (concatMaps' (Map.assocs x) a)
    where
        concatMaps' [] a = a
        concatMaps' (x:xs) a = 
            case Map.lookup (Char.toLower (fst x)) a of
                Nothing -> concatMaps' (xs) (Map.insert (Char.toLower (fst x)) (snd x) a)
                Just t -> concatMaps' (xs) (Map.insert (Char.toLower (fst x)) ( t + snd x) a)

wordCharCounts::MyWord -> Count
wordCharCounts x = helper x Map.empty
    where
        helper [] a = a
        helper (x:xs) a =
            case Map.lookup (Char.toLower x) a of
                Nothing -> helper (xs) (Map.insert (Char.toLower x) 1 a)
                Just t -> helper (xs) (Map.insert (Char.toLower x) (t+1) a)


dictCharCounts::[MyWord] -> [(MyWord,Count)]
dictCharCounts x = [(y ,(wordCharCounts y)) | y<-x ]


hash::MyWord -> MyWord
hash [] = ""
hash  x = helper (Map.assocs (wordCharCounts x) )
    where 
        helper [] = []
        helper (x:xs) = (show (fst x)) ++ (show (snd x)) ++ helper xs 

dictWordsByCharCounts::[(MyWord,Count)] -> Map.Map String [MyWord]
dictWordsByCharCounts x = helper [ ((fst y), hash (fst y))  | y<-x] Map.empty
    where 
        helper [] a = a
        helper (x:xs) a =
            case Map.lookup (snd x) a of
                Nothing -> helper xs (Map.insert (snd x) [ (fst x) ] a)
                Just t -> helper xs  (Map.insert (snd x) (t++[ (fst x) ]) a)

wordAnagrams::MyWord -> Map.Map String [MyWord] -> [MyWord]
wordAnagrams x y = case Map.lookup (hash x) y of 
    Nothing -> []
    Just t -> t

charCountSubSets::Count->[Count]
charCountSubSets x = helper x (Map.assocs x) 
    where