import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.size': 14})

# name, slope inclination, xATS, xPP
CGparams = ['CG', -30.42, 10.52, 4.52]
RGparams = ['RG', -47.25, 6.12, 3.75]
TGparams = ['TG', -18.28, 11.42, 9.5]

groups = [CGparams, RGparams, TGparams]

# approximates a R -> R function for the condylar slope
# returns function value at x
# function is defined by params (containing name, inclination, xATS and xPP of the slope)
# first part of the function is linear (for x<xATS), and a quadratic part follows
# for xATS < x < xATS + xATC + xPP
def condylar_slope(x, params):
	slope = params[1]
	xATS = params[2]
	xPP = params[3]
	xATC = 2.0

	dy = np.tan(np.radians(slope))

	if x < -2:
		y = -99
		print("x is out of range")
	elif x < 1:
		xmax0 = 3  # range from -2 to +1
		a = -dy / (2 * xmax0)  # coefficient a of parabola such that slope at x = xmax0 equals slope of ATS
		y0 =  a * (xmax0) ** 2  # y value at x = xmax0
		y = -a * (x + 2) ** 2 + y0 + dy
	elif x < xATS:
		y = dy * x
	elif x < xATS + 2.2 * xATC: # ATC+PP
		a = -dy / (2 * xATC)  # coefficient a of parabola such that slope at x = -x_ATC equals slope of ATS
		y1 = a * xATC ** 2  # y value at x = x_ATC
		xshifted = x - xATS - xATC
		y = a * xshifted ** 2 - y1 + dy * xATS
	else:
		y = -99

	return y

for g in groups:
	pts_x = []
	pts_y = []
	for j in range(-20,160, 2):
		y = condylar_slope(j/10, g)
		if y > -10:
			pts_x.append(j/10)
			pts_y.append(y)
	plt.plot(pts_x, pts_y, label = (g[0]+" ("+str(-1*g[1])+"°)"))

plt.grid()
plt.axis("equal")
#plt.title("condylar slopes")
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.axis("equal")
plt.legend()
plt.show()
