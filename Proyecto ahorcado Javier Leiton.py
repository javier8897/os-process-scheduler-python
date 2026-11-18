#Proyecto ahorcado Javier Leiton 
#fecha: 15/04/2026
 #palabras y pistas 
import random
palabras = [ 
    ["Casa", "Es un lugar para vivir"],
    ["Perro", "Es un animal domestico"],
    ["Arbol", "Se observa en los bosques"],
    ["Montaña", "Es grande y se ve a lo lejos"],
    ["Semaforo", "Indica si pasar o no"],
    ["Computadora", "Compuesta de ceros y unos"],
]
eleccion = random.choice(palabras)

palabra = eleccion[0]
pista = eleccion[1]

print("*" * len(palabra), pista)

intentos = 6
letras_incorrectas = []
letras_correctas =[]

while intentos > 0:
 #Menu del jugador 
    estado_actual = ""
    for letra in palabra:
        if letra.lower() in letras_correctas:
            estado_actual += letra + " "
        else:
            estado_actual += "_ "  
    print("\nPalabra: ", estado_actual)
    print("Intentos restantes: ", intentos)
    print("Letras usadas:", " ".join(letras_incorrectas))
    
#Entrada de palabras o letras 
    entrada = input("Adivina una letra o la palabra completa: ").strip().lower()
    
#Verificar si es la palabra completa
    if entrada == palabra.lower():
        print("Felicidades Adivinaste la palabra")
        break
    
    #verificacion de letras 
    if not entrada.isalpha() or len(entrada) != 1:
        print("Por favor, ingresa solo una letra o la palabra que crees que sea")
        continue
    
#ver si la palabra ya se uso
    if entrada in letras_correctas or entrada in letras_incorrectas:
        print("La letra ya se uso intenta con otra")
        continue
    
#Letras correctas 
    if entrada in palabra.lower():
        letras_correctas.append(entrada)
        print("Bien, la letra está en la palabra")
    else:
        letras_incorrectas.append(entrada)
        intentos -= 1
        print("Incorrecto")

   #fin
if intentos == 0:
    print("Te quedaste sin intentos")
    print("La palabra era: ", palabra)