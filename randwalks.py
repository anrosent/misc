from math import *
"""Provides utilities for analyzing symmetric 3-D random walks"""

def z_3(n):
"""Returns the probability of being at the origin after n steps of a symmetric 3-dimensional random walk"""
	if n%2 == 1:
		return 0
	else:
		return (1/6)**(n)*sum(factorial(n)/(factorial(j)**2 * factorial(k)**2 * factorial(n//2-k-j)**2) for k in range(n//2+1) for j in range(n//2+1) if k + j <= n//2)
	
def beta(N):
"""Returns the sum of the probability of having returned to the origin at step i of a symmetric 3-dimensional random walk starting at the origin for all i from 0 to N"""
	return sum(z_3(n) for n in range(N+1))
	
def R(N):
"""Return an approximation of the probability of returning to the origin in an N-step symmetric 3-dimensional random walk"""
	return 1-1/beta(N)
	
def plot(N):
"""gnuplot commands:
		set xlabel 'x'
		set ylabel 'R'
		plot 'APMA1690_HW5_P3.dat'"""
		
	datafile = open('APMA1690_HW5_P3.dat','w')
	for n in range(N):
		datafile.write(str(n)+'\t'+str(R(n))+'\n')
	datafile.close()
	
