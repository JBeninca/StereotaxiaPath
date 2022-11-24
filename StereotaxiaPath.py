# -*- coding: utf-8 -*-
# StereotaxiaPath version 22.0809
from __main__ import qt, ctk, slicer, vtk
from slicer.ScriptedLoadableModule import *

import os
import numpy as np
import logging
import time
import ast   # para eval seguras
import importlib

from Recursos import Maquina_Russell_Brown
from Recursos import utilitarios 
from Recursos import gestion_Fiduciarios 

importlib.reload(Maquina_Russell_Brown)
importlib.reload(utilitarios)
importlib.reload(gestion_Fiduciarios)

class StereotaxiaPath(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class"""
    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "StereotaxiaPath"
        self.parent.categories = ["Stereotaxia"]
        self.parent.dependencies = []
        self.parent.contributors = ["Dr. Jorge Beninca; Dr. Dante Lovey; Dr. Lucas Vera; Dra. Elena Zema; Dra. Anabella Gatti."]
        self.parent.helpText = "Esta es la Version 22.0901"
        self.parent.acknowledgementText = "Este modulo calcula en un corte tomografico, los 9 fiduciarios, realiza la registración con las ecuaciones de Russel Brown para la determinacion 3D de un sistema de localizadores N de un marco Estereotáxico "

class StereotaxiaPathWidget(ScriptedLoadableModuleWidget):
    """Uses ScriptedLoadableModuleWidget base class"""    
    def __init__(self, parent=None):
        ScriptedLoadableModuleWidget.__init__(self, parent)
        self.utiles = utilitarios.util()
        self.gest = gestion_Fiduciarios.gestion()
        self.maqui = Maquina_Russell_Brown.calculus()

        

    def setup(self):
        ScriptedLoadableModuleWidget.setup(self)
        self.Registracion_Bton = ctk.ctkCollapsibleButton()
        self.Registracion_Bton.text = "Registración y cálculo del Target"
        self.Registracion_Bton.collapsed = False
        self.layout.addWidget(self.Registracion_Bton)
        self.Grilla1 = qt.QGridLayout(self.Registracion_Bton)
        self.Layout_Bton = ctk.ctkCollapsibleButton()
        self.Layout_Bton.text = "Gráfica"
        self.Layout_Bton.collapsed = False
        self.layout.addWidget(self.Layout_Bton)
        self.Grilla2 = qt.QGridLayout(self.Layout_Bton)
        self.Resultados_Bton = ctk.ctkCollapsibleButton()
        self.Resultados_Bton.text = "Resultados"
        self.Resultados_Bton.collapsed = False
        self.layout.addWidget(self.Resultados_Bton)
        self.Grilla3 = qt.QGridLayout(self.Resultados_Bton)
        
        #self.Bton1 = qt.QPushButton("Inicializa")
        self.Bton2= qt.QPushButton("abre Archivo")
        self.Bton3 = qt.QPushButton("Registración ")
        #self.Bton4 = qt.QPushButton("Traza path")
        self.Bton5 = qt.QPushButton("Target / Entry")
        #self.Bton6 = qt.QPushButton("Entry")
        self.Bton7 = qt.QPushButton("Dieño MPR")
        self.Bton8 = qt.QPushButton("Diseño tabulado")
        self.Bton9 = qt.QPushButton("Guarda la Sesión")
        self.Bton20 = qt.QPushButton("prueba 1")
        self.Bton21 = qt.QPushButton("prueba 2")
        
        self.Combo1 = qt.QComboBox()
        self.Combo1.setEditable(True)
        self.Combo1.lineEdit().setAlignment(qt.Qt.AlignCenter)
        self.Combo1.addItems(["Marco",'MICROMAR', 'LEKSELL'])
        self.Combo2 = qt.QComboBox()
        self.Combo2.setEditable(True)
        self.Combo2.lineEdit().setAlignment(qt.Qt.AlignCenter)
        self.Combo2.addItems(["Fiduciarios", 'UPWARD', 'DOWNWARD'])
      
        self.Lbl0 = qt.QLabel("")

        #self.textEdit = qt.QTextEdit("")
        #self.textEdit.setMaximumSize(500, 200)
        self.lbl0 = qt.QLabel("Geometría :")
        self.lbl0.setAlignment(qt.Qt.AlignCenter)
        
        self.Grilla1.addWidget(self.Bton2, 1, 0, 1, 0)
        self.Grilla1.addWidget(self.lbl0, 2, 0)
        self.Grilla1.addWidget(self.Combo1, 2, 1)
        self.Grilla1.addWidget(self.Combo2, 2, 2)
        self.Grilla1.addWidget(self.Bton3, 3, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton4, 4, 0)
        #self.Grilla1.addWidget(self.Bton6, 5, 1)
        self.Grilla1.addWidget(self.Lbl0, 6, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton5, 7, 2)
        self.Grilla1.addWidget(self.Bton9, 9, 0, 1, 0)
        #self.Grilla1.addWidget(self.Bton20, 10, 0 )
        #self.Grilla1.addWidget(self.Bton21, 10, 1 )
  

        #self.Grilla2.setMaximunSize(200, 200)
        self.Grilla2.addWidget(self.Bton5, 5, 2)
        self.Grilla2.addWidget(self.Bton7, 5, 0)
        self.Grilla2.addWidget(self.Bton8, 5, 1)
        
        #self.Grilla3.addWidget(self.textEdit, 13, 0)
        #self.textEdit = qt.QTextEdit()
        #self.textEdit.setMaximumSize(500, 200)
        #self.Grilla3.addWidget(self.textEdit, 13, 0)
        
        self.lbl1 = qt.QLabel("Marco :")
        self.ledt1 = qt.QLineEdit()
        self.lbl2 = qt.QLabel("Fiduciarios :")
        self.ledt2 = qt.QLineEdit()
        self.lbl3 = qt.QLabel("Target :")
        self.ledt3 = qt.QLineEdit()
        self.lbl4 = qt.QLabel("Entry :")
        self.ledt4 = qt.QLineEdit()
        self.lbl5 = qt.QLabel("Trayectoria :")
        self.ledt5 = qt.QLineEdit()
        #self.lbl6 = qt.QLabel("ang Alfa :")
        #self.ledt6 = qt.QLineEdit()
        #self.lbl7 = qt.QLabel("ang Beta :")
        #self.ledt7 = qt.QLineEdit()
        self.lbl9 = qt.QLabel(" ")

        self.Grilla3.addWidget(self.lbl1, 1, 0)
        self.Grilla3.addWidget(self.ledt1, 1, 1)
        self.Grilla3.addWidget(self.lbl2, 1, 2)
        self.Grilla3.addWidget(self.ledt2, 1, 3)
        self.Grilla3.addWidget(self.lbl3, 3, 0)
        self.Grilla3.addWidget(self.ledt3, 3, 1)
        self.Grilla3.addWidget(self.lbl4, 3, 2)
        self.Grilla3.addWidget(self.ledt4, 3, 3)
        self.Grilla3.addWidget(self.lbl5, 4, 0)
        self.Grilla3.addWidget(self.ledt5, 4, 1)
        self.Grilla3.addWidget(self.lbl5, 5, 0)
        self.Grilla3.addWidget(self.ledt5, 5, 1)
        #self.Grilla3.addWidget(self.lbl6, 6, 0)
        #self.Grilla3.addWidget(self.ledt6, 6, 1)
        #self.Grilla3.addWidget(self.lbl7, 6, 2)
        #self.Grilla3.addWidget(self.ledt7, 6, 3)

        self.Grilla3.addWidget(self.lbl9, 8, 0, 1, 0)
        self.Grilla3.addWidget(self.Bton9, 9, 0, 1, 0)

        self.layout.addStretch(1)   # Add vertical spacer
        
        # conecciones con las clases logicas
        #
        #self.Bton1.clicked.connect(lambda: self.selectora_botones("Inicializa"))
        self.Bton2.clicked.connect(lambda: self.selectora_botones("Dicom"))
        self.Bton3.clicked.connect(lambda: self.selectora_botones("Registracion"))
        #self.Bton4.clicked.connect(lambda: self.selectora_botones("Path"))
        self.Bton5.clicked.connect(lambda: self.selectora_botones("Target/Entry"))
        #self.Bton6.clicked.connect(lambda: self.selectora_botones("Entry"))
        self.Bton9.clicked.connect(lambda: self.selectora_botones("Guarda"))
        self.Bton7.clicked.connect(lambda: self.selectora_botones("MPR"))
        self.Bton8.clicked.connect(lambda: self.selectora_botones("Tabulado"))
        self.Bton20.clicked.connect(lambda: self.selectora_botones("Prueba1"))
        self.Bton21.clicked.connect(lambda: self.selectora_botones("Prueba2"))
        
        self.Combo1.currentTextChanged.connect(self.on_combo1_changed)
        self.Combo2.currentTextChanged.connect(self.on_combo2_changed)
     
        ######################  Incio de la actividad del widget ##############
        #slicer.mrmlScene.Clear(0)
        #self.utiles.Genera_Nodo("vtkMRMLScriptedModuleNode", "Param_data")
        self.Inicializa_Escena()
        #######################################################################
 

    def selectora_botones(self, modo):
        if modo == "Dicom":
            self.Bton2.setText("abre Archivo")
            self.Inicializa_Escena()
            slicer.util.selectModule("DICOM")

        elif modo == "Registracion":
            nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
            param = slicer.util.getNode("Param_data")
            if nodo_volu == None:
                texto = "ERROR: no hay paciente cargados !!!"
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                return
            if self.Combo1.currentText == "Marco" or self.Combo2.currentText == "Fiduciarios":
                texto = "ATENCION: No se ha elegido correctamente el Marco !!!  "
                slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
                self.Bton3.setStyleSheet(self.rojito) # verde
                return        
            self.Setup_Escena()
            slicer.app.layoutManager().setLayout(6)  # red panel
            param = slicer.util.getNode("Param_data")
            param.SetParameter("Paciente", nodo_volu.GetName())
            self.Bton2.setText(nodo_volu.GetName())
            self.Bton3.setStyleSheet(self.amarillito)
            self.utiles.centra_nodo_de_widget("Red")
            self.utiles.cambia_window_level("Red", 100, 50)
            self.Obtiene_9_Fiduciarios_f()
            self.utiles.Renderiza_3D_Volumen(nodo_volu)         # Renderiza el volumen en uso
       
        elif modo == "Target/Entry":
            if self.E_T_flag == 0:
                self.E_T_flag = 1
                self.utiles.impri_layout_2D("Red", "Target", None)
            else:
                self.E_T_flag = 0
                self.utiles.impri_layout_2D("Red", "Entry", None)
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

        elif modo == "Renderiza":
            nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
            self.utiles.Renderiza_3D_Volumen(nodo_volu)

 
    def Inicializa_Escena(self):
        slicer.mrmlScene.Clear(0)

        self.modulo = slicer.util.modulePath("StereotaxiaPath")
        print("modulo: ", self.modulo)
        self.rootPath = slicer.mrmlScene.GetRootDirectory()
        print("root path: ", self.rootPath)
        self.moduloPath = os.path.split(self.modulo)[0]
        print("modulo path:", self.moduloPath)
        self.archivoPath = self.moduloPath + "/Archivo"
        self.escenaPath = self.moduloPath + "/Espacio_Marco/_Marco_Scene.mrml"

        self.verdecito = "background-color:rgb(95, 127, 117)"
        self.rojito = "background-color:rgb(143,84,84)"
        self.amarillito = "background-color:rgb(214, 200, 139)"
        self.color_default = "background-color:"

        self.E_T_flag = 0   # flag señalando la activacion el punto Target

        self.utiles.Genera_Nodo("vtkMRMLScriptedModuleNode", "Param_data")

        ###
        slicer.util.loadVolume(self.moduloPath + "/Paciente.nrrd")
        ####
        
        self.Combo1.setCurrentIndex(0)
        self.Combo2.setCurrentIndex(0)
        
        self.Setup_Escena()
        
    def Setup_Escena(self):
        slicer.app.layoutManager().setLayout(6)  # red panel
               
        self.utiles.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        self.utiles.Genera_Nodo("vtkMRMLMarkupsFiducialNode", "f")
        self.utiles.Genera_Nodo("vtkMRMLMarkupsLineNode", "Path")
         
        #param = self.utiles.Genera_Nodo("vtkMRMLScriptedModuleNode", "Param_data")
 
        #param.SetParameter("Marco", self.Combo1.currentText)  # ****
        #param.SetParameter("Fiduciarios", self.Combo2.currentText)  # ****
        #param.SetParameter("Registered_flag", "False")
        #self.actualiza_widget(None, None)

        self.limpia_widget()         
        self.Bton3.setStyleSheet(self.rojito)
       

    def on_combo1_changed(self, value):
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.Setup_Escena()
        param = slicer.util.getNode("Param_data")
        param.SetParameter("Marco", self.Combo1.currentText)
        self.ledt1.setText(self.Combo1.currentText)
        print("Cambia la geometria: ", self.Combo1.currentText)
        

    def on_combo2_changed(self, value):
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        if nodo_volu == None:
            texto = "ERROR: no hay paciente cargados !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            return
        self.Setup_Escena()
        param = slicer.util.getNode("Param_data")
        param.SetParameter("Fiduciarios", self.Combo2.currentText)
        self.ledt2.setText(self.Combo2.currentText)
        print("Cambia la geometria: ", self.Combo2.currentText)
        

    def Obtiene_9_Fiduciarios_f(self):
        print("Vino a marcacion de 9 fiduciarios")
        nodo_volu = self.utiles.obtiene_nodo_de_widget("Red")
        print("El volumen con que se trabaja es = ", nodo_volu.GetName())
        print("El origen del volumen es =", nodo_volu.GetOrigin())
        self.utiles.modifica_origen_de_volumen(nodo_volu, [100,100,-100])
        self.utiles.centra_nodo_de_widget("Red")
                
        nodo_fidu = self.gest.Inicializa_nodo("f")
        dnodo_fidu = nodo_fidu.GetDisplayNode()
        dnodo_fidu.SetGlyphType(1)
        dnodo_fidu.SetSelectedColor(0.0, 1.0, 0.0)
        dnodo_fidu.SetActiveColor(1.0, 0.0, 0.0)
        transformada = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        #transformada = self.utiles.Genera_Nodo("vtkMRMLLinearTransformNode", "Transformada_Correctora_del_Volumen")
        nodo_volu.SetAndObserveTransformNodeID(transformada.GetID())
        nodo_fidu.SetAndObserveTransformNodeID(transformada.GetID())
        
        param = slicer.util.getNode("Param_data")
        param.SetParameter("Nombre_del_Paciente", nodo_volu.GetName())
        
        self.mixObservador_1 = slicer.util.VTKObservationMixin()
        self.mixObservador_1.addObserver(nodo_fidu, vtk.vtkCommand.UserEvent, self.calculos_para_registracion)
        
        self.gest.Marcacion_Fiduciarios("f", 9)
        
        
    def calculos_para_registracion(self, caller, event):  # funcion principal MAIN del procesamiento de fiduciarios
        print("vino a callback main desde :", type(caller), event)
        self.mixObservador_1.removeObservers()      
        param = slicer.util.getNode("Param_data")
        #
        #     procedimiento de REGISTRACION
        #
        nodo_fidu = slicer.util.getNode("f")
        nodo_fidu.SetDisplayVisibility(False)
        fiduciarios_TAC = self.gest.Lectura_Fiduciarios(nodo_fidu)
        geometria = param.GetParameter("Marco") + "_" + param.GetParameter("Fiduciarios")
        matriz_RB = self.maqui.Ecuaciones_Russell_Brown(fiduciarios_TAC, geometria)
        if matriz_RB == None:
            texto = "ATENCION: hay un error en el Marco y/o Fiduciarios !!!"
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
            self.Bton3.setStyleSheet(self.rojito) # rojito
            return        

        array_M_RB = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        fiduciarios_3D = self.maqui.Multiplica_lista_de_puntos(fiduciarios_TAC, matriz_RB)
        
        matriz_4x4  = self.maqui.Analisis_por_ICP(fiduciarios_TAC, fiduciarios_3D)
        array_M_3D = slicer.util.arrayFromVTKMatrix(matriz_RB).tolist()
        
        transformada = vtk.vtkTransform()
        transformada.SetMatrix(matriz_4x4)
        nodo_transfo = slicer.util.getNode("Transformada_Correctora_del_Volumen")
        nodo_transfo.SetAndObserveTransformToParent(transformada)

        self.utiles.centra_nodo_de_widget("Red")
        slicer.app.layoutManager().setLayout(3)  # 4 up

        if param.GetParameter("Marco") == "LEKSELL":
            Target = np.array([100.0, 100.0, 60.0])
            Entry = np.array([160.0, 160.0, 130.0])
        else:
            Target = np.array([0.0, 0.0, 60.0])
            Entry = np.array([60.0, 60.0, 130.0])
        
        self.inicia_path(Target, Entry)    
        
        param.SetParameter("Fiduciarios_TAC", str(self.utiles.redondea_lista_de_puntos(fiduciarios_TAC, 2)))
        param.SetParameter("Array_Matrix_RB", str(array_M_RB))
        param.SetParameter("Fiduciarios_3D", str(self.utiles.redondea_lista_de_puntos(fiduciarios_3D, 2)))
        param.SetParameter("Array_Matrix_3D", str(array_M_3D))
        param.SetParameter("Target", "X= "+str(Target[0])+ ", Y= " + str(Target[1]) +", Z= "+ str(Target[2]))
        param.SetParameter("Entry" , "X= "+str(Entry[0])+ ", Y= " + str(Entry[1]) +", Z= "+ str(Entry[2]))
        param.SetParameter("Transformada_Position", str(self.utiles.redondea(transformada.GetPosition(), 2)))
        param.SetParameter("Transformada_Orientation", str(self.utiles.redondea(transformada.GetOrientation(), 2)))
        param.SetParameter("Registered_flag", "True")
        self.actualiza_widget(param, None)       

        self.Bton3.setStyleSheet(self.verdecito) # verde


    def inicia_path(self, Target, Entry):        
        nodo_path = self.utiles.genera_linea(Target, Entry)
        # inicia observador
        self.mixObservador_5 = slicer.util.VTKObservationMixin()
        self.mixObservador_5.addObserver(nodo_path, nodo_path.PointEndInteractionEvent, self.funcion_mueve_path)
        self.funcion_mueve_path(nodo_path, None)               
        
    
    def funcion_mueve_path(self, nodo, ev):
        print("vino a mueve path")
        p_RAS = slicer.util.arrayFromMarkupsControlPoints(nodo, True)
        param = slicer.util.getNode("Param_data")
        
        self.utiles.ubicar_la_punta_en_RPN(p_RAS[self.E_T_flag])
        
        Target = self.utiles.redondea((p_RAS[0]), 1)
        Entry = self.utiles.redondea((p_RAS[1]), 1)
        
        Alfa, Beta = self.utiles.calcula_angulos_con_vtk(Target, Entry)
        print("Alfa, Beta con vtk =", Alfa, Beta)
        Alfa, Beta = self.utiles.calcula_angulos_simple(Target, Entry)
        print("Alfa, Beta con formula simple =", Alfa, Beta)
         
        if (Entry[0]>=0) != (Target[0]>=0):   #(a>0) == (b>0)   #### ojo con leksell
            texto = "ATENCION: el PATH atraviesa la línea media !  "
            slicer.util.warningDisplay(texto, windowTitle="Error", parent=None, standardButtons=None)
        
        if Entry[0] >= 0:
            param.SetParameter("Target_Izq_Der_flag", str(True))
        else:
            param.SetParameter("Target_Izq_Der_flag", str(False))

        param.SetParameter("Target", "X= "+str(Target[0])+ ", Y= " + str(Target[1]) +", Z= "+ str(Target[2]))
        param.SetParameter("Entry" , "X= "+str(Entry[0])+ ", Y= " + str(Entry[1]) +", Z= "+ str(Entry[2]))
        largo_path = nodo.GetLineLengthWorld()
        param.SetParameter("Path_length", str(round(largo_path, 2)) +"  mm.")
        param.SetParameter("Target_Angulo_Alfa", str(round(Alfa, 2)) + "  grados")
        param.SetParameter("Target_Angulo_Beta", str(round(Beta, 2)) + "  grados")

        self.actualiza_widget(param, None)
    

    def limpia_widget(self):
        #self.ledt1.setText("")
        #self.ledt2.setText("")
        self.ledt3.setText("")
        self.ledt4.setText("")
        self.ledt5.setText("")
        #self.ledt6.setText("")
        #self.ledt7.setText("")    
        pass


    def actualiza_widget(self, param, event):
        print("vino al callback actualiza widget !!!!!!!!!!!")
        self.limpia_widget()
        param = slicer.util.getNode("Param_data")
        
        self.ledt1.setText(param.GetParameter("Marco"))
        self.ledt2.setText(param.GetParameter("Fiduciarios"))
        self.ledt3.setText(param.GetParameter("Target"))
        self.ledt4.setText(param.GetParameter("Entry"))
        self.ledt5.setText(param.GetParameter("Path_length"))
        #self.ledt6.setText(param.GetParameter("Target_Angulo_Alfa"))
        #self.ledt7.setText(param.GetParameter("Target_Angulo_Beta"))    
                
        #if self.E_T_flag == 0:
        #    self.utiles.impri_layout_2D("Red", "Target", None)
        #    self.utiles.impri_layout_2D("Green", "Target", None)
        #    self.utiles.impri_layout_2D("Yellow", "Target", None)
        #else:
        #    self.utiles.impri_layout_2D("Red", "Entry", None)
        #    self.utiles.impri_layout_2D("Green", "Entry", None)
        #    self.utiles.impri_layout_2D("Yellow", "Entry", None)
            

    def guarda(self):
        print("vino a save")
        # Create a new directory where the scene will be saved into
        ref_time = time.strftime("%Y%m%d-%H%M%S")
        sceneSaveDirectory = self.moduloPath + "/Archivo/Escena_" + ref_time
        if not os.access(sceneSaveDirectory, os.F_OK):
            os.makedirs(sceneSaveDirectory)
        # Save the scene
        if slicer.app.applicationLogic().SaveSceneToSlicerDataBundleDirectory(sceneSaveDirectory, None):
            logging.info("Scene saved to: {0}".format(sceneSaveDirectory))
        else:
            logging.error("Scene saving failed")
        
        # Save los parametros
        param = slicer.util.getNode("Param_data")
        param.SetParameter(" Referencia_tiempo", ref_time)
        dictio = {}
        for item in param.GetParameterNames():
            dictio[item] = param.GetParameter(item)
        import json
        #json.dump(dictio, sceneSaveDirectory + "/parametros.json")   
        js = json.dumps(dictio)
        # Open new json file if not exist it will create
        fp = open(sceneSaveDirectory + "/Parametros_" + ref_time + ".json", 'a')
        # write to json file
        fp.write(js)
        # close the connection
        fp.close()

 