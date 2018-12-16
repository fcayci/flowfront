import matplotlib.pyplot as plt
from numpy import mgrid, random

# 1d
d1d = lambda x, kx, a: x**2 * (kx * a)
# 2d
d2d = lambda x, y, kx, ky, a, b: x**2 * (kx * a) + y**2 * (ky * b)
# 3d
d3d = lambda x, y, kx, ky, kz, a, b, c: x**2 * (kx * a) + y**2 * (ky * b) + (x+y)**2 * (kz * c)

x, y = mgrid[0:0.2:11j, 0:0.7:36j]

kx = (random.random()+1) * 1000
ky = (random.random()+1) * 1000
kz = (random.random()+1) * 1000
print('kx: {}, ky: {}, kz: {}'.format(kx, ky, kz))

r1 = d1d(y, kx, 1)
r2 = d2d(x, y, kx, ky, 1, 1)
r3 = d3d(x, y, kx, ky, kz, 1, 1, 1)

fig, axs = plt.subplots(3, 1)
ax = axs[0]
c = ax.imshow(r1, cmap='tab20b', interpolation='bicubic', origin='lower')
ax.set_title('1d flowfront')
fig.colorbar(c, ax=ax)

ax = axs[1]
c = ax.imshow(r2, cmap='tab20b', interpolation='bicubic', origin='lower')
ax.set_title('2d flowfront')
fig.colorbar(c, ax=ax)

ax = axs[2]
c = ax.imshow(r3, cmap='tab20b', interpolation='bicubic', origin='lower')
ax.set_title('3d flowfront')
fig.colorbar(c, ax=ax)

plt.show()