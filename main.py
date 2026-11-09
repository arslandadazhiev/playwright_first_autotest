import os
from playwright.sync_api import sync_playwright

def test_playwright():
    with sync_playwright() as p:
        # Запускаем браузер в видимом режиме с небольшой задержкой, чтобы успевать следить за действиями
        browser = p.webkit.launch(headless=False, slow_mo=500)
        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )

        page = context.new_page()
        page.goto('https://demoqa.com/automation-practice-form')

        # 1. Заполнение текстовых полей (Имя, Фамилия, Email, Телефон)
        page.fill('#firstName', 'Иван')
        page.fill('#lastName', 'Иванов')
        page.fill('#userEmail', 'ivanov@example.com')
        page.fill('#userNumber', '9991112233')  # Ровно 10 цифр для валидации

        # 2. Выбор пола (Gender) через клик по тексту/лейблу (так как нативные радиокнопки скрыты стилями)
        page.click('label[for="gender-radio-1"]') # Male

        # 3. Выбор даты рождения (простой способ — через очистку и ввод текста)
        page.click('#dateOfBirthInput')
        # Выделяем весь текст в поле даты и заменяем его
        page.keyboard.press('Control+A')
        page.keyboard.type('15 May 1995')
        page.keyboard.press('Enter')

        # 4. Выбор предметов (Subjects) — автокомплит
        page.fill('#subjectsInput', 'Maths')
        page.keyboard.press('Enter')

        # 5. Выбор хобби (Hobbies) — кликаем по лейблу чекбокса
        page.click('label[for="hobbies-checkbox-1"]') # Sports
        page.click('label[for="hobbies-checkbox-3"]') # Music

        # 6. Загрузка файла (создаем временный текстовый файл для теста)
        file_path = os.path.abspath("test_file.txt")
        with open(file_path, "w") as f:
            f.write("Тестовый файл для Playwright")
        page.set_input_files('#uploadPicture', file_path)

        # 7. Заполнение адреса
        page.fill('#currentAddress', 'г. Москва, ул. Ленина, д. 1')

        # 8. Выбор штата и города (выпадающие списки react-select)
        # Скроллим вниз, чтобы элементы были в зоне видимости и реклама не мешала клику
        page.locator('#submit').scroll_into_view_if_needed()

        page.click('#state')
        page.click('div[id^="react-select-3-option"]:has-text("NCR")') # Выбираем NCR

        page.click('#city')
        page.click('div[id^="react-select-4-option"]:has-text("Delhi")') # Выбираем Delhi

        # 9. Отправка формы
        page.click('#submit')

        # 10. Проверка успешной отправки (ждем появления модального окна)
        modal_title = page.locator('#example-modal-sizes-title-lg')
        if modal_title.is_visible(timeout=5000):
            print("Тест пройден! Форма успешно отправлена.")
        else:
            print("Ошибка: модальное окно подтверждения не появилось.")

        # Закрываем браузер и удаляем временный файл
        browser.close()
        if os.path.exists(file_path):
            os.remove(file_path)

if __name__ == '__main__':
    test_playwright()
