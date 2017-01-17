# endem-su-test-task

### Установка

```bash
virtualenv env
source env/bin/activate
pip install -r requirements_dev.txt
```

### Тестирование

В составе библиотеки 21 тест формата `pytest`

### Использование

Параметры провайдеров задаются в файле `providers.yml`.
Сейчас есть настройки для Gmail, Mail.ru, Yandex.

Для управления логированием нужно менять конфигурацию логера `emaillib`

#### CLI интерфейс

Параметры можно передавать в командной строке или вводить интерактивно.

Пример:
```bash
python endem/cli.py --provider gmail --email user@gmail.com --password secret --to user@gmail.com --subject 'Test subject' --message 'Hello, world!'
```

#### Программно

Нужно указывать код провайдера из конфига при создании экземпляра

```python
from endem import EmailSender


EmailSender(provider='gmail').send(
    from_email, from_user_password, to, subject, message_text,
)
```
