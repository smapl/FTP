# FTP

Файл конфигурации :
  В первой секции ("information about server") в роли ключа записываются хост, имя пользователя и пароль, далее их значения.
  Во второй секции ("file name") в роли ключа записываются имена файлов, в роли значения - полный путь к файлу.
  В трейтьей секции ("server path") в роли ключа записыавюся полный путь файла и его имя, в роли значения 
папка в которую нужно скопировать файл, если в третьей секции не будет указано информации о папки, то файл скопируется в начальную
директорию на сервере, также если директории на сервере, которую вы указали нет, то она будет создана.

