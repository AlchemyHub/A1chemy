from __future__ import division

# import necessary libaries
import unittest
import math
import numpy as np
from scipy.stats import norm
from scipy.stats import mvn

# Developer can toggle _DEBUG to True for more messages
# normally this is set to False
_DEBUG = False

# This class contains the limits on inputs for GBS models
# It is not intended to be part of this module's public interface
class _GBS_Limits:
    # An GBS model will return an error if an out-of-bound input is input
    MAX32 = 2147483248.0

    MIN_T = 1.0 / 1000.0  # requires some time left before expiration
    MIN_X = 0.01
    MIN_FS = 0.01

    # Volatility smaller than 0.5% causes American Options calculations
    # to fail (Number to large errors).
    # GBS() should be OK with any positive number. Since vols less
    # than 0.5% are expected to be extremely rare, and most likely bad inputs,
    # _gbs() is assigned this limit too
    # MIN_V = 0.005
    MIN_V = 0.00001

    MAX_T = 100
    MAX_X = MAX32
    MAX_FS = MAX32

    # Asian Option limits
    # maximum TA is time to expiration for the option
    MIN_TA = 0

    # This model will work with higher values for b, r, and V. However, such values are extremely uncommon. 
    # To catch some common errors, interest rates and volatility is capped to 100%
    # This reason for 1 (100%) is mostly to cause the library to throw an exceptions 
    # if a value like 15% is entered as 15 rather than 0.15)
    MIN_b = -1
    MIN_r = -1

    MAX_b = 1
    MAX_r = 1
    MAX_V = 1
      

# ------------------------------
# This function verifies that the Call/Put indicator is correctly entered
def _test_option_type(option_type):
    if (option_type != "c") and (option_type != "p"):
        raise GBS_InputError("Invalid Input option_type ({0}). Acceptable value are: c, p".format(option_type))

# ------------------------------
# This function makes sure inputs are OK
# It throws an exception if there is a failure
def _gbs_test_inputs(option_type, fs, x, t, r, b, v):
    # -----------
    # Test inputs are reasonable
    _test_option_type(option_type)

    if (x < _GBS_Limits.MIN_X) or (x > _GBS_Limits.MAX_X):
        raise GBS_InputError(
            "Invalid Input Strike Price (X). Acceptable range for inputs is {1} to {2}".format(x, _GBS_Limits.MIN_X,
                                                                                               _GBS_Limits.MAX_X))

    if (fs < _GBS_Limits.MIN_FS) or (fs > _GBS_Limits.MAX_FS):
        raise GBS_InputError(
            "Invalid Input Forward/Spot Price (FS). Acceptable range for inputs is {1} to {2}".format(fs,
                                                                                                      _GBS_Limits.MIN_FS,
                                                                                                      _GBS_Limits.MAX_FS))

    if (t < _GBS_Limits.MIN_T) or (t > _GBS_Limits.MAX_T):
        raise GBS_InputError(
            "Invalid Input Time (T = {0}). Acceptable range for inputs is {1} to {2}".format(t, _GBS_Limits.MIN_T,
                                                                                             _GBS_Limits.MAX_T))

    if (b < _GBS_Limits.MIN_b) or (b > _GBS_Limits.MAX_b):
        raise GBS_InputError(
            "Invalid Input Cost of Carry (b = {0}). Acceptable range for inputs is {1} to {2}".format(b,
                                                                                                      _GBS_Limits.MIN_b,
                                                                                                      _GBS_Limits.MAX_b))

    if (r < _GBS_Limits.MIN_r) or (r > _GBS_Limits.MAX_r):
        raise GBS_InputError(
            "Invalid Input Risk Free Rate (r = {0}). Acceptable range for inputs is {1} to {2}".format(r,
                                                                                                       _GBS_Limits.MIN_r,
                                                                                                       _GBS_Limits.MAX_r))

    if (v < _GBS_Limits.MIN_V) or (v > _GBS_Limits.MAX_V):
        raise GBS_InputError(
            "Invalid Input Implied Volatility (V = {0}). Acceptable range for inputs is {1} to {2}".format(v,
                                                                                                           _GBS_Limits.MIN_V,
                                                                                                           _GBS_Limits.MAX_V))


# The primary class for calculating Generalized Black Scholes option prices and deltas
# It is not intended to be part of this module's public interface

