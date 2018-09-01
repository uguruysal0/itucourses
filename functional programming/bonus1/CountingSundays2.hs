module CountingSundays2 where 
dayOfWeek :: Integer -> Integer -> Integer -> Integer
dayOfWeek year month day = res
    where 
        j = floor (  fromIntegral(year`div`100)  )
        k = year `mod` 100
        month' = if month<=2 then month + 12 else month
        t1 = floor (fromIntegral (13 * (month' + 1)) / 5.0)  
        t2 = floor( fromIntegral(k `div` 4))
        t3 = floor ( fromIntegral(j `div` 4))
        res = (day + t1 + k + t2 + t3 + 5 *j ) `mod` 7
    
sundays1 :: Integer -> Integer -> Integer
sundays1 start end = sundays' 0 start 1
    where
    sundays' :: Integer -> Integer -> Integer -> Integer
    sundays' acc year month
        | year > end                  = acc
        | dayOfWeek year month 1 == 1 = sundays' (acc+1) nextY nextM 
        | otherwise                   = sundays'  acc    nextY nextM
        where
            nextM = if month == 12 then 1 else month + 1
            nextY = if month == 12 then year + 1 else year