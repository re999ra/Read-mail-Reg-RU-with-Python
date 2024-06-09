import imaplib
import email
import time
from email.header import decode_header

# Установите учетные данные электронной почты
username = 'Имя'  # введите ваше имя пользователя
password = 'Пароль'  # введите ваш пароль

# Установите соединение с сервером IMAP
imap_server = 'mail.hosting.reg.ru'
imap_port = 993

# Подключитесь к серверу IMAP
mail = imaplib.IMAP4_SSL(imap_server, imap_port)
mail.login(username, password)
print("Успешно авторизован на IMAP сервере")

# Получите список всех папок в почте
status, folders = mail.list()
print("Папки:")
for folder in folders:
    print(folder.decode('utf-8'))

# Выбираем почтовый ящик "Входящие"
mail.select('INBOX', readonly=True)  # Выбираем почтовый ящик
print("Выбран почтовый ящик: Входящие")

# Выполните команду SEARCH в состоянии SELECTED
status, response = mail.search(None, 'ALL')
print("Результат поиска:", response)

# Создайте список сообщений в папке
messages = []
for num in range(1, len(response[0].split()) + 1):
    status, msg = mail.fetch(str(num), '(RFC822)')
    raw_message = msg[0][1]
    message = email.message_from_bytes(raw_message)
    messages.append(message)

# Вывод сообщений в папке
for message in messages:
    subject = decode_header(message['Subject'])[0][0]
    if isinstance(subject, bytes):
        subject = subject.decode('utf-8')
    from_addr = message['From']
    print(f"Тема: {subject}")
    print(f"От: {from_addr}")
    if message.is_multipart():
        for part in message.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get('Content-Disposition'))
            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                body = part.get_payload()
                print(f"Текст: {body}")
    else:
        body = message.get_payload()
        print(f"Текст: {body}")
    print()

# Запускаем безконечную проверку новых письмем, каждые 60 секунд
while True:
    mail.select('INBOX', readonly=True)  # Выбераем почтовый ящик
    print("Выбран почтовый ящик: Входящие")
    status, response = mail.search(None, 'UNSEEN')
    unread_msgs = response[0].split()
    print(f"Непрочитанные сообщения в папке Входящие: {unread_msgs}")

    # Создайте список новых сообщений в папке
    new_messages = []
    for num in unread_msgs:
        status, msg = mail.fetch(num, '(RFC822)')
        raw_message = msg[0][1]
        message = email.message_from_bytes(raw_message)
        new_messages.append(message)

    # Вывод новых сообщений в папке
    for message in new_messages:
        subject = decode_header(message['Subject'])[0][0]
        if isinstance(subject, bytes):
            subject = subject.decode('utf-8')
        from_addr = message['From']
        print(f"Тема: {subject}")
        print(f"От: {from_addr}")
        if message.is_multipart():
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get('Content-Disposition'))
                if content_type == 'text/plain' and 'attachment' not in content_disposition:
                    body = part.get_payload()
                    print(f"Текст: {body}")
        else:
            body = message.get_payload()
            print(f"Текст: {body}")
        print()
    time.sleep(60)

# Close the IMAP connection
mail.expunge()
mail.close()
mail.logout()
