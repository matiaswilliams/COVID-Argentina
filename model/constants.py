N_c = 4  # average number of contacts per day
beta0 = 0.35  # people infected by patient per day
alpha = 0.4  # fraction of cases that are asymptomatic
lambda_e = 1 / 5  # 1/(length of incubation period)
lambda_p = 1  # 2?   #1/(days till symptoms appear)
lambda_a = 0.1429  # 1/(days till asymptomatic person recovers)
lambda_m = 0.1429  # 1/(days till mild case recovers)
lambda_s = 0.1736  # 1/(days till severe case is hospitalised)
rho = 0.075  # 1/(days in hospital)
delta = 0.2  # number of deaths/number hospitalised
mu = 0.9  # 0.956      #fraction of symptomatic cases that don't need hospitalisation

distance_cutoff = 0.012

# Age-specific mu values
mu_0_19 = 0.9795 # mu for 0-19 : 0.984 to 0.975
mu_20_44 = 0.8245 # mu for 20-44 : 0.857 to 0.792
mu_45_54 = 0.7525 # mu for 45-54 : 0.788 to 0.717
mu_55_64 = 0.747 # mu for 55-64 : 0.795 to 0.699
mu_65_74 = 0.6395 # mu for 65-74 : 0.714 to 0.565
mu_75_84 = 0.554 # mu for 75-84 : 0.695 to 0.413
mu_85_above = 0.492 # mu for 85 & above : 0.687 to 0.297

# Age-specific delta values
# Dividing case fatality rate (cfr) by (1-mu) to get delta values
delta_0_19 = 0 # cfr = 0 and mu = 0.9795
delta_20_44 = 0.0085 # cfr = 0.001 to 0.002 = 0.0015 and mu = 0.8245
delta_45_54 = 0.02626 # cfr = 0.005 to 0.008 = 0.0065 and mu = 0.7525
delta_55_64 = 0.07905  # cfr = 0.014 to 0.026 = 0.02 and mu = 0.747
delta_65_74 = 0.1054  # cfr = 0.027 to 0.049 = 0.038 and mu = 0.6395
delta_75_84 = 0.1659  # cfr = 0.043 to 0.105 = 0.074 and mu = 0.554
delta_85_above = 0.37106   # cfr = 0.104 to 0.273 = 0.1885 and mu = 0.492