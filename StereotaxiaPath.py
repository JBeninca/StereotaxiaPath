# -*- coding: utf-8 -*-
# StereotaxiaPath version 22.0809
from __main__ import qt, ctk, slicer, vtk
from slicer.ScriptedLoadableModule import *

import os
import numpy as np
import logging
import time
import json
import importlib

from Resources import ui
from Resources import Maquina_Russell_Brown
from Resources import utilitarios 
from Resources import gestion_Fiduciarios 


importlib.reload(ui)
importlib.reload(Maquina_Russell_Brown)
importlib.reload(utilitarios)
importlib.reload(gestion_Fiduciarios)


class StereotaxiaPath(ScriptedLoadableModule):
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "StereotaxiaPath"
        self.parent.categories = ["Stereotaxia"]
        self.parent.dependencies = []
        self.parent.contributors = ["Dr. Jorge Beninca; Dr. Dante Lovey; Dr. Lucas Vera; Dra. Elena Zema; Dra. Anabella Gatti."]
        self.parent.helpText = "Esta es la Version 23.0130"
        self.parent.acknowledgementText = "Este modulo calcula en un corte tomografico, los 9 fiduciarios, realiza la registración con las ecuaciones de Russel Brown para la determinacion 3D de un sistema de localizadores N de un marco Estereotáxico "


