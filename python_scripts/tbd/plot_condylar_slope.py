import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(0, 14, 100)

slope_one = 0.0052*x**3-0.072*x**2-0.387*x ## J.-C. Coutant et al and Haiying Wen, Weiliang Xu

slope_two = [5*np.cos(i/13*math.pi)-5 for i in x], ## Peck, Hannam 2000

#trapezoidal parts

curvParams = [ 0.0, # x0
	 -0.5, # y0
	 2.5, # xf
	 -0.1, # yf
	 0.0, # initial slope
	 -20.0 #final slope
     ]
curvParams2 = [2.5, # x0
	 -0.6, # y0
	 7.5, # xf
	 -6.4, # yf
	 -50.0, # initial slope
	 -5.0 #final slope
     ]
curvParams3 = [ 10.0, # x0
	-7.0, # y0
	 2.0, # xf
	 2.0, # yf
	 20.0, # initial slope
	 100.0 #final slope
     ]

#triangular parts

curvParams_triang1 = [0.0, # x0
	 0.5, # y0
	 10.0, # xf
	 -7.5, # yf
	 -50.0, # initial slope
	 -30.0 #final slope
     ]
curvParams_triang2 = [ 10.0, # x0
	-7.0, # y0
	 2.0, # xf
	 2.0, # yf
	 30.0, # initial slope
	 100.0 #final slope
     ]

# CG group

ats_1 = [ 0, # x0
	0.0, # y0
	 10.52/2, # xf
	 -4.0, # yf
	 0.0, # initial slope
	 -30.42 #final slope
     ]

ats_2 = [ 10.52/2, # x0
	-4.0, # y0
	 10.52/2, # xf
	 -4.0, # yf
	 -30.42, # initial slope
	 0.0 #final slope
     ]

pp = [ 10.52, # x0
	-8.0, # y0
	 3.75, # xf
	 4.0, # yf
	 0.0, # initial slope
	 30.42 #final slope
     ]


def getCubicParams(xf, yf, slopeInit, slopeFinal):
    mat = np.array([
    [0, 0, 0, 1],
    [xf**3, xf**2, xf, 1],
    [0, 0, 1, 0],
    [3.0*xf**2, 2.0*xf, 1, 0]])
    y = np.array([0, yf, np.radians(slopeInit), np.radians(slopeFinal)])
    a = np.linalg.inv(mat).dot(y)
    return np.flipud(a)

def getCurvPts(params, numSegments):
    a = getCubicParams(params[2], params[3], params[4], params[5])
    print(a)
    #a = [0, -0.387, -0.072, 0.0052]
    deltax = params[2] #- params[0] # xf-x0
    step = deltax / numSegments
    pts_x = []
    pts_y = []
    for i in range(numSegments+1):
        x = step*i # params[0] + step * i
        y = params[1] + a[3] * x**3 + a[2] * x**2 + a[1] * x + a[0]
        pts_x.append(params[0] + step * i) #x
        pts_y.append(y)

    return pts_x, pts_y


a = getCubicParams(curvParams2[2], curvParams2[3], curvParams2[4], curvParams2[5])

slope_three = a[3] * x**3 + a[2] * x**2 + a[1] * x + a[0]

print(len(slope_two))
print(2*len(x))

points = [-x[i/2] if i%2 == 0 else slope_two[0][i/2] for i in range(2*len(x))]
lastValue = points[len(points)-1]

for i in range(1, 20):
	points.append(-(16+0.2*i))
	points.append(lastValue)

print(points)

plt.plot(x, slope_one, c="b", label="Wen")
plt.plot(x, slope_two[0], c="r", label="Peck, Hannam")

pts_x, pts_y = getCurvPts(curvParams, 20)
plt.plot(pts_x, pts_y, c="g", label="trapezoidal")
pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(curvParams2, 20)
plt.plot(pts_x, pts_y, c="g")
pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(curvParams3, 20)
plt.plot(pts_x, pts_y, c="g")

pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(curvParams_triang1, 20)
print(pts_x, pts_y)
#plt.plot(pts_x, pts_y, c="y", label="triangular")
pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(curvParams_triang2, 20)
#plt.plot(pts_x, pts_y, c="y")

pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(ats_1, 20)
print(pts_x, pts_y)
plt.plot(pts_x, pts_y, c="y", label="CG")
pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(ats_2, 20)
plt.plot(pts_x, pts_y, c="y")
pts_x = []
pts_y = []
pts_x, pts_y = getCurvPts(pp, 20)
plt.plot(pts_x, pts_y, c="y")

plt.axis("equal")
plt.title("condylar slopes")
plt.xlabel("x")
plt.ylabel("z")
plt.legend()
plt.show()


## Artisynth slope is defined by points,
## therefore for each individual an individual set of points can be set
## for the four classes, create point set
## the slope as used by Wen rather fits a round condylar shape
## Peck, Hannam curve fits oval condyles
# missing a trapezoidal and triangular implementation

## plot incisor trajectory and difference for each of these
## for evaluation could (should) be compared to actual incisor trajectory of patients with these condylar shapes
## plot how controller this works for any of these shapes
