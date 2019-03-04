
#### A/B Testing Tools and Handy Function

### Sample size function

from scipy import stats

### Get Power Function
def get_power(n, p1, p2, cl):
    alpha = 1 - cl
    qu = stats.norm.ppf(1 - alpha/2)
    diff = abs(p2-p1)
    bp = (p1+p2) / 2
    
    v1 = p1 * (1-p1)
    v2 = p2 * (1-p2)
    bv = bp * (1-bp)
    
    power_part_one = stats.norm.cdf((n**0.5 * diff - qu * (2 * bv)**0.5) / (v1+v2) ** 0.5)
    power_part_two = 1 - stats.norm.cdf((n**0.5 * diff + qu * (2 * bv)**0.5) / (v1+v2) ** 0.5)
    
    power = power_part_one + power_part_two
    
    return (power)


get_power(1000, 0.1, 0.12, 0.95)
get_power(2000, 0.1, 0.12, 0.95)
get_power(1000, 0.1, 0.12, 0.8)

### Get Sample Size Function
def get_sample_size(power, p1, p2, cl, max_n=1000000):
    n = 1 
    while n <= max_n:
        tmp_power = get_power(n, p1, p2, cl)

        if tmp_power >= power: 
            return n 
        else: 
            n = n + 100

    return "Increase Max N Value"

# Trial1
conversion_rate = 0.03
power = 0.8
cl = 0.9
percent_lift = 0.1
conversion_rate_p2 = conversion_rate * (1 + percent_lift)

get_sample_size(power, conversion_rate, conversion_rate_p2, cl)
# =>>>>>>> 42001

# Trial2
conversion_rate = 0.03
power = 0.95
cl = 0.9
percent_lift = 0.1
conversion_rate_p2 = conversion_rate * (1 + percent_lift)

get_sample_size(power, conversion_rate, conversion_rate_p2, cl)
# =>>>>>> 73401
# If a product analyst want to conclude the sample size for an experiement, the higher the power he desires,
# the more sample he needs.

### Get P-value 
def get_pvalue(con_conv, test_conv, con_size, test_size):
    lift = -abs(test_conv - con_conv)
    
    scale_one = con_conv * (1-con_conv) * (1/ con_size)
    scale_two = test_conv * (1-test_conv) * (1/ test_size)
    scale_val = (scale_one + scale_two) ** 0.5
    
    p_value = 2 * stats.norm.cdf(lift, loc=0, scale = scale_val)  
    return p_value

# Trial 1
con_conv = 0.034351
test_conv = 0.041984
con_size = 48236
test_size = 49867 

get_pvalue(con_conv, test_conv, con_size, test_size)   # 4.257297485586909e-10

# Trial 2
con_conv = 0.034351
test_conv = 0.041984
con_size = 48
test_size = 49 

get_pvalue(con_conv, test_conv, con_size, test_size)  # 0.8443


### Get Confidence Interval
def get_ci(lift, alpha, sd):
    val = abs(stats.norm.ppf((1-alpha)/2))
    
    lwr_bnd = lift - val * sd
    upr_bnd = lift + val * sd
    
    return (lwr_bnd, upr_bnd)

# Trial 1
test_conv = 0.102005
con_conv = 0.090965
test_size = 56350
con_size = 58583

lift_mean = test_conv - con_conv
lift_variance = (1 - test_conv) * test_conv /test_size + (1 - con_conv) * con_conv / con_size
lift_sd = lift_variance**0.5

get_ci(lift_mean, 0.95, lift_sd)   # (0.007624337671217316, 0.014455662328782672)

# Trial 2
test_conv = 0.102005
con_conv = 0.090965
test_size = 563
con_size = 585

lift_mean = test_conv - con_conv
lift_variance = (1 - test_conv) * test_conv /test_size + (1 - con_conv) * con_conv / con_size
lift_sd = lift_variance**0.5

get_ci(lift_mean, 0.95, lift_sd)   # (-0.023135997406420666, 0.045215997406420655)






