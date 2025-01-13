from twitchio.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        # Укажите ваш OAuth-токен и каналы
        super().__init__(
            token='oauth:41s4xfxfa11osvpo2p23lgcx8hv8gn',  # Замените на ваш OAuth-токен
            prefix='?',
            initial_channels=['leekbeats', 'stepycdragon', 'wipr']  # Укажите каналы
        )

    async def event_ready(self):
        # Бот успешно подключился к Twitch
        print(f'Бот подключен как | {self.nick}')
        print(f'ID пользователя | {self.user_id}')

    async def event_message(self, message):
        # Выводим сообщения из чата в консоль с указанием канала
        print(f'[{message.channel.name}] {message.author.name}: {message.content}')

        # Обрабатываем команды (если нужно)
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        # Отправляем ответ на команду !hello
        await ctx.send(f'Привет, {ctx.author.name}!')

# Запуск бота
bot = Bot()
bot.run()