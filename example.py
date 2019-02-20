import PySide2.QtWidgets as qw
import PySide2.QtCore as qc
import maya.cmds as cmds
    
class simpleUI(qw.QDialog):
    def __init__(self):
        qw.QDialog.__init__(self)
        self.setWindowTitle('Build_Camera')     
        self.setModal(False)   
        #TECHDEBT: set size window
        self.setMaximumHeight(400)
        self.setMinimumHeight(200) 
        self.setMaximumWidth(400)     
        self.setMinimumWidth(250)
        
        #TECHDEBT: set global layout
        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        
        #TECHDEBT:  set place for camera settings
        camera_frame = qw.QFrame()
        camera_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        picture_frame = qw.QFrame()
        picture_frame.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        
        #TECHDEBT: add places to global layout
        self.layout().addWidget(camera_frame)      
        self.layout().addWidget(picture_frame) 
        camera_frame.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Maximum)
        self.layout().setAlignment(qc.Qt.AlignTop)

        #TECHDEBT: add layouts and items to camera settings
        camera_title = qw.QLabel('Camera Settings.')
        self.camera_button = qw.QPushButton('Create')
        camera_frame.setLayout(qw.QVBoxLayout())
        camera_text_layout = qw.QHBoxLayout()
        camera_frame.layout().setAlignment(qc.Qt.AlignTop)
        camera_frame.layout().addWidget(camera_title)
        camera_frame.layout().addLayout(camera_text_layout)
        camera_frame.layout().addWidget(self.camera_button)
        camera_frame.layout().setSpacing(15)
        self.camera_button.setSizePolicy(qw.QSizePolicy.Maximum, qw.QSizePolicy.Maximum)
               
        #TECHDEBT: add items to text_camera_frame_layout
        camera_title_text = qw.QLabel('Camera name: ')        
        self.camera_new_name = qw.QLineEdit()
        camera_text_layout.addWidget(camera_title_text)
        camera_text_layout.addWidget(self.camera_new_name)
        
        #TECHDEBT: add layouts and items to image settings
        image_title = qw.QLabel('Image Settings.')
        picture_frame.setLayout(qw.QVBoxLayout())
        picture_frame.layout().addWidget(image_title)
        
        #TECHDEBT: actions
        self.connect(self.camera_button, qc.SIGNAL("clicked()"), self.create_camera)
    
    def create_camera(self):
        new_name = self.camera_new_name.text()
        cameraName = cmds.camera(name = new_name + "#")
 #       print(cmds.listCameras())
 #       cmds.rename(cameraName, 'spinning_ball')