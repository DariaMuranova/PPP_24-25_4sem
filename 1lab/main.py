import asyncio

async def send_file(writer, file_name):
    with open(f'./{file_name}', 'rb') as f:
        stroka=f"new {file_name} "
        stroka+=f.read().decode()        
        writer.write(stroka.encode()+b'\0')
        f.close()
        await writer.drain()

async def get_data(reader):
    data = bytearray()
    while True:
        chunk = await reader.read(1024)
        if not chunk:
            break  # Если нет данных, выходим из цикла
        data.extend(chunk)
        if b'\0' in chunk:
            break
    return data

async def main():
    reader, writer = await asyncio.open_connection('localhost', 8000)

    print('''
    str - запускает цикл из процессов
    tim *arg - изменяет время между итерациями (вместо *args указываем число)
    add *args - добавляет процессы в очередь, вместо *args указываем названия процессов
    res *name - возвращает последние результаты выполнения процесса *name
    new *name - позволяет добавить файл под именем *name.
    lst - список доступных файлов
    ''')

    while True:
        message = input("Введите команду: ").strip()
        if message.split()[0]=="new":
            await send_file(writer,message.split()[1])
        else:
            writer.write((message + '\0').encode())
            await writer.drain()  # Ожидаем, пока данные будут отправлены
        
        # Получаем ответ сервера
        data = await get_data(reader)
        print(data.decode())  # Декодируем байты обратно в строку

    # Закрываем соединение
    writer.close()
    await writer.wait_closed()

# Запуск клиента
asyncio.run(main())
