def tribonacci(signature,n):
    """ Calculate tribonacci sequence of specified length
        with specified starting elements """
    if n <= 3:
        return signature[:n]
    for i in range(n-3):
        signature.append(signature[-1]+signature[-2]+signature[-3])
    return signature

