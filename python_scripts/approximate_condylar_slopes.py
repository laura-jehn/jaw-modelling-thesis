import matplotlib.pyplot as plt
import numpy as np
from numpy import tan
import math

plt.rcParams.update({'font.size': 12})

def plot_condylar_slope(slope, x_ATS, x_ATC, group_label):
	dy = tan(np.radians(slope))
	pts_x = []
	pts_y = []

	# Intro:
	xmax0 = 3  # range from -2 to +1
	a = -dy / (2 * xmax0)  # coefficient a of parabola so that slope at x = xmax0 equals slope of ATS
	y0 =  a * (xmax0) ** 2  # y value at x = xmax0

	for i in range(11):
		x = (i) / 10 * xmax0
		y = -a * x * x + y0 + dy
		pts_x.append(x - 2)
		pts_y.append(y)

    #ATS
	for i in range(1, 11):
		x = i / 10 * x_ATS
		if x > 1:
			y = dy * x
			if i==0 or i==10:
				pts_x.append(x)
				pts_y.append(y)
	y_end = y

	# ATC+PP
	a = -dy / x_ATC  # coefficient a of parabola so that slope at x = x_ATC/2 equals slope of ATS
	y1 = a * (x_ATC / 2) ** 2  # y value at x = x_ATC/2
	for i in range(1, 11):
		x = (i - 5) / 10 * x_ATC
		y = a * x * x
		pts_x.append(x + x_ATS + x_ATC / 2)
		pts_y.append(y - y1 + y_end)

	print(group_label)

	pts_xy = []
	for i in range(len(pts_x)):
		pts_xy.append(-round(pts_x[i], 2))
		pts_xy.append(round(pts_y[i], 2))

	print(pts_xy)

	print(len(pts_xy))

	plt.plot(pts_x, pts_y, label = group_label)

	return

slope_CG = -30.42
slope_RG = -47.25
slope_TG = -18.28
xATS_CG = 10.52
xATS_RG = 6.12
xATS_TG = 11.42
xPP_CG = 4.52
xPP_RG = 3.75
xPP_TG = 9.5

plot_condylar_slope(slope_CG, xATS_CG, xPP_CG, "CG (30.42°)")
plot_condylar_slope(slope_RG, xATS_RG, xPP_RG, "RG (47.25°)")
plot_condylar_slope(slope_TG, xATS_TG, xPP_TG, "TG (18.28°)")

x = np.linspace(-2, 14, 100)

#slope_one = 0.0052*x**3-0.072*x**2-0.387*x ## J.-C. Coutant et al and Haiying Wen, Weiliang Xu

#plt.plot(x, slope_one, label="Wen")

plt.grid()
plt.axis("equal")
#plt.title("condylar slopes")
plt.xlabel("X (mm)")
plt.ylabel("Z (mm)")
plt.axis("equal")
plt.legend()
plt.show()
