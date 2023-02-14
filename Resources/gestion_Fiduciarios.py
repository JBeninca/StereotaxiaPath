 # -*- coding: utf-8 -*-
# Estereotaxia_Simplex version 16.1206

from __main__ import slicer, vtk
from Resources import utilitarios
import importlib

importlib.reload(utilitarios)


def __init__():
        nombre_Nodo = ""
        total_de_Fiduciarios = 1
        mixObservador_2 = slicer.util.VTKObservationMixin()  # agrega observador
    

def Lectura_Fiduciarios(nodo_fidu):
    print("Lectura de los fiduciarios.-")
    fiduciarios_TAC = slicer.util.arrayFromMarkupsControlPoints(nodo_fidu)
    return fiduciarios_TAC.tolist()
    

def Marcacion_Fiduciarios(nombre):
    activo = 1
    nodo_fidu = slicer.util.getNode(nombre)
    nodo_fidu.SetLocked(False)    
    interaccion_Markups(nodo_fidu, 1)
    mixObservador_2 = slicer.util.VTKObservationMixin()  # agrega observador
    mixObservador_2.addObserver(nodo_fidu, nodo_fidu.PointPositionDefinedEvent, onFiducialAgregado)
    

def onFiducialAgregado(nodo_fidu, event):
    """ callback de evaluacion de cada fiduciario luego de marcado """
    nombre_Nodo = nodo_fidu.GetName()
    nume_fidu = nodo_fidu.GetNumberOfControlPoints()
    total_fidu = nodo_fidu.GetMaximumNumberOfControlPoints()
    print("Markup # ", nombre_Nodo, nume_fidu)
    if nombre_Nodo == "f":   # corrige el fiduciario a su centroide
        RAS_fidu = [0, 0, 0]
        nodo_fidu.GetNthFiducialPosition(nume_fidu-1, RAS_fidu)
        nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
        fidu_centrado = utilitarios.Obtiene_Centro_de_Masa(nodo_volu, nume_fidu-1, RAS_fidu,  20, -200)
        # modificacion de la posicion del fiduciario
        nodo_fidu.SetNthControlPointPositionFromArray(nume_fidu-1, fidu_centrado[:3])
    if nume_fidu == total_fidu:  # se terminó la colecta
        #mixObservador_2.removeObservers()
        nodo_fidu.SetLocked(True)
        print("Se termina de registrar el/los fiduciarios de :", nombre_Nodo) 
        interaccion_Markups(nodo_fidu, 0)  # finaliza interaccion
        nodo_fidu.InvokeEvent(1000)  # para lector de eventos a MAIN
        

def interaccion_Markups(nodo_fidu, activo):
    #  activo = True para interactuar False para no
    nodo_logi = slicer.modules.markups.logic()
    nodo_logi.SetActiveListID(nodo_fidu)
    nodo_sele = slicer.mrmlScene.GetNodeByID("vtkMRMLSelectionNodeSingleton")
    nodo_sele.SetReferenceActivePlaceNodeClassName("vtkMRMLMarkupsFiducialNode")
    nodo_interac = slicer.mrmlScene.GetNodeByID("vtkMRMLInteractionNodeSingleton")
    nodo_interac.SetPlaceModePersistence(activo)
    nodo_interac.SetCurrentInteractionMode(activo)


def Inicializa_nodo(nombre_Nodo):
    Borra_nodo(nombre_Nodo)  # intenta borrar nodo anterior
    nodo = Genera_nodo(nombre_Nodo)  # sin puntos fiduciarios
    return nodo


def Genera_nodo(nombre_Nodo):
    nodo = slicer.vtkMRMLMarkupsFiducialNode()
    nodo.SetName(nombre_Nodo)
    nodo.SetScene(slicer.mrmlScene)
    slicer.mrmlScene.AddNode(nodo)
    print("ha generado fiducial nodo =", nombre_Nodo)
    return nodo


def Borra_nodo(nombre_Nodo):
    try:
        nodo = slicer.util.getNode(nombre_Nodo)
        if nodo.IsA("vtkMRMLMarkupsFiducialNode"):
            slicer.mrmlScene.RemoveNode(nodo)
            print("ha borrado =", nombre_Nodo)
        else:
            print("no es fiducial node.")
    except:
        print("ha fallado en borrar nodo =", nombre_Nodo)


def Borra_nodos_por_clase(nombre_Nodo):
    nodos = slicer.util.getNodesByClass("vtkMRMLMarkupsFiducialNode")
    for nodo in nodos:   # borra nodos antiguos
        if nodo.GetName() == nombre_Nodo:
            slicer.mrmlScene.RemoveNode(nodo)
            print("ha borrado nodo =", nodo.GetName())


def Borra_puntos_fiduciarios(nombre_Nodo):
    nodo = slicer.util.getNode(nombre_Nodo)
    nodo.RemoveAllMarkups()
    print("se removieron los markups de= ", nombre_Nodo)
    
