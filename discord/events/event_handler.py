from disnake.ext import commands
from logs.setup_logs import setup_logger

from ..tickets.ticket import TicketSystem

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ticket = TicketSystem(self.bot) 

        self.l = setup_logger()
        self.l.info("[DISCORD] EventHandler cog loaded successfully.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        await self.ticket.send_ticket_view()

        self.l.info("[DISCORD] Ticket message sended.")


def setup(bot):
    bot.add_cog(EventHandler(bot))