ADMIN_LEXICON: dict = {
    "/start": "Приветствую, выберите опцию",
    "/help": "Информация для админа",
    "Input nickname": "Введите ссылку на пользователя в формате https://t.me/nickname, \nили никнейм в формате @nickname с символом '@' в начале",
    "Successful addition of game host: ": "Успешное добавление ведущего: ",
    "Incorrect input user": "Некорректный ввод пользователя. Введите ссылку на пользователя в формате https://t.me/nickname или никнейм в формате @nickname",
    "Are you sure delete all data?!": "Вы уверены, что хотите удалить все данные?!",
    "All data was deleted!": "Все данные были удалены!",
    "Hosts not set": "Ведущие комнат не назначены",
    "Host nicknames. Press for action.": "Никнеймы ведущих комнаты. Нажмите для выбора.",
    "Select option for room host: ": "Выберите опцию для ведущего комнаты: ",
    "Are you sure delete: ": "Вы уверены, что хотите удалить: ",
    "Can not deleted: ": "Не удалось удалить: ",
    "successful deleted!": "успешно удален!",
    "Cancel operation": "Отменить операцию",
}


ADMIN_BOTTOMS: dict = {
    "Add host": "Добавить ведущего",
    "Delete all data!": "❌ Удалить все данные!",
    "Show hosts": "📋 Показать ведущих",
    "Create room for game": "🎮 Создать комнату для игры",
    "Confirm add host": "✔ Подтвердить добавление ведущего",
    "Cancel": "Отмена",
    "Cancel operation": "Отменить операцию",
    "Attention! Cancel ALL data!": "❌ Внимание! Удалить ВСЕ данные!",
    "Host:": "🧑 Ведущий:",
    "Show statistic": "📋 Показать статистику",
    "Delete host": "❌ Удалить ведущего",
    "Confirm delete": "Подтвердить удаление",
}

HOST_LEXICON: dict = {
    "/start": "Привет! \n Реакция на команду 'start' от пользователя без регистрации\n",
    "/help": "Информация о боте",
    "Start for registered": "Запуск для зарегистрированного пользователя, id: ",
    "Game data cleared": "Данные игры очищены",
    "Message state of play": "Вы находитесь в состоянии игры. Завершите игру, чтобы перейти в главное меню.",
    "Waiting for a room name:": "Ожидание ввода названия комнаты:",
    "Can't start without Room Name or pass": "Невозможно начать без названия комнаты или пароля",
    "Message waiting players": "Ожидание регистрации игроков. Регистрация доступна до начала игры.",
    "Registered players": "Ожидайте зарегистрированных игроков. Не нажимайте 'start', пока все игроки не зарегистрируются.",
    "Unable to start": "Невозможно начать игру с менее чем 3 игроками",
    "Cancel": "Отмена",
    "Click to exit": "Нажмите для выхода",
    "Room name: ": "Название комнаты: ",
    "Password: ": "Пароль: ",
    "States canceled": "Состояния сброшены",
    "All data canceled": "Все данные очищены",
}

HOST_BOTTOMS: dict = {
    "Game menu: ": "Меню игры: ",
    "Start registration in game": "🎮 Начать регистрацию в игре",
    "Change room name": "⚙ Изменить название комнаты",
    "Change password": "⚙ Изменить пароль",
    "Game setting": "⚙ Настройки игры",
    "Press for update user lists": "📋 Нажмите для обновления списка пользователей",
    "Start game": "🎮 Начать игру",
    "Finish game": "❌ Завершить игру",
    "Exit to the main menu": "Выйти в главное меню",
    "Cancel state": "Сбросить состояние",
    "Cancel data": "Удалить все данные",
    "Player: ": "🧑 Игрок: ",
}

USER_LEXICON: dict = {
    "/start": "Привет! \n Выберите свой никнейм. Если не выбрать никнейм, будет использован ваш никнейм в Telegram по умолчанию.\n"
              "Зарегистрируйтесь в активной комнате и ждите, пока ведущий не начнет игру.",
    "Can not enter without QR code": "Невозможно войти без QR-кода",
    "/help": "Информация о боте",
    "active rooms": "Активные комнаты. Нажмите для входа.",
    "no active rooms": "В данный момент нет активных комнат",
    "Input password for room: ": "Введите пароль для комнаты: ",
    "Input password: ": "Введите пароль: ",
    "Password entry error": "Ошибка ввода пароля. Попробуйте еще раз или нажмите отмену",
    "Cancel": "Отмена",
    "Cancel operation": "Отменить операцию",
    "Confirm": "Подтвердить",
    "Successful registered in room: ": "Успешная регистрация в комнате: ",
    "Wait for the game to start": "Ожидайте начала игры",
    "Toast timer message": "Ваш черед произносить тост",
    "Your minute is over": "Ваша минута истекла",
    "Something wrong in select room": "Что-то не так с выбором комнаты",
    "Your QR code number: ": "Ваш номер QR-кода: ",
    "Input your nickname": "Введите ваш никнейм",
    "Your current nickname: ": "Ваш текущий никнейм: ",
    "All settings reset": "Все настройки сброшены",
}

USER_BOTTOMS: dict = {
    "Show active rooms": "Показать активные комнаты",
    "Set nickname": "Выбрать никнейм",
    "Change role": "Изменить роль",
    "Show your role": "Показать вашу роль",
    "Click to exit": "Нажмите для выхода",
}

USER_TIMER: dict = {"0": "0️⃣", "1": "1️⃣", "2": "2️⃣", "3": "3️⃣", "4": "4️⃣",
                    "5": "5️⃣", "6": "6️⃣", "7": "7️⃣", "8": "8️⃣", "9": "9️⃣",
                    }

LEXICON_COMMANDS: dict[str: str] = {
    '/start': 'Init connect with bot',
    '/help': 'Information about bot',
    # '/command_3': 'command_3 desription',
    # '/command_4': 'command_4 desription'
}

# LEXICON: dict[str, str] = {
#     '/start': 'Hello! \n Reaction on command start from user without registration\n',
#     '/help': 'Game info',
#     '/start_admin': 'Hello for Admin!',
#     '/help_admin': 'Help info for admin',
#
# }

