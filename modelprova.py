from model.model import Model

model = Model()
model.creaGrafo(7, '2016-01-01 00:00:00', '2018-12-28 00:00:00')
print(model.grafo)