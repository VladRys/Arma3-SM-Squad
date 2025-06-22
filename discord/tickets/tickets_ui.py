import disnake
from disnake.ui import View, Button, Select, TextInput, Modal
from disnake import ButtonStyle, Interaction

from core.config import EMBED_COLOR, END_OF_TICKET_CHANNEL_ID

class TicketView(View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot
        

    @disnake.ui.button(label=" Arma 3",emoji="<:customemoji:1386364977874468874>", style=ButtonStyle.gray)
    async def create_ticket(self, button: Button, interaction: Interaction):
        modal = TicketModalArma3(self.bot)
        await interaction.response.send_modal(modal)

class TicketModalArma3(Modal):
    def __init__(self, bot):
        components = [
            TextInput(label="Ваш желаемый позывной:", placeholder=None, required=True, custom_id="callsign"),
            TextInput(label="Ваш возраст:", placeholder=None, required=False, custom_id="age"),
            TextInput(label="Кол-во часов?", placeholder=None, required=True, custom_id="hours"),
            TextInput(label="Имеется ли опыт в твт/тве?", placeholder="Если да, то на каких проектах/серверах", required=True, custom_id="experience"),
            TextInput(label="На сколько оцениваете свою адекватность?", placeholder="от 0 до 10", required=True, custom_id="adequacy"),
        ]
        super().__init__(title="Подать заявку", components=components)
        self.bot = bot

    async def callback(self, interaction: Interaction):

        

        nickname = interaction.author.display_name

        callsign = interaction.text_values.get("callsign", "—")
        age = interaction.text_values.get("age", "—")
        hours = interaction.text_values.get("hours", "—")
        experience = interaction.text_values.get("experience", "—")
        adequacy = interaction.text_values.get("adequacy", "—")

        embed_text = (
            f"**Дискорд:** {nickname}\n"
            f"**Позывной:** {callsign}\n"
            f"**Возраст:** {age}\n"
            f"**Кол-во часов:** {hours}\n"
            f"**Опыт в твт/тве:** {experience}\n"
            f"**Адекватность:** {adequacy}/10"
        )
        embed = disnake.Embed(
            title="Заявка на вступление в отряд",
            description=embed_text,
            color=EMBED_COLOR
        )

        await self.bot.get_channel(END_OF_TICKET_CHANNEL_ID).send(
            embed=embed,
            content=f"<@265888314781990914> <@1326943255400808518>",
        )

        await interaction.response.send_message("Ваша заявка успешно создана! Ожидайте ответа от представителей отряда.\n\nПо любым вопросам обращаться к офицерам отряда указанным в сообщении выше.", ephemeral=True)