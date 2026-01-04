import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# واجهة إدخال النص
class TextModal(discord.ui.Modal, title="تحويل النص"):
    text = discord.ui.TextInput(
        label="حط النص (كل سطر لحاله)",
        style=discord.TextStyle.paragraph,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        # تقسيم النص سطر سطر وإضافة "..."
        lines = self.text.value.split("\n")
        result = "\n".join(
            [f"\"{line.strip()}\"," for line in lines if line.strip()]
        )

        # إرسال النتيجة بدون أي ```
        await interaction.response.send_message(
            result,
            ephemeral=True
        )

# الزر لفتح الواجهة
class OpenModal(discord.ui.View):
    @discord.ui.button(label="✍️ أدخل النص", style=discord.ButtonStyle.primary)
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TextModal())

# عند تشغيل البوت
@bot.event
async def on_ready():
    print("✅ البوت شغال")
    await bot.tree.sync()

# أمر /format
@bot.tree.command(name="format", description="تحويل النص إلى \"text\",")
async def format(interaction: discord.Interaction):
    await interaction.response.send_message(
        "اضغط الزر:",
        view=OpenModal(),
        ephemeral=True
    )

# تشغيل البوت باستخدام متغير البيئة BOT_TOKEN
bot.run(os.getenv("BOT_TOKEN"))
