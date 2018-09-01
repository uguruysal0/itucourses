module Trie
(
    empty,
    insert,
    search,
    getWords,
    prefix
) 

where

import qualified Data.Map as Map
import System.IO
import System.Environment

data Trie = Trie {end :: Bool, children :: Map.Map Char Trie}
    deriving (Show,Eq)


empty = Trie False Map.empty 

insert::String->Trie->Trie
insert [] (Trie e c) = Trie True c
insert (x:xs) (Trie k a) = case Map.lookup x a of 
    Nothing -> Trie k (Map.insert x (insert xs (empty)) a) 
    Just y -> Trie k (Map.insert x (insert xs y) a)

insertList a t = foldr (\x y -> insert x y) t a

search::String->Trie->Bool
search [] (Trie e c) = e
search (x:xs) (Trie e c) = case Map.lookup x c of 
    Nothing -> False
    Just y  -> search xs y
        
helper::String->[(Char,Trie)]->Bool->[String]
helper acc' [] e'
    | e' = [acc']
    | otherwise = []
helper acc' (x:xs) e'
    | e' = [acc'] ++ helper (acc'++[fst x]) (Map.toList $ children $ snd x) (end $ snd x) ++ helper acc' xs False
    | otherwise =  helper (acc'++[fst x]) (Map.toList $ children $ snd x) (end $ snd x) ++ helper acc' xs False


getWords::Trie->[String]
getWords t' =helper "" (Map.toList $ children t') (end t')

getWords'::Trie->[String]
getWords' (Trie e c)
    | e         = ("" :) $ concat $ map (\(k,t) -> map (k:) $ getWords t) (Map.toList c)
    | otherwise =  concat $ map (\(k,t) -> map (k:) $ getWords t) (Map.toList c)


prefix::String->Trie-> Maybe [String]
prefix acc t = prefix' acc acc t
    where
        prefix' acc [] (Trie e c) =  Just (helper acc (Map.toList c) e )
        prefix' acc (x:xs) (Trie e c) = case Map.lookup x c of 
            Nothing -> Nothing
            Just t' -> prefix' acc xs t'


printMenu = do 
    putStrLn "a) Add Word"
    putStrLn "s) Search Word"
    putStrLn "f) Find words with prefix"
    putStrLn "p) Print all words"
    putStrLn "e) Exit"
    putStrLn "Enter the action"

programloop t = do
    printMenu
    c <- getChar
    putStrLn ""
    case c of
        'a' -> do putStrLn  "Enter word/prefix"
                  word <- getLine
                  programloop (Trie.insert word t)
        's' -> do putStrLn  "Enter word/prefix"
                  word <- getLine
                  case Trie.search word t of 
                    True -> putStrLn "Exist" >>  programloop t
                    otherwise -> putStrLn "Non Exist" >> programloop t
        'f' -> do putStrLn "Enter word/prefix"
                  word <- getLine
                  case  Trie.prefix word t of 
                    Nothing -> putStrLn "With prefix" >> programloop t
                    Just a ->  programloop t
        'p' -> do putStrLn "Enter word/prefix"
                  word <- getLine
                  putStrLn (show (Trie.getWords' t) ) >> programloop t
        'e' -> return ()
        _   -> programloop t
    
main:: IO()
main = do
    args <- getArgs
    content <- readFile $ head args
    let strings = lines content
    let trie = empty
    programloop $ Trie.insertList strings trie
    return ()