module CountingSundays1 where 
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
                    
--- The variables names are taken from python source code given at ninova 
--- I could not get the algorithm well, if I understand algorithm better
        
sundays1 :: Integer -> Integer -> Integer
sundays1 start end = sundays' start 1
    where
    sundays' :: Integer -> Integer -> Integer
    sundays' year month
        | year > end = 0
        | otherwise  = if  dayOfWeek year month 1 == 1 then rest +1 else rest
        where
            nextY = if month == 12 then year + 1 else year
            nextM = if month == 12 then 1 else month + 1
            rest = sundays' nextY nextM