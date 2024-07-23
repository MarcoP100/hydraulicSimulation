import matplotlib
matplotlib.use('TkAgg')  # Usa il backend TkAgg per l'output grafico

import matplotlib.pyplot as plt

# Genera un semplice grafico
plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
plt.title('Test Plot')
plt.xlabel('x-axis')
plt.ylabel('y-axis')

# Mostra il grafico
plt.show()
