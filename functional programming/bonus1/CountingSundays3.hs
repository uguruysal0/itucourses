module CountingSundays3 where
leap :: Integer -> Bool
leap y = ((y `mod` 4) == 0) && ((y `mod` 100)/=0) || ((y `mod` 400) == 0)

daysInMonth:: Integer -> Integer -> Integer
daysInMonth 2 y = if leap(y) then 29 else 28
daysInMonth m y
    | m==4 || m==6 || m== 9 || m== 11 = 30
    | otherwise                       = 31

sundays2 :: Integer -> Integer -> Integer
sundays2 start end = helper 0 2 1 start
    where 
    helper :: Integer -> Integer -> Integer -> Integer -> Integer
    helper acc weekday month year 
        | year > end         = acc
        | weekday'`mod` 7==0  = helper (acc +1) weekday' month' year'
        | otherwise           = helper acc weekday' month' year'
        where 
            weekday' =  weekday + daysInMonth month year 
            month' = if month == 12 then 1 else month+1
            year' = if month== 12 then year +1 else year