# Inputs: option_type = "p" or "c", fs = price of underlying, x = strike, t = time to expiration, r = risk free rate
#         b = cost of carry, v = implied volatility
# Outputs: value, delta, gamma, theta, vega, rho
def _gbs(option_type, fs, x, t, r, b, v):
    _debug("Debugging Information: _gbs()")
    # -----------
    # Test Inputs (throwing an exception on failure)
    _gbs_test_inputs(option_type, fs, x, t, r, b, v)

    # -----------
    # Create preliminary calculations
    t__sqrt = math.sqrt(t)
    d1 = (math.log(fs / x) + (b + (v * v) / 2) * t) / (v * t__sqrt)
    d2 = d1 - v * t__sqrt

    if option_type == "c":
        # it's a call
        _debug("     Call Option")
        value = fs * math.exp((b - r) * t) * norm.cdf(d1) - x * math.exp(-r * t) * norm.cdf(d2)
        delta = math.exp((b - r) * t) * norm.cdf(d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) - (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(d1) - r * x * math.exp(-r * t) * norm.cdf(d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = x * t * math.exp(-r * t) * norm.cdf(d2)
    else:
        # it's a put
        _debug("     Put Option")
        value = x * math.exp(-r * t) * norm.cdf(-d2) - (fs * math.exp((b - r) * t) * norm.cdf(-d1))
        delta = -math.exp((b - r) * t) * norm.cdf(-d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) + (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(-d1) + r * x * math.exp(-r * t) * norm.cdf(-d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = -x * t * math.exp(-r * t) * norm.cdf(-d2)

    _debug("     d1= {0}\n     d2 = {1}".format(d1, d2))
    _debug("     delta = {0}\n     gamma = {1}\n     theta = {2}\n     vega = {3}\n     rho={4}".format(delta, gamma,
                                                                                                        theta, vega,
                                                                                                        rho))
    
    return value, delta, gamma, theta, vega, rho    

# -----------
# Generalized American Option Pricer
# This is a wrapper to check inputs and route to the current "best" American option model
def _american_option(option_type, fs, x, t, r, b, v):
    # -----------
    # Test Inputs (throwing an exception on failure)
    _debug("Debugging Information: _american_option()")
    _gbs_test_inputs(option_type, fs, x, t, r, b, v)

    # -----------
    if option_type == "c":
        # Call Option
        _debug("     Call Option")
        return _bjerksund_stensland_2002(fs, x, t, r, b, v)
    else:
        # Put Option
        _debug("     Put Option")

        # Using the put-call transformation: P(X, FS, T, r, b, V) = C(FS, X, T, -b, r-b, V)
        # WARNING - When reconciling this code back to the B&S paper, the order of variables is different

        put__x = fs
        put_fs = x
        put_b = -b
        put_r = r - b

        # pass updated values into the Call Valuation formula
        return _bjerksund_stensland_2002(put_fs, put__x, t, put_r, put_b, v)

# -----------
# American Call Option (Bjerksund Stensland 1993 approximation)
# This is primarily here for testing purposes; 2002 model has superseded this one
def _bjerksund_stensland_1993(fs, x, t, r, b, v):
    # -----------
    # initialize output
    # using GBS greeks (TO DO: update greek calculations)
    my_output = _gbs("c", fs, x, t, r, b, v)

    e_value = my_output[0]
    delta = my_output[1]
    gamma = my_output[2]
    theta = my_output[3]
    vega = my_output[4]
    rho = my_output[5]

    # debugging for calculations
    _debug("-----")
    _debug("Debug Information: _Bjerksund_Stensland_1993())")

    # if b >= r, it is never optimal to exercise before maturity
    # so we can return the GBS value
    if b >= r:
        _debug("     b >= r, early exercise never optimal, returning GBS value")
        return e_value, delta, gamma, theta, vega, rho

    # Intermediate Calculations
    v2 = v ** 2
    sqrt_t = math.sqrt(t)

    beta = (0.5 - b / v2) + math.sqrt(((b / v2 - 0.5) ** 2) + 2 * r / v2)
    b_infinity = (beta / (beta - 1)) * x
    b_zero = max(x, (r / (r - b)) * x)

    h1 = -(b * t + 2 * v * sqrt_t) * (b_zero / (b_infinity - b_zero))
    i = b_zero + (b_infinity - b_zero) * (1 - math.exp(h1))
    alpha = (i - x) * (i ** (-beta))

    # debugging for calculations
    _debug("     b = {0}".format(b))
    _debug("     v2 = {0}".format(v2))
    _debug("     beta = {0}".format(beta))
    _debug("     b_infinity = {0}".format(b_infinity))
    _debug("     b_zero = {0}".format(b_zero))
    _debug("     h1 = {0}".format(h1))
    _debug("     i  = {0}".format(i))
    _debug("     alpha = {0}".format(alpha))

    # Check for immediate exercise
    if fs >= i:
        _debug("     Immediate Exercise")
        value = fs - x
    else:
        _debug("     American Exercise")
        value = (alpha * (fs ** beta)
                 - alpha * _phi(fs, t, beta, i, i, r, b, v)
                 + _phi(fs, t, 1, i, i, r, b, v)
                 - _phi(fs, t, 1, x, i, r, b, v)
                 - x * _phi(fs, t, 0, i, i, r, b, v)
                 + x * _phi(fs, t, 0, x, i, r, b, v))

    # The approximation can break down in boundary conditions
    # make sure the value is at least equal to the European value
    value = max(value, e_value)
    return value, delta, gamma, theta, vega, rho

# -----------
# American Call Option (Bjerksund Stensland 2002 approximation)
def _bjerksund_stensland_2002(fs, x, t, r, b, v):
    # -----------
    # initialize output
    # using GBS greeks (TO DO: update greek calculations)
    my_output = _gbs("c", fs, x, t, r, b, v)

    e_value = my_output[0]
    delta = my_output[1]
    gamma = my_output[2]
    theta = my_output[3]
    vega = my_output[4]
    rho = my_output[5]

    # debugging for calculations
    _debug("-----")
    _debug("Debug Information: _Bjerksund_Stensland_2002())")

    # If b >= r, it is never optimal to exercise before maturity
    # so we can return the GBS value
    if b >= r:
        _debug("     Returning GBS value")
        return e_value, delta, gamma, theta, vega, rho

    # -----------
    # Create preliminary calculations
    v2 = v ** 2
    t1 = 0.5 * (math.sqrt(5) - 1) * t
    t2 = t

    beta_inside = ((b / v2 - 0.5) ** 2) + 2 * r / v2
    # forcing the inside of the sqrt to be a positive number
    beta_inside = abs(beta_inside)
    beta = (0.5 - b / v2) + math.sqrt(beta_inside)
    b_infinity = (beta / (beta - 1)) * x
    b_zero = max(x, (r / (r - b)) * x)

    h1 = -(b * t1 + 2 * v * math.sqrt(t1)) * ((x ** 2) / ((b_infinity - b_zero) * b_zero))
    h2 = -(b * t2 + 2 * v * math.sqrt(t2)) * ((x ** 2) / ((b_infinity - b_zero) * b_zero))

    i1 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h1))
    i2 = b_zero + (b_infinity - b_zero) * (1 - math.exp(h2))

    alpha1 = (i1 - x) * (i1 ** (-beta))
    alpha2 = (i2 - x) * (i2 ** (-beta))

    # debugging for calculations
    _debug("     t1 = {0}".format(t1))
    _debug("     beta = {0}".format(beta))
    _debug("     b_infinity = {0}".format(b_infinity))
    _debug("     b_zero = {0}".format(b_zero))
    _debug("     h1 = {0}".format(h1))
    _debug("     h2 = {0}".format(h2))
    _debug("     i1 = {0}".format(i1))
    _debug("     i2 = {0}".format(i2))
    _debug("     alpha1 = {0}".format(alpha1))
    _debug("     alpha2 = {0}".format(alpha2))

    # check for immediate exercise
    if fs >= i2:
        value = fs - x
    else:
        # Perform the main calculation    
        value = (alpha2 * (fs ** beta)
                 - alpha2 * _phi(fs, t1, beta, i2, i2, r, b, v)
                 + _phi(fs, t1, 1, i2, i2, r, b, v)
                 - _phi(fs, t1, 1, i1, i2, r, b, v)
                 - x * _phi(fs, t1, 0, i2, i2, r, b, v)
                 + x * _phi(fs, t1, 0, i1, i2, r, b, v)
                 + alpha1 * _phi(fs, t1, beta, i1, i2, r, b, v)
                 - alpha1 * _psi(fs, t2, beta, i1, i2, i1, t1, r, b, v)
                 + _psi(fs, t2, 1, i1, i2, i1, t1, r, b, v)
                 - _psi(fs, t2, 1, x, i2, i1, t1, r, b, v)
                 - x * _psi(fs, t2, 0, i1, i2, i1, t1, r, b, v)
                 + x * _psi(fs, t2, 0, x, i2, i1, t1, r, b, v))

    # in boundary conditions, this approximation can break down
    # Make sure option value is greater than or equal to European value
    value = max(value, e_value)

    # -----------
    # Return Data
    return value, delta, gamma, theta, vega, rho


# ---------------------------
# American Option Intermediate Calculations

# -----------
# The Psi() function used by _Bjerksund_Stensland_2002 model
def _psi(fs, t2, gamma, h, i2, i1, t1, r, b, v):
    vsqrt_t1 = v * math.sqrt(t1)
    vsqrt_t2 = v * math.sqrt(t2)

    bgamma_t1 = (b + (gamma - 0.5) * (v ** 2)) * t1
    bgamma_t2 = (b + (gamma - 0.5) * (v ** 2)) * t2

    d1 = (math.log(fs / i1) + bgamma_t1) / vsqrt_t1
    d3 = (math.log(fs / i1) - bgamma_t1) / vsqrt_t1

    d2 = (math.log((i2 ** 2) / (fs * i1)) + bgamma_t1) / vsqrt_t1
    d4 = (math.log((i2 ** 2) / (fs * i1)) - bgamma_t1) / vsqrt_t1

    e1 = (math.log(fs / h) + bgamma_t2) / vsqrt_t2
    e2 = (math.log((i2 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e3 = (math.log((i1 ** 2) / (fs * h)) + bgamma_t2) / vsqrt_t2
    e4 = (math.log((fs * (i1 ** 2)) / (h * (i2 ** 2))) + bgamma_t2) / vsqrt_t2

    tau = math.sqrt(t1 / t2)
    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    psi = math.exp(lambda1 * t2) * (fs ** gamma) * (_cbnd(-d1, -e1, tau)
                                                    - ((i2 / fs) ** kappa) * _cbnd(-d2, -e2, tau)
                                                    - ((i1 / fs) ** kappa) * _cbnd(-d3, -e3, -tau)
                                                    + ((i1 / i2) ** kappa) * _cbnd(-d4, -e4, -tau))
    return psi

# -----------
# The Phi() function used by _Bjerksund_Stensland_2002 model and the _Bjerksund_Stensland_1993 model
def _phi(fs, t, gamma, h, i, r, b, v):
    d1 = -(math.log(fs / h) + (b + (gamma - 0.5) * (v ** 2)) * t) / (v * math.sqrt(t))
    d2 = d1 - 2 * math.log(i / fs) / (v * math.sqrt(t))

    lambda1 = (-r + gamma * b + 0.5 * gamma * (gamma - 1) * (v ** 2))
    kappa = (2 * b) / (v ** 2) + (2 * gamma - 1)

    phi = math.exp(lambda1 * t) * (fs ** gamma) * (norm.cdf(d1) - ((i / fs) ** kappa) * norm.cdf(d2))

    _debug("-----")
    _debug("Debug info for: _phi()")
    _debug("    d1={0}".format(d1))
    _debug("    d2={0}".format(d2))
    _debug("    lambda={0}".format(lambda1))
    _debug("    kappa={0}".format(kappa))
    _debug("    phi={0}".format(phi))
    return phi

# -----------
# Cumulative Bivariate Normal Distribution
# Primarily called by Psi() function, part of the _Bjerksund_Stensland_2002 model
def _cbnd(a, b, rho):
    # This distribution uses the Genz multi-variate normal distribution 
    # code found as part of the standard SciPy distribution
    lower = np.array([0, 0])
    upper = np.array([a, b])
    infin = np.array([0, 0])
    correl = rho
    error, value, inform = mvn.mvndst(lower, upper, infin, correl)
    return value

# ----------
# Inputs (not all functions use all inputs)
#      fs = forward/spot price
#      x = Strike
#      t = Time (in years)
#      r = risk free rate
#      b = cost of carry
#      cp = Call or Put price
#      precision = (optional) precision at stopping point
#      max_steps = (optional) maximum number of steps

# ----------
# Approximate Implied Volatility
#
# This function is used to choose a starting point for the
# search functions (Newton and bisection searches). 
# Brenner & Subrahmanyam (1988), Feinstein (1988)

def _approx_implied_vol(option_type, fs, x, t, r, b, cp):
    _test_option_type(option_type)

    ebrt = math.exp((b - r) * t)
    ert = math.exp(-r * t)

    a = math.sqrt(2 * math.pi) / (fs * ebrt + x * ert)

    if option_type == "c":
        payoff = fs * ebrt - x * ert
    else:
        payoff = x * ert - fs * ebrt

    b = cp - payoff / 2
    c = (payoff ** 2) / math.pi

    v = (a * (b + math.sqrt(b ** 2 + c))) / math.sqrt(t)

    return v

# ----------
# Find the Implied Volatility of an European (GBS) Option given a price
# using Newton-Raphson method for greater speed since Vega is available

def _gbs_implied_vol(option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    return _newton_implied_vol(_gbs, option_type, x, fs, t, b, r, cp, precision, max_steps)

# ----------
# Find the Implied Volatility of an American Option given a price
# Using bisection method since Vega is difficult to estimate for Americans
def _american_implied_vol(option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    return _bisection_implied_vol(_american_option, option_type, fs, x, t, r, b, cp, precision, max_steps)

# ----------
# Calculate Implied Volatility with a Newton Raphson search
def _newton_implied_vol(val_fn, option_type, x, fs, t, b, r, cp, precision=.00001, max_steps=100):
    # make sure a valid option type was entered
    _test_option_type(option_type)

    # Estimate starting Vol, making sure it is allowable range
    v = _approx_implied_vol(option_type, fs, x, t, r, b, cp)
    v = max(_GBS_Limits.MIN_V, v)
    v = min(_GBS_Limits.MAX_V, v)

    # Calculate the value at the estimated vol
    value, delta, gamma, theta, vega, rho = val_fn(option_type, fs, x, t, r, b, v)
    min_diff = abs(cp - value)

    _debug("-----")
    _debug("Debug info for: _Newton_ImpliedVol()")
    _debug("    Vinitial={0}".format(v))

    # Newton-Raphson Search
    countr = 0
    while precision <= abs(cp - value) <= min_diff and countr < max_steps:

        v = v - (value - cp) / vega
        if (v > _GBS_Limits.MAX_V) or (v < _GBS_Limits.MIN_V):
            _debug("    Volatility out of bounds")
            break

        value, delta, gamma, theta, vega, rho = val_fn(option_type, fs, x, t, r, b, v)
        min_diff = min(abs(cp - value), min_diff)

        # keep track of how many loops
        countr += 1
        _debug("     IVOL STEP {0}. v={1}".format(countr, v))

    
    # check if function converged and return a value
    if abs(cp - value) < precision:
        # the search function converged
        return v
    else:
        # if the search function didn't converge, try a bisection search
        return _bisection_implied_vol(val_fn, option_type, fs, x, t, r, b, cp, precision, max_steps)

# ----------
# Find the Implied Volatility using a Bisection search
def _bisection_implied_vol(val_fn, option_type, fs, x, t, r, b, cp, precision=.00001, max_steps=100):
    _debug("-----")
    _debug("Debug info for: _bisection_implied_vol()")

    # Estimate Upper and Lower bounds on volatility
    # Assume American Implied vol is within +/- 50% of the GBS Implied Vol
    v_mid = _approx_implied_vol(option_type, fs, x, t, r, b, cp)

    if (v_mid <= _GBS_Limits.MIN_V) or (v_mid >= _GBS_Limits.MAX_V):
        # if the volatility estimate is out of bounds, search entire allowed vol space
        v_low = _GBS_Limits.MIN_V
        v_high = _GBS_Limits.MAX_V
        v_mid = (v_low + v_high) / 2
    else:
        # reduce the size of the vol space
        v_low = max(_GBS_Limits.MIN_V, v_mid * .5)
        v_high = min(_GBS_Limits.MAX_V, v_mid * 1.5)

    # Estimate the high/low bounds on price
    cp_mid = val_fn(option_type, fs, x, t, r, b, v_mid)[0]
    
    # initialize bisection loop
    current_step = 0
    diff = abs(cp - cp_mid)

    _debug("     American IVOL starting conditions: CP={0} cp_mid={1}".format(cp, cp_mid))
    _debug("     IVOL {0}. V[{1},{2},{3}]".format(current_step, v_low, v_mid, v_high))

    # Keep bisection volatility until correct price is found
    while (diff > precision) and (current_step < max_steps):
        current_step += 1

        # Cut the search area in half
        if cp_mid < cp:
            v_low = v_mid
        else:
            v_high = v_mid

        cp_low = val_fn(option_type, fs, x, t, r, b, v_low)[0]
        cp_high = val_fn(option_type, fs, x, t, r, b, v_high)[0]

        v_mid = v_low + (cp - cp_low) * (v_high - v_low) / (cp_high - cp_low)
        v_mid = max(_GBS_Limits.MIN_V, v_mid)  # enforce high/low bounds
        v_mid = min(_GBS_Limits.MAX_V, v_mid)  # enforce high/low bounds

        cp_mid = val_fn(option_type, fs, x, t, r, b, v_mid)[0]
        diff = abs(cp - cp_mid)

        _debug("     IVOL {0}. V[{1},{2},{3}]".format(current_step, v_low, v_mid, v_high))

    # return output
    if abs(cp - cp_mid) < precision:
        return v_mid
    else:
        raise GBS_CalculationError(
            "Implied Vol did not converge. Best Guess={0}, Price diff={1}, Required Precision={2}".format(v_mid, diff,
                                                                                                          precision))
#-----------------------------------------
# Public Interface for valuation functions
#-----------------------------------------


# This is the public interface for European Options
# Each call does a little bit of processing and then calls the calculations located in the _gbs module

# Inputs: 
#    option_type = "p" or "c"
#    fs          = price of underlying
#    x           = strike
#    t           = time to expiration
#    v           = implied volatility
#    r           = risk free rate
#    q           = dividend payment
#    b           = cost of carry
# Outputs: 
#    value       = price of the option
#    delta       = first derivative of value with respect to price of underlying
#    gamma       = second derivative of value w.r.t price of underlying
#    theta       = first derivative of value w.r.t. time to expiration
#    vega        = first derivative of value w.r.t. implied volatility
#    rho         = first derivative of value w.r.t. risk free rates

# ---------------------------
# Black Scholes: stock Options (no dividend yield)
def black_scholes(option_type, fs, x, t, r, v):
    b = r
    return _gbs(option_type, fs, x, t, r, b, v)

# ---------------------------
# Merton Model: Stocks Index, stocks with a continuous dividend yields
def merton(option_type, fs, x, t, r, q, v):
    b = r - q
    return _gbs(option_type, fs, x, t, r, b, v)

# ---------------------------
# Commodities
def black_76(option_type, fs, x, t, r, v):
    b = 0
    return _gbs(option_type, fs, x, t, r, b, v)

# ---------------------------
# FX Options
def garman_kohlhagen(option_type, fs, x, t, r, rf, v):
    b = r - rf
    return _gbs(option_type, fs, x, t, r, b, v)

# ---------------------------
# Average Price option on commodities
def asian_76(option_type, fs, x, t, t_a, r, v):
    # Check that TA is reasonable
    if (t_a < _GBS_Limits.MIN_TA) or (t_a > t):
        raise GBS_InputError(
            "Invalid Input Averaging Time (TA = {0}). Acceptable range for inputs is {1} to <T".format(t_a,
                                                                                                       _GBS_Limits.MIN_TA))

    # Approximation to value Asian options on commodities
    b = 0
    if t_a == t:
        # if there is no averaging period, this is just Black Scholes
        v_a = v
    else:
        # Approximate the volatility
        m = (2 * math.exp((v ** 2) * t) - 2 * math.exp((v ** 2) * t_a) * (1 + (v ** 2) * (t - t_a))) / (
            (v ** 4) * ((t - t_a) ** 2))
        v_a = math.sqrt(math.log(m) / t)

    # Finally, have the GBS function do the calculation
    return _gbs(option_type, fs, x, t, r, b, v_a)

# ---------------------------
# Spread Option formula
def kirks_76(option_type, f1, f2, x, t, r, v1, v2, corr):
    # create the modifications to the GBS formula to handle spread options
    b = 0
    fs = f1 / (f2 + x)
    f_temp = f2 / (f2 + x)
    v = math.sqrt((v1 ** 2) + ((v2 * f_temp) ** 2) - (2 * corr * v1 * v2 * f_temp))
    my_values = _gbs(option_type, fs, 1.0, t, r, b, v)

    # Have the GBS function return a value
    return my_values[0] * (f2 + x), 0, 0, 0, 0, 0

# ---------------------------
# American Options (stock style, set q=0 for non-dividend paying options)
def american(option_type, fs, x, t, r, q, v):
    b = r - q
    return _american_option(option_type, fs, x, t, r, b, v)

# ---------------------------
# Commodities
def american_76(option_type, fs, x, t, r, v):
    b = 0
    return _american_option(option_type, fs, x, t, r, b, v)


#-------------------------------------------------
#Public Interface for implied Volatility Functions
#-------------------------------------------------
# Inputs: 
#    option_type = "p" or "c"
#    fs          = price of underlying
#    x           = strike
#    t           = time to expiration
#    v           = implied volatility
#    r           = risk free rate
#    q           = dividend payment
#    b           = cost of carry
# Outputs: 
#    value       = price of the option
#    delta       = first derivative of value with respect to price of underlying
#    gamma       = second derivative of value w.r.t price of underlying
#    theta       = first derivative of value w.r.t. time to expiration
#    vega        = first derivative of value w.r.t. implied volatility
#    rho         = first derivative of value w.r.t. risk free rates

def euro_implied_vol(option_type, fs, x, t, r, q, cp):
    b = r - q
    return _gbs_implied_vol(option_type, fs, x, t, r, b, cp)

def euro_implied_vol_76(option_type, fs, x, t, r, cp):
    b = 0
    return _gbs_implied_vol(option_type, fs, x, t, r, b, cp)

def amer_implied_vol(option_type, fs, x, t, r, q, cp):
    b = r - q
    return _american_implied_vol(option_type, fs, x, t, r, b, cp)

def amer_implied_vol_76(option_type, fs, x, t, r, cp):
    b = 0
    return _american_implied_vol(option_type, fs, x, t, r, b, cp)


#-----------------------------------
### Implementation: Helper Functions
#-----------------------------------
# ---------------------------
# Helper Function for Debugging

# Prints a message if running code from this module and _DEBUG is set to true
# otherwise, do nothing

def _debug(debug_input):
    if (__name__ is "__main__") and (_DEBUG is True):
        print(debug_input)

# This class defines the Exception that gets thrown when invalid input is placed into the GBS function
class GBS_InputError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

# This class defines the Exception that gets thrown when there is a calculation error
class GBS_CalculationError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

# This function tests that two floating point numbers are the same
# Numbers less than 1 million are considered the same if they are within .000001 of each other
# Numbers larger than 1 million are considered the same if they are within .0001% of each other
# User can override the default precision if necessary
def assert_close(value_a, value_b, precision=.000001):
    my_precision = precision

    if (value_a < 1000000.0) and (value_b < 1000000.0):
        my_diff = abs(value_a - value_b)
        my_diff_type = "Difference"
    else:
        my_diff = abs((value_a - value_b) / value_a)
        my_diff_type = "Percent Difference"

    _debug("Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(value_a, value_b, my_diff,
                                                                                     my_diff_type))

    if my_diff < my_precision:
        my_result = True
    else:
        my_result = False

    if (__name__ is "__main__") and (my_result is False):
        print("  FAILED TEST. Comparing {0} and {1}. Difference is {2}, Difference Type is {3}".format(value_a, value_b,
                                                                                                       my_diff,
                                                                                                       my_diff_type))
    else:
        print(".")

    return my_result
# impv = calculate_impv(
#     bid_price,
#     underlying_price,
#     strike_price,
#     interest_rate,
#     time_to_expire,
#     option_type
# )
#euro_implied_vol(self.option_type, fs=current_price, x=self.strike, t=t, r=r, q=q, cp=self.price)
def calculate_impv(
    price: float,
    s: float,
    k: float,
    r: float,
    t: float,
    cp: int
):
    return euro_implied_vol(
        option_type= 'c' if cp ==1 else 'p',
        fs=s,
        x=k,
        t=t,
        r=r,
        q=0,
        cp=price
    )

# calculate_greeks(
#     underlying_price,
#     strike_price,
#     interest_rate,
#     time_to_expire,
#     impv,
#     option_type
# )
#merton(option_type, fs=underlying_price, x=strike_price, t=time_to_expire, r=interest_rate, q=0, v=iv)
def calculate_greeks(
    s: float,
    k: float,
    r: float,
    t: float,
    v: float,
    cp: int
):
    return merton(
        option_type= 'c' if cp ==1 else 'p',
        fs=s,
        x=k,
        t=t,
        r=r,
        q=0,
        v=v
    )[0:5]