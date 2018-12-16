from pylab import mgrid, contourf, cm, show

f = lambda x,y: (1 - x)**2 + 100*(y - x**2)**2

x,y = mgrid[-1.5:1.5:50j, 0.7:2:50j]

contourf(x, y, f(x,y))
show()