
"""
Основное окно приложения.
Вариант 4: Окно с изображением.
"""

import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QLabel,
    QFileDialog,
    QMessageBox
)

from PyQt6.QtCore import Qt

from image_utils import load_image, display_image


class MainWindow(QMainWindow):
    """Главное окно приложения."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Просмотр изображения")
        self.resize(800, 600)

        self.current_image = None

        self.init_ui()

    def init_ui(self):
        """Создание пользовательского интерфейса."""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # Область отображения изображения
        self.image_label = QLabel("Загрузите изображение")
        self.image_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.image_label.setMinimumSize(400, 300)

        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px dashed gray;
                background-color: #f0f0f0;
                color: #333333;
                font-size: 16px;
            }
        """)

        # Кнопка загрузки
        self.load_button = QPushButton(
            "Загрузить изображение"
        )
        self.load_button.setMinimumHeight(40)

        self.load_button.clicked.connect(
            self.on_button_click
        )

        layout.addWidget(self.image_label, stretch=1)
        layout.addWidget(self.load_button)

        central_widget.setLayout(layout)

    def on_button_click(self):
        """Обработчик нажатия кнопки."""

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите изображение",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.tif *.tiff)"
        )

        if not file_path:
            return

        image = load_image(file_path)

        if image is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось загрузить изображение."
            )
            return

        self.current_image = image

        if not display_image(
            self.image_label,
            self.current_image
        ):
            QMessageBox.warning(
                self,
                "Ошибка",
                "Не удалось отобразить изображение."
            )

    def resizeEvent(self, event):
        """Обновление изображения при изменении размера окна."""

        super().resizeEvent(event)

        if self.current_image is not None:
            display_image(
                self.image_label,
                self.current_image
            )


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
