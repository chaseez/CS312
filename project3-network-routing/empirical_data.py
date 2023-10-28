from numpy import mean

hundred_heap = [0.003128,0.002564,0.000998,0.002793,0.001748]
hundred_array = [0.001952,0.000956,0.000798,0.000632,0.000569]

hundred_heap_mean = mean(hundred_heap)
hundred_array_mean = mean(hundred_array)

thousand_heap = [0.074704,0.076634,0.059854,0.076664,0.053289]
thousand_array = [0.062725,0.062616,0.062584,0.038113,0.044410]

thousand_heap_mean = mean(thousand_heap)
thousand_array_mean = mean(thousand_array)


ten_thousand_heap = [2.792942,2.805419,2.804175,2.841827,2.810710]
ten_thousand_array = [3.693154,3.665705,3.706433,3.669325,3.693779]

ten_thousand_heap_mean = mean(ten_thousand_heap)
ten_thousand_array_mean = mean(ten_thousand_array)

print(hundred_heap_mean, hundred_array_mean)

print(thousand_heap_mean, thousand_array_mean)

print(ten_thousand_heap_mean, ten_thousand_array_mean)