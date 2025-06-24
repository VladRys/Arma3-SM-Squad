import disnake
from disnake.ext import commands
from .tickets_ui import TicketView
from core.config import BOT_CHANNEL_ID, TICKET_CHANNEL_ID, EMBED_COLOR
from logs.setup_logs import setup_logger

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.l = setup_logger()
        self.l.info("[DISCORD] Ticket system initialized successfully.")
        
        self.bot = bot

    async def send_ticket_view(self):
        view = TicketView(self.bot)

        embed = disnake.Embed(
            title="Вступить в отряд",
            description="Чтобы подать заявку на вступление в отряд, выберите нужую игру и нажмите на кнопку ниже. Ваша заявка будет расмотрена в ближайшее время.\n\nПо всем вопросам обращаться к @lazcore или @vxrsdlx8888",
            color=EMBED_COLOR
        )

        await self.bot.get_channel(TICKET_CHANNEL_ID).send(
            embed=embed,
            view=view
        )
        
def setup(bot):
    bot.add_cog(TicketSystem(bot))    
