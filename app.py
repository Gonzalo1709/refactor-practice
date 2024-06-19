import csv
# el programa deberá calcular el ganador de votos validos considerando que los siguientes datos son proporcionados:
# region,provincia,distrito,dni,candidato,esvalido
# Si hay un candidato con >50% de votos válidos retornar un array con un string con el nombre del ganador
# Si no hay un candidato que cumpla la condicion anterior, retornar un array con los dos candidatos que pasan a segunda vuelta
# Si ambos empatan con 50% de los votos se retorna el que apareció primero en el archivo
# el DNI debe ser valido (8 digitos)

class Voto:
    def __init__(self, region, provincia, distrito, dni, candidato, esvalido):
        self.region = region
        self.provincia = provincia
        self.distrito = distrito
        self.dni = dni
        self.candidato = candidato
        self.esvalido = True if esvalido == '1' and len(dni) == 8 else False

    def __str__(self):
        return self.region + ' ' + self.provincia + ' ' + self.distrito + ' ' + self.dni + ' ' + self.candidato + ' ' + self.esvalido
    
class DatosVotos:
    def __init__ (self, ruta = '', lista = []):
        self.storedData = []
        if ruta == '' and lista == []:
            print('No ingreso datos')
        elif ruta == '' and lista != []:
            for item in lista:
                self.storedData.append(Voto(item[0], item[1], item[2], item[3], item[4], item[5]))
        else:
            self.storedData = self.leerdatos(ruta)

    def leerdatos(self, archivo):
        data = []
        with open(archivo, 'r') as csvfile:
            next(csvfile)
            datareader = csv.reader(csvfile)
            for fila in datareader:
                data.append(Voto(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5]))
        self.storedData = data
        return data
    
class CalculaGanador:
    def calcularganador(self, votos):
        votosxcandidato, ordenado = self.iterarVotos(votos)
        cantidadTotalVotos = len(votos)
        for candidato in votosxcandidato:
            print('candidato: ' + candidato + ' votos validos: ' + str(votosxcandidato[candidato]))
        if ordenado[0][1][1] > cantidadTotalVotos / 2 or (ordenado[0][1][1] == cantidadTotalVotos / 2 and ordenado[1][1][1] == cantidadTotalVotos / 2):
            return ordenado[0]
        else:
            return [ordenado[0], ordenado[1]]

    def iterarVotos(self, votos):
        votosxcandidato = {}
        for voto in votos:
            if not voto.candidato in votosxcandidato:
                votosxcandidato[voto.candidato] = [voto.candidato, 0]
            if voto.esvalido:
                votosxcandidato[voto.candidato][1] = votosxcandidato[voto.candidato][1] + 1
        ordenado = sorted(votosxcandidato.items(), key=lambda item:item[1][1], reverse=True)
        return votosxcandidato, ordenado

def testEleccion():
    # Test segunda vuelta (retorna los dos candidatos con mas votos validos)
    dLista = DatosVotos(lista = [
        ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '0'],
        ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1'],
    ])
    c = CalculaGanador()
    assert c.calcularganador(dLista.storedData) == [('Aundrea Grace', ['Aundrea Grace', 2]), ('Eddie Hinesley', ['Eddie Hinesley', 1])], 'No se calculo correctamente el empate'
    # Test ganador unico
    dLista = DatosVotos(lista = [
        ['Áncash', 'Asunción', 'Acochaca', '40810062', 'Eddie Hinesley', '0'],
        ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1'],
    ])
    assert c.calcularganador(dLista.storedData) == ('Aundrea Grace', ['Aundrea Grace', 3]), 'No se calculo correctamente el ganador'
    # Test empate (deberia retornar el primero que fue agregado a la lista)
    dLista = DatosVotos(lista = [
        ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Eddie Hinesley', '1'],
    ])
    print(c.calcularganador(dLista.storedData))
    assert c.calcularganador(dLista.storedData) == ('Eddie Hinesley', ['Eddie Hinesley', 2]), 'No se calculo correctamente el empate'

    print('Test de eleccion exitoso')

def testVoto():
    dLista = DatosVotos(lista = [
        ['Áncash', 'Asunción', 'Acochaca', '408', 'Eddie Hinesley', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '57533597', 'Eddie Hinesley', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '86777322', 'Aundrea Grace', '1'],
        ['Áncash', 'Asunción', 'Acochaca', '23017965', 'Aundrea Grace', '1']
    ])
    assert dLista.storedData[0].esvalido == False, 'Un voto que no es valido y fue marcado como valido'
    print('Test de voto exitoso')

def testLecturaArchivo(ruta):
    dArchivo = DatosVotos(ruta = ruta)
    assert len(dArchivo.storedData) > 0, 'No se cargaron datos'
    assert type(dArchivo.storedData[0]) == Voto, 'No se cargaron datos de tipo Voto'
    assert type(dArchivo.storedData[0].candidato) == str, 'El candidato no es un string'
    assert type(dArchivo.storedData[0].esvalido) == bool, 'El esvalido no es un boolean'
    assert type(dArchivo.storedData[0].dni) == str, 'El DNI no es un string'
    assert type(dArchivo.storedData[0].distrito) == str, 'El distrito no es un string'
    assert type(dArchivo.storedData[0].provincia) == str, 'La provincia no es un string'
    assert type(dArchivo.storedData[0].region) == str, 'La region no es un string'
    print('Test de lectura de archivo exitoso')

testEleccion()
testVoto()
testLecturaArchivo('0204.csv')