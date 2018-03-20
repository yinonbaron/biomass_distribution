# This module contains functions that calculate the mean and 95% confidence interval of fractions
import numpy as np

def frac_mean(fractions,weights=None):
    """
    This functions calculates the geometric mean of several fractions. 
    We assume the fractions themselves are not distributed log normally.
    A fraction can be defined as f = X/(X+Y), where f is the fraction 
    and X and Y are two parts of the population (X is the component for which
    we calculate the fraction and Y is the rest).
    because f is bound by [0,1], we transform the fractions to a quantity 
    which is not bound, ramely a = X/Y.
    a = f/(1-f)
    We calculate the geometric mean of a, and then convert back a to f by the relation
    f = 1/(1+1/a)
    
    Input: 
        fractions: a numpy array of the fractions for which we calculate the geometric mean
        weights: an optional array of weights for each fraction, in case we want to calculate
                 weighted averages
    Output: the geometric mean of fractions
    """

    alpha = fractions/(1.-fractions)
    log_alpha = np.log10(alpha)
    if weights is not None:
        mean_alpha = 10**np.average(log_alpha,weights=weights)                        
    else:
        mean_alpha = 10**np.mean(log_alpha)            
    mean_frac = 1./(1.+1./mean_alpha)
    return mean_frac

def frac_CI(fractions):
    """
    This functions calculates the 95% multiplicative confidence interval of the geometric mean of several fractions. 
    We assume the fractions themselves are not distributed log normally.
    A fraction can be defined as f = X/(X+Y), where f is the fraction 
    and X and Y are two parts of the population (X is the component for which
    we calculate the fraction and Y is the rest).
    because f is bound by [0,1], we transform the fractions to a quantity 
    which is not bound, ramely a = X/Y.
    a = f/(1-f)
    We calculate the 95% confidence interval of a, and then convert back a to f by the relation
    f = 1/(1+1/a)
     
    Input: 
        fractions: a numpy array of the fractions for which we calculate the geometric mean
        weights: an optional array of weights for each fraction, in case we want to calculate
                 weighted averages
    Output: the geometric mean of fractions
    """
    
    alpha = fractions/(1.-fractions)
    log_alpha = np.log(alpha)
    se_alpha = np.std(log_alpha,ddof=1)/np.sqrt(log_alpha.shape[0])
    mean_alpha = np.mean(log_alpha)
    # To turn a into f, we assume a is lognormally distributed, so we sample from a lognormal 
    # distribution with a mean that is equal to the mean a and an std equal to the std of a.
    alpha_dist = np.random.lognormal(mean_alpha,se_alpha,100000)
    # We calculate f based on a to generate a distribution of fractions f    
    frac_dist = 1./(1.+1./alpha_dist)
    # We calculate the multiplicative value of the 97.5 percentile of the distribution of fraction relative to the mean
    upper_CI = np.percentile(frac_dist,97.5)/frac_mean(fractions)
    # We calculate the multiplicative value of the mean of the distribution of fraction relative to the 2.5 percentile
    lower_CI = frac_mean(fractions)/np.percentile(frac_dist,2.5)
    # We return the mean of the upper and lower multiplicative values
    return np.mean([upper_CI,lower_CI])
