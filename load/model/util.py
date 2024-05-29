
import os
import sys
from urllib.parse import urlsplit
from urllib.parse import unquote
#from load.table.marca.view import MarcaView
import requests



#from load.yolov5_v2 import api_detect
#from load.model.yolo_nas import Detector

class Util():

    def Analyze(weights, source, imgsz, conf_thres):
        return api_detect.init(weights, source, imgsz, conf_thres)
    
    #def Analyze_yolo_nas(source):
     #   return Detector.onImage(source)
    
    #def Download(path,url_image):
     #   url_image=unquote(url_image) #Convertir caracteres especiales
      #  file_name, ext = os.path.splitext(os.path.basename(urlsplit(url_image).path))
       # path_img = path + file_name + '.jpg' 
        #img = open(path_img, 'wb')
        #img.write(bytearray(image))
        #return path_img
    

    def Download(path, url_image):
        url_image = unquote(url_image)  # Convertir caracteres especiales
        file_name, ext = os.path.splitext(os.path.basename(urlsplit(url_image).path))
        path_img = os.path.join(path, file_name + '.png')
        response = requests.get(url_image)
        with open(path_img, 'wb') as img:
            img.write(response.content)
        return path_img



    def QuantityElement(coordinates, label):
        quantity=0
        for coordinate in coordinates:
            if coordinate['label'] == label:
                quantity+=1      
        return quantity
    
    def PresenciaProducto(coordinates, label):
        for coordinate in coordinates:
            if coordinate['label']==label:
                return True
        return False
    

    def Overall(coordinates):
        overall=0
        for coordinate in coordinates:
            label=coordinate['label']
            if label!="OTROS" and label!="TAPAS" and label!="PRECIOS" and coordinate['own'] == 1 and not MarcaView.GetMarca(label):
                overall+=1
        return overall
    

    def Competence(coordinates):
        for coordinate in coordinates:
            if coordinate['own'] == 0 and coordinate['label'] != 'OTROS':
                return True     
        return False

    
    def Beer(coordinates):
        beer=0
        sixpack=0
        for coordinate in coordinates:
            if MarcaView.GetMarca(coordinate['label']):
                height=coordinate["coordinates"][3]-coordinate["coordinates"][1]
                width=coordinate["coordinates"][2]-coordinate["coordinates"][0]
                if width>=height:
                    sixpack+=1
                elif height>width:
                    beer+=1     
        return sixpack, beer

    
    def Structure(coordinates):
        for coordI in coordinates:
            labelI = coordI['label']
            ymin=coordI["coordinates"][1]-110
            ymax=coordI["coordinates"][3]-110
            if labelI!="OTROS" and labelI!="TAPAS" and labelI!="PRECIOS":
                for coordII in coordinates:
                    labelII = coordII['label']
                    if labelII!="OTROS" and labelII!="TAPAS" and labelII!="PRECIOS":
                        ymn=coordII["coordinates"][1]
                        ymx=coordII["coordinates"][3]
                        if (ymax < ymn) or (ymn > ymx):
                            return True
        return False
    
    def Structuredospisos(coordinates,etiquetas,altura):
        for coordI in coordinates:
            labelI = coordI['label']
            ymax=coordI["coordinates"][3]
            if labelI in etiquetas:
                for coordII in coordinates:
                    labelII = coordII['label']
                    if labelII in etiquetas:
                        ymx=coordII["coordinates"][3]
                        resta = ymax-ymx
                        if (resta>altura):
                            return True
        return False
    
    def structure_has_two_phits(coordinates, labels):
        filtered_coords = list(filter(lambda x: x['label'] in labels, coordinates))
        ymax = None
        for coord in filtered_coords:
            y_max_coord = coord["coordinates"][3]
            if ymax is None or y_max_coord > ymax:
                ymax = y_max_coord
        
        for coord in filtered_coords:
            y_max_coord = coord["coordinates"][3]
            if ymax - y_max_coord > 200:
                return True
                
        return False
    
    def StructurePisos(coordinates, etiquetas,distancia,pisos):
        conteo_pisos = []

        for coord in coordinates:
            label = coord['label']
            ymax = coord['coordinates'][3]

            if label in etiquetas:
                if not conteo_pisos:
                    conteo_pisos.append(ymax)
                else:
                    piso_encontrado = False
                    for i, piso in enumerate(conteo_pisos):
                        if ymax > piso + distancia:
                            conteo_pisos[i] = ymax
                            piso_encontrado = True
                            break
                    if not piso_encontrado:
                        conteo_pisos.append(ymax)

                if len(conteo_pisos) == pisos:
                    return True

        return False
    
    def structure_has_three_phits(coordinates, labels):
        filtered_coords = list(filter(lambda x: x['label'] in labels, coordinates))
        ymax1, ymax2, ymax3 = None, None, None
        for coord in filtered_coords:
            y_max_coord = coord["coordinates"][3]
            if ymax1 is None or y_max_coord > ymax1:
                ymax3 = ymax2
                ymax2 = ymax1
                ymax1 = y_max_coord
            elif ymax2 is None or y_max_coord > ymax2:
                ymax3 = ymax2
                ymax2 = y_max_coord
            elif ymax3 is None or y_max_coord > ymax3:
                ymax3 = y_max_coord
        
        if ymax1 - ymax2 > 110 and ymax2 - ymax3 > 110:
            return True
                
        return False
    
    def structure_adyacents(coordinates, etiquetas, cantidad):
        contador = 0
        for coordI in coordinates:
            labelI = coordI['label']
            xmax = coordI["coordinates"][2]
            xmin = coordI["coordinates"][0]
            if labelI in etiquetas:
                for coordII in coordinates:
                    labelII = coordII['label']
                    if labelII in etiquetas:
                        xmx = coordII["coordinates"][2]
                        xmn = coordII["coordinates"][0]
                        if abs(xmax - xmn) <= 10 or abs(xmx - xmin) <= 10:
                            contador += 1

        if contador >= cantidad:
            return True

        return False
    
    def ubicacion_productos_nevera(coordinates, producto):
        ubicacion = ""
        productos_adyacentes = []
        for coord in coordinates:
            label = coord['label']
            if label == producto:
                xmin = coord['coordinates'][0]
                xmax = coord['coordinates'][2]
                for coord_adyacente in coordinates:
                    if coord_adyacente['label'] != producto:
                        xmin_adyacente = coord_adyacente['coordinates'][0]
                        xmax_adyacente = coord_adyacente['coordinates'][2]
                        if (xmax < xmin_adyacente and xmin_adyacente - xmax < 50) or (xmin > xmax_adyacente and xmin - xmax_adyacente < 50):
                            productos_adyacentes.append(coord_adyacente['label'])
                ubicacion = "Primer piso"
                if coord['coordinates'][3] - coord['coordinates'][1] > 150:
                    ubicacion = "Segundo piso"
                    for coord_adyacente in coordinates:
                        if coord_adyacente['label'] != producto:
                            xmin_adyacente = coord_adyacente['coordinates'][0]
                            xmax_adyacente = coord_adyacente['coordinates'][2]
                            if (xmax < xmin_adyacente and xmin_adyacente - xmax < 50) or (xmin > xmax_adyacente and xmin - xmax_adyacente < 50):
                                productos_adyacentes.append(coord_adyacente['label'])
                    break
        return ubicacion, productos_adyacentes



    def ConverToArray(labels):
        labels=labels.split(',')
        labels.pop()
        return labels


    def RemoveImage(file_name):
        os.remove(file_name)


    def Response(Analyze, message, labels, time, coordinates, verdict, explanation, version):
        return {
            "Analyze":Analyze,
            "message": message,
            "result":labels,
            "time":time,
            "coordinates":coordinates,
            "verdict":verdict,
            "explanation":explanation,
            "version":version
        }
    