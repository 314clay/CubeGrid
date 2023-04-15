import matplotlib.pyplot as plt

points = [[5, 10], [10, 5], [10, 10], [3, 0], [8, 0], [8, 5], [9, 0], [9, 8], [1, 8], [0, 0], [8, 0], [8, 8]]

x = [p[0] for p in points]
y = [p[1] for p in points]

plt.scatter(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Points')
plt.show()
