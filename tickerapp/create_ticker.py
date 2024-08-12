import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tempfile


def create_ticker(text):
    # Параметры видео
   # breakpoint()
    video_width = 100
    video_height = 100
    fps = 30
    duration = 3  # Длительность видео в секундах
    #text = "Хочу на стажировку :)"  # Текст для отображения

    temp_file = tempfile.NamedTemporaryFile(suffix='.avi', delete=False)
    video_path = temp_file.name
    temp_file.close()


    # Создание видео
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(video_path, fourcc, fps, (video_width, video_height))

    # Загрузка шрифта
    font_size = 80
    font = ImageFont.truetype('running_str/myapp/fonts/arial.ttf', size=font_size)

    # Рассчитываем длину текста в пикселях
    (left, top, right, bottom) = font.getbbox(text)
    text_width = right-left
    text_height = top-bottom

    # Начальная позиция текста
    x = video_width

    for frame_num in range(fps * duration):
        # Создаем пустое изображение
        image = Image.new("RGB", (video_width, video_height), (255,192,203))
        draw = ImageDraw.Draw(image)

        # Рисуем текст
        draw.text((int(x), int(video_height+text_height)/2), text, font=font, fill=(255, 255, 255))

        # Конвертируем изображение в массив numpy
        frame = np.array(image)

        # Записываем кадр в видео
        video.write(cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        # Обновляем позицию текста
        x -= text_width/(duration*fps)*1.5
        if x < -text_width:
            x = video_width

    # Освобождаем ресурсы
    video.release()
    
    return video_path