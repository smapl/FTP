import ftplib
from json import load
import os
from threading import Thread, RLock


class UploadFile:
    def __init__(self, info_about_server):
        self.info_about_server = info_about_server

    def upload(self, file_name, server_path, start=0, point=0):

        keys = list()
        s_path = list()
        ftp = ftplib.FTP(
            self.info_about_server["host"],
            self.info_about_server["user"],
            self.info_about_server["password"],
        )  # авторизация
        for i in file_name:
            keys.append(i)  # тут клюючи от словаря fileName

        for i in server_path:
            s_path.append(i)

        for i in range(len(server_path)):
            print(server_path[s_path[i]])

        for i in range(start, point):
            for j in range(
                len(server_path)
            ):  # проверка на существование директории на сервере
                if (file_name[keys[i]] + keys[i]) == s_path[
                    j
                ]:  # если данный файл нужно перенести в директорию на сервере
                    try:
                        ftp.cwd(server_path[s_path[j]])

                    except ftplib.error_perm:  # иначе создать директорию и перейти
                        ftp.mkd(server_path[s_path[j]])
                    ftp.cwd(server_path[s_path[j]])
                    os.chdir(file_name[keys[i]])  # переход в директорию на компьютере

                    try:  # проверка файла на существование
                        f = open(keys[i], "rb")
                        print(
                            "{0}.{1} - make dir: {2}".format(
                                i, j, file_name[keys[i]] + keys[i]
                            )
                        )
                        send = ftp.storbinary("STOR " + keys[i], f)
                        ftp.cwd("//")  # переход в изначальную директорию
                        f.close()
                    except FileNotFoundError:
                        print("файла {0} не существует".format(keys[i]))

                elif (file_name[keys[i]] + "/" + keys[i]) not in s_path:
                    os.chdir(file_name[keys[i]])
                    f = open(keys[i], "rb")
                    print(
                        "{0}.{1} - withoot make dir: {2}".format(
                            i, j, file_name[keys[i]] + keys[i]
                        )
                    )
                    send = ftp.storbinary("STOR " + keys[i], f)
                    f.close()
                    ftp.cwd("//")

        ftp.close()  # закрытие ftp соединения


if __name__ == "__main__":
    with open("../data_linux.json") as f:  # считывание данных с файла конифгуации
        data = load(f)

    infoAboutServer = data.get("information about server")
    sourcePath = data.get("source path")
    fileName = data["filename"]
    serverPath = data.get("server path")

    obj_upload = UploadFile(infoAboutServer)

    thread1 = Thread(
        target=obj_upload.upload, args=(fileName, serverPath, 0, len(fileName) // 2)
    )
    thread2 = Thread(
        target=obj_upload.upload,
        args=(fileName, serverPath, len(fileName) // 2, len(fileName)),
    )

    thread1.start()  # старт потока 1
    # thread2.start()      # старт потока 2

    thread1.join()
    # thread2.join()
