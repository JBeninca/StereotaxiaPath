from __main__ import qt, ctk, slicer, vtk

def setupUI(self):
    print("vino a setupUI")
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
    self.Bton2= qt.QPushButton("abre Archivo Dicom")
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
    #self.Combo1.addItems(['LEKSELL'])
    self.Combo2 = qt.QComboBox()
    self.Combo2.setEditable(True)
    self.Combo2.lineEdit().setAlignment(qt.Qt.AlignCenter)
    #self.Combo2.addItems(['UPWARD'])
    
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
    self.Bton5.clicked.connect(lambda: self.selectora_botones("Target/Entry"))
    self.Bton9.clicked.connect(lambda: self.selectora_botones("Guarda"))
    self.Bton7.clicked.connect(lambda: self.selectora_botones("MPR"))
    self.Bton8.clicked.connect(lambda: self.selectora_botones("Tabulado"))
    self.Bton20.clicked.connect(lambda: self.selectora_botones("Prueba1"))
    self.Bton21.clicked.connect(lambda: self.selectora_botones("Prueba2"))
    
    self.Combo1.currentTextChanged.connect(self.on_combo1_changed)
    self.Combo2.currentTextChanged.connect(self.on_combo2_changed)

