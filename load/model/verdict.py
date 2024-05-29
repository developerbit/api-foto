from ast import And

class Verdict():

    def LogicaNegocio(quantity=0, cantidad_etiquetas=0, etiquetas=0):
        print(cantidad_etiquetas)
        #print(etiquetas)
        if quantity >= 2: #logica negocio 
            if cantidad_etiquetas==0:
                if quantity==0:
                    return 1, "La nevera cuenta con la cantidad necesaria"  #Explicacion 
                else:
                    return 0, "Se detecta competencia" 
            else:
                return 0, "se detecta contaminantes"
        else:
            return 0, "No cuenta con la cantidad necesaria"  #Explicacion