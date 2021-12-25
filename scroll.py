self.textEdit = QTextEdit()
self.vbox.addWidget(self.textEdit)

 def metaData(self):
        # pip install hachoir

        input_file = self.imagePath
        exe = "hachoir-metadata"
        self.process = subprocess.Popen([exe, input_file], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        for output in self.process.stdout:
            a = str(output.strip())
            self.textEdit.append(a)
