import telebot

API_KEY = '***' # API бота
TEXT_START = "Привет! Я бот который помогу тебе записать твои задачи"
TEXT_HELP = """Список доступных команд:
* /add - Добавить задачу на дату
* /show - Напечать все задачи на заданную дату
* /help - Напечатать help
"""

todos = dict()
bot = telebot.TeleBot(API_KEY)

@bot.message_handler(commands=['start'])
def start(message):
  bot.send_message(message.chat.id, TEXT_START)
  help(message)

@bot.message_handler(commands=['help'])
def help(message):
  bot.send_message(message.chat.id, TEXT_HELP)

@bot.message_handler(commands=['show'])
def show(message):
  keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)

  for date in todos:
    heart_button = telebot.types.KeyboardButton(f"{date}")
    keyboard.row(heart_button)

  bot.send_message(message.chat.id, "Выберите дату:", reply_markup=keyboard)
  bot.register_next_step_handler(message, output_on_display)

def output_on_display(message):
  date = message.text
  if date in todos:
    tasks = ''
    for task in todos[date]:
      tasks += f'[ ] {task}\n'
  else:
    tasks = 'Такой даты нет'
  bot.send_message(message.chat.id, tasks)

@bot.message_handler(commands=['add'])
def add(message):
  bot.send_message(message.chat.id, "Введите дату:")
  bot.register_next_step_handler(message, add_date)

def add_date(message):
  date = message.text
  bot.send_message(message.chat.id, "Введите задачу:")
  bot.register_next_step_handler(message, add_task, date)

def add_task(message, date):
  task = message.text  
  add_todo(date, task)
  text = f'Задача "{task}" добавлена на дату "{date}"'
  bot.send_message(message.chat.id, text)

def add_todo(date, task):
  date = date.lower()
  if todos.get(date) is not None:
    todos[date].append(task)
  else:
    todos[date] = [task]

bot.enable_save_next_step_handlers(delay = 2)
bot.load_next_step_handlers()
bot.infinity_polling()