class StereotaxiaPathWidget(ScriptedLoadableModuleWidget):
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        ScriptedLoadableModuleWidget.setup(self)
        ui.setupUI(self)
        

    def setup(self):
        modulo = slicer.util.modulePath("StereotaxiaPath")
        utilitarios.Inicializa_Escena(modulo)
        self.param = slicer.util.getNode("Param_data")
        

    def selectora_botones(self, modo):
        if modo == "Dicom":
            self.Setup_Escena()
            slicer.util.selectModule("DICOM")
            #slicer.util.loadVolume(self.param.GetParameter("modulo_path") + "/Paciente.nrrd")
            self.Combo1.addItems(['MICROMAR'])
            self.Combo2.addItems(['UPWARD', 'DOWNWARD'])
    

        elif modo == "Registracion":
            nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
            if nodo_volu == None:
                texto = "ERROR: no hay paciente cargados !!!"
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                return
            if self.Combo2.currentText == "Fiduciarios":
                texto = "ERROR: No se ha elegido correctamente el Marco !!!  "
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                self.Bton3.setStyleSheet(self.param.GetParameter("rojito")) 
                return        
                    
            slicer.app.layoutManager().setLayout(6)  # red panel
            name = nodo_volu.GetName()
            self.ledt1.setText(self.Combo1.currentText)
            self.ledt2.setText(self.Combo2.currentText)
            self.param.SetParameter("Paciente", name)
            self.Bton2.setText("Paciente: " + name)
            self.Bton3.setStyleSheet(self.param.GetParameter("amarillito"))
            utilitarios.centra_nodo_de_widget("Red")
            utilitarios.cambia_window_level("Red", 100, 50)
            self.Obtiene_9_Fiduciarios_f()
            
        elif modo == "Target/Entry":
            if self.E_T_flag == 0:
                self.E_T_flag = 1
                utilitarios.impri_layout_2D("Red", "Target", None)
            else:
                self.E_T_flag = 0
                utilitarios.impri_layout_2D("Red", "Entry", None)
            nodo_path = slicer.util.getNode("Path")
            self.funcion_mueve_path(nodo_path, None)        
            
        elif modo == "MPR":
            slicer.app.layoutManager().setLayout(3)  # 3d panel   
            print("cambia layout a 4-UPp")        
            
        elif modo == "Tabulado":
            slicer.app.layoutManager().setLayout(10)  # tabulado    
            print("cambia layout a tabulado")                   
            
        elif modo == "Guarda":
            self.guarda()
            
 
    def Setup_Escena(self):
        slicer.app.layoutManager().setLayout(6)  # red panel
        utilitarios.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        utilitarios.Genera_Nodo("vtkMRMLMarkupsFiducialNode", "f")
        utilitarios.Genera_Nodo("vtkMRMLMarkupsLineNode", "Path")
        self.limpia_widget()         
        self.E_T_flag = 0       # flag señalando la activacion el punto Target
        self.Combo1.setCurrentIndex(0)
        self.Combo2.setCurrentIndex(0)
        self.Bton3.setStyleSheet(self.param.GetParameter("rojito"))
       

    def on_combo1_changed(self, value):
        nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.param.SetParameter("Marco", self.Combo1.currentText)
        self.ledt1.setText(self.Combo1.currentText)
        print("Cambia la geometria: ", self.Combo1.currentText)
        

    def on_combo2_changed(self, value):
        nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.param.SetParameter("Fiduciarios", self.Combo2.currentText)
        self.ledt2.setText(self.Combo2.currentText)
        print("Cambia la geometria: ", self.Combo2.currentText)
        

    def Obtiene_9_Fiduciarios_f(self):
        print("Vino a marcacion de 9 fiduciarios")
        nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
        self.param.SetParameter("Nombre_del_Paciente", nodo_volu.GetName())
        print("El volumen con que se trabaja es = ", nodo_volu.GetName())
        print("El origen del volumen es =", nodo_volu.GetOrigin())
        
        utilitarios.modifica_origen_de_volumen(nodo_volu, [100,100,-100])
        utilitarios.centra_nodo_de_widget("Red")
                
        nodo_fidu = gestion_Fiduciarios.Inicializa_nodo("f")
        nodo_fidu.SetMaximumNumberOfControlPoints(9)

        dnodo_fidu = nodo_fidu.GetDisplayNode()
        dnodo_fidu.SetGlyphType(1)
        dnodo_fidu.SetSelectedColor(0.0, 1.0, 0.0)
        dnodo_fidu.SetActiveColor(1.0, 0.0, 0.0)
        
        transformada = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        #transformada = utilitarios.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        nodo_volu.SetAndObserveTransformNodeID(transformada.GetID())
        nodo_fidu.SetAndObserveTransformNodeID(transformada.GetID())
                
        self.mixObservador_1 = slicer.util.VTKObservationMixin()
        self.mixObservador_1.addObserver(nodo_fidu, vtk.vtkCommand.UserEvent, self.calculos_para_registracion)
        
        gestion_Fiduciarios.Marcacion_Fiduciarios("f")
             

    def calculos_para_registracion(self, caller, event):   # funcion principal MAIN del procesamiento de fiduciarios
        print("vino a callback calculos desde :", type(caller), event)
        self.mixObservador_1.removeObservers()      
        #
        #-----------------procedimiento de REGISTRACION--------------------
        #
        nodo_fidu = slicer.util.getNode("f")
        nodo_fidu.SetDisplayVisibility(False)

        fiduciarios_TAC = gestion_Fiduciarios.Lectura_Fiduciarios(nodo_fidu)
        
        self.param.SetParameter("Marco", self.Combo1.currentText)
        self.ledt1.setText(self.Combo1.currentText)
        self.param.SetParameter("Fiduciarios", self.Combo2.currentText)
        self.ledt1.setText(self.Combo2.currentText)

        geometria = self.param.GetParameter("Marco") + "_" + self.param.GetParameter("Fiduciarios")
        matriz_RB = Maquina_Russell_Brown.calculus().Ecuaciones_Russell_Brown(fiduciarios_TAC, geometria)
        if matriz_RB == None:
            texto = "ATENCION: hay un error en el Marco y/o Fiduciarios !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            self.Bton3.setStyleSheet(self.param.GetParameter("rojito")) # rojito
            return        

        array_M_RB = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        fiduciarios_3D = Maquina_Russell_Brown.calculus().Multiplica_lista_de_puntos(fiduciarios_TAC, matriz_RB)
        
        matriz_4x4  = Maquina_Russell_Brown.calculus().Analisis_por_ICP(fiduciarios_TAC, fiduciarios_3D)
        array_M_3D = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        
        transformada = vtk.vtkTransform()
        transformada.SetMatrix(matriz_4x4)
        nodo_transfo = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        nodo_transfo.SetAndObserveTransformToParent(transformada)

        utilitarios.centra_nodo_de_widget("Red")
        slicer.app.layoutManager().setLayout(3)  # 4 up

        nodo_volu = utilitarios.obtiene_nodo_de_widget("Red")
        utilitarios.Renderiza_3D_Volumen(nodo_volu)     # Renderiza el volumen en uso
        #utilitarios.Yaw_y_Pitch(20)                     # gira hacia abajo y a la derecha el volumen 
        
        Target = np.array([0.0, 0.0, 60.0])
        Entry = np.array([60.0, 60.0, 130.0])
        
        self.inicia_path(Target, Entry)    
        
        self.param.SetParameter("Fiduciarios_TAC", str(utilitarios.redondea_lista_de_puntos(fiduciarios_TAC, 2)))
        self.param.SetParameter("Array_Matrix_RB", str(array_M_RB))
        self.param.SetParameter("Fiduciarios_3D", str(utilitarios.redondea_lista_de_puntos(fiduciarios_3D, 2)))
        self.param.SetParameter("Array_Matrix_3D", str(array_M_3D))
        self.param.SetParameter("Target", str(Target[0])+ ", " + str(Target[1]) +", " + str(Target[2]))
        self.param.SetParameter("Entry" , str(Entry[0])+ ", " + str(Entry[1]) +", " + str(Entry[2]))
        self.param.SetParameter("Transformada_Position", str(utilitarios.redondea(transformada.GetPosition(), 2)))
        self.param.SetParameter("Transformada_Orientation", str(utilitarios.redondea(transformada.GetOrientation(), 2)))
        self.param.SetParameter("Registered_flag", "True")
        
        self.actualiza_widget()       
        self.Bton3.setStyleSheet(self.param.GetParameter("verdecito")) # verde


    def inicia_path(self, Target, Entry):        
        nodo_path = utilitarios.genera_linea(Target, Entry)
        # inicia observador
        self.mixObservador_5 = slicer.util.VTKObservationMixin()
        self.mixObservador_5.addObserver(nodo_path, nodo_path.PointEndInteractionEvent, self.funcion_mueve_path)
        self.funcion_mueve_path(nodo_path, None)               
        
    
    def funcion_mueve_path(self, nodo, ev):
        print("vino a mueve path")
        p_RAS = slicer.util.arrayFromMarkupsControlPoints(nodo, True)
        utilitarios.ubicar_la_punta_en_RPN(p_RAS[self.E_T_flag])
        
        Target = utilitarios.redondea((p_RAS[0]), 1)
        Entry = utilitarios.redondea((p_RAS[1]), 1)
        
        Alfa, Beta = utilitarios.calcula_angulos_con_vtk(Target, Entry)
        print("Alfa, Beta con vtk =", Alfa, Beta)
        Alfa, Beta = utilitarios.calcula_angulos_simple(Target, Entry)
        print("Alfa, Beta con formula simple =", Alfa, Beta)
         
        if (Entry[0]>=0) != (Target[0]>=0):   #(a>0) == (b>0)   #### ojo con leksell
            texto = "ATENCION: el PATH atraviesa la línea media !  "
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
        
        if Entry[0] >= 0:
            self.param.SetParameter("Target_Izq_Der_flag", str(True))
        else:
            self.param.SetParameter("Target_Izq_Der_flag", str(False))

        self.param.SetParameter("Target", str(Target[0])+ ", " + str(Target[1]) +", "+ str(Target[2]))
        self.param.SetParameter("Entry" , str(Entry[0])+ ", " + str(Entry[1]) +", "+ str(Entry[2]))
        largo_path = nodo.GetLineLengthWorld()
        self.param.SetParameter("Path_length", str(round(largo_path, 2)) +"  mm.")
        self.param.SetParameter("Target_Angulo_Alfa", str(round(Alfa, 2)) + "  grados")
        self.param.SetParameter("Target_Angulo_Beta", str(round(Beta, 2)) + "  grados")

        self.actualiza_widget()
    

    def limpia_widget(self):
        #self.ledt1.setText("")
        #self.ledt2.setText("")
        self.ledt3.setText("")
        self.ledt4.setText("")
        self.ledt5.setText("")
        #self.ledt6.setText("")
        #self.ledt7.setText("")    
        pass


    def actualiza_widget(self):
        print("vino a actualiza widget.-")
        self.ledt1.setText(self.param.GetParameter("Marco"))
        self.ledt2.setText(self.param.GetParameter("Fiduciarios"))
        self.ledt3.setText(self.param.GetParameter("Target"))
        self.ledt4.setText(self.param.GetParameter("Entry"))
        self.ledt5.setText(self.param.GetParameter("Path_length"))
        #self.ledt6.setText(param.GetParameter("Target_Angulo_Alfa"))
        #self.ledt7.setText(param.GetParameter("Target_Angulo_Beta"))    
                

    def guarda(self):
        print("vino a guardar la Escena")
        # Create a new directory where the scene will be saved into
        ref_time = time.strftime("%Y%m%d-%H%M%S")
        sceneSaveDirectory = self.param.GetParameter("modulo_path") + "/Archivo/Escena_" + ref_time
        if not os.access(sceneSaveDirectory, os.F_OK):
            os.makedirs(sceneSaveDirectory)
        # Save the scene
        if slicer.app.applicationLogic().SaveSceneToSlicerDataBundleDirectory(sceneSaveDirectory, None):
            logging.info("Escena guardada en: {0}".format(sceneSaveDirectory))
        else:
            logging.error("Escena guardar falló")
        
        # Guarda los parametros
        self.param.SetParameter("Referencia_tiempo_guarda", ref_time)
        dictio = {}
        for item in self.param.GetParameterNames():
            dictio[item] = self.param.GetParameter(item)
        js = json.dumps(dictio)
        fp = open(sceneSaveDirectory + "/Parametros_" + ref_time + ".json", 'a')
        fp.write(js)
        fp.close()

 