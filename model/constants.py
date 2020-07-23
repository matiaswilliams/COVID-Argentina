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


mu_0_19 = 0.9795 # mu for 0-19 : 0.984 to 0.975
mu_20_44 = 0.8245 # mu for 20-44 : 0.857 to 0.792
mu_45_54 = 0.7525 # mu for 45-54 : 0.788 to 0.717
mu_55_64 = 0.747 # mu for 55-64 : 0.795 to 0.699
mu_65_74 = 0.6395 # mu for 65-74 : 0.714 to 0.565
mu_75_84 = 0.554 # mu for 75-84 : 0.695 to 0.413
mu_85_above = 0.492 # mu for 85 & above : 0.687 to 0.297