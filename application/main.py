from twitchio.ext import commands
from db_utils import save_message, update_cleaned_comments
from process_message import preprocess_text, is_toxic
from config import TOKEN, INITIAL_CHANNELS

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TOKEN,
            prefix='?',
            initial_channels=INITIAL_CHANNELS
        )

    async def event_ready(self):
        print(f'Бот подключен как | {self.nick}')
        print(f'ID пользователя | {self.user_id}')

    async def event_message(self, message):
        print(f'[{message.channel.name}] {message.author.name}: {message.content}')

        # Сохраняем сообщение в таблицу row_comments
        save_message(message)

        # Обрабатываем команды
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, ctx: commands.Context):
        await ctx.send(f'Привет, {ctx.author.name}!')

# Запуск бота
if __name__ == "__main__":
    bot = Bot()
    bot.run()