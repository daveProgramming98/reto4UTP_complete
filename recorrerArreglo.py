# ¿Como recorrer listas?
# LISTA NORMAL
a = [1, 2, 3, 4]
for valor_a in a:
    valor_a
# LISTA DE LISTAS
b = [[1, 2], [3, 4]]
for valor_b in b:
    val0_lista = valor_b[0]
    val1_lista = valor_b[1]
# LISTA DE DICCIONARIOS
c = [{"x": 1, "y": 2}, {"x": 3, "y": 4}, {"x": 5, "y": 6}]
for valor_c in c:
    val0_dict = valor_c["x"]
    val1_dict = valor_c["y"]