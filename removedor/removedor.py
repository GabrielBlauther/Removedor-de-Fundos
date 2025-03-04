import sys
import os
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from rembg import remove
from PIL import Image

class RemoveFundoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Removedor de Fundo")
        self.setGeometry(100, 100, 400, 300)
        self.setAcceptDrops(True)

        self.label = QLabel("Arraste e solte uma imagem aqui", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
    
    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            image_path = urls[0].toLocalFile()
            self.process_image(image_path)
    
    def process_image(self, image_path):
        try:
            if not os.path.exists(image_path):
                self.label.setText("Erro: Arquivo não encontrado.")
                return

            input_image = Image.open(image_path)
            if input_image is None:
                self.label.setText("Erro: Falha ao carregar a imagem.")
                return

            output_image = remove(input_image)
            if output_image is None:
                self.label.setText("Erro: rembg.remove() retornou None.")
                return

            output_path = os.path.splitext(image_path)[0] + "_sem_fundo.png"
            output_image.save(output_path)
            
            pixmap = QPixmap(output_path)
            if pixmap.isNull():
                self.label.setText("Erro: Não foi possível carregar a imagem processada.")
                return

            self.label.setPixmap(pixmap.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
            self.label.setText("Arraste e solte outra imagem para processar")
        except Exception as e:
            self.label.setText(f"Erro: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RemoveFundoApp()
    window.show()
    sys.exit(app.exec())
