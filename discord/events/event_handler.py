import disnake
from disnake.ext import commands
from logs.setup_logs import setup_logger

from core.config import TICKET_CHANNEL_ID, TICKET_MESSAGE_ID

from ..tickets.ticket import TicketSystem
from ..tickets.tickets_ui import TicketView

class EventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.ticket = TicketSystem(self.bot) 

        self.l = setup_logger()
        self.l.info("[DISCORD] EventHandler cog loaded successfully.")
    
    @commands.Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(TICKET_CHANNEL_ID)
        try:
            message = await channel.fetch_message(TICKET_MESSAGE_ID)
            await message.edit(view=TicketView(self.bot))
        except disnake.NotFound:
            await self.ticket.send_ticket_view()
        except Exception as e:
            self.l.error(f"[DISCORD] Error while fetching ticket message: {e}")

        self.l.info("[DISCORD] Ticket message sended.")
        


def setup(bot):
    bot.add_cog(EventHandler(bot))