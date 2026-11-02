
"""
Утилиты для работы с изображениями.
"""

import os
import cv2
import numpy as np

from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt


def load_image(file_path):
    """
    Загружает изображение из файла.
    Поддерживает пути с русскими буквами.
    """

    if not os.path.isfile(file_path):
        return None

    try:
        # Читаем файл, включая пути с кириллицей
        file_data = np.fromfile(file_path, dtype=np.uint8)

        # Декодируем изображение
        image = cv2.imdecode(file_data, cv2.IMREAD_COLOR)

        return image

    except (OSError, cv2.error, ValueError):
        return None


def opencv_to_qt_image(cv_image):
    """
    Преобразует изображение OpenCV в QPixmap.
    """

    if cv_image is None:
        return None

    try:
        # Преобразуем BGR в RGB
        rgb_image = cv2.cvtColor(
            cv_image,
            cv2.COLOR_BGR2RGB
        )

        height, width, channels = rgb_image.shape
        bytes_per_line = channels * width

        # Создаём QImage и копируем данные,
        # чтобы изображение не зависело от массива NumPy
        qt_image = QImage(
            rgb_image.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888
        ).copy()

        return QPixmap.fromImage(qt_image)

    except (cv2.error, ValueError):
        return None



def display_image(label, cv_image):
    """
    Отображает изображение в QLabel.
    """

    pixmap = opencv_to_qt_image(cv_image)

    if pixmap is None or pixmap.isNull():
        return False

    # Масштабируем изображение с сохранением пропорций
    scaled_pixmap = pixmap.scaled(
        label.size(),
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    label.setPixmap(scaled_pixmap)

    return True
