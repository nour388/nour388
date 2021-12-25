 def restartLayout(self):
       args = sys.argv[:]  # get shallow copy of running script args
       args.insert(0, sys.executable)  # give it the executable
       os.execv(sys.executable, args)

      
    
    
 self.btn7 = QPushButton("Restart")
        self.btn7.setStyleSheet('background-color: rgb(97, 173, 184)')
        self.btn7.clicked.connect(self.restartLayout)
        self.vbox.addWidget(self.btn7)
