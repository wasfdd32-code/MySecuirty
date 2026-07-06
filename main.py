import discord
from discord.ext import commands

# إعدادات الصلاحيات
intents = discord.Intents.default()
intents.members = True   # ضروري للتعامل مع الأعضاء (الباند)
intents.guilds = True    # ضروري لمراقبة القنوات والرتب

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ البوت يعمل كـ {bot.user}')

@bot.event
async def on_guild_role_delete(role):
    # مراقبة حذف الرتب
    async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
        user = entry.user
        # استثناء البوت نفسه ومالك السيرفر
        if not user.bot and user.id != role.guild.owner_id:
            # التحقق: إذا كانت رتبة المخرب أقل من رتبة البوت
            if role.guild.get_member(user.id).top_role < role.guild.me.top_role:
                await user.ban(reason="محاولة تخريب: حذف رتبة")
                print(f"🚫 تم حظر {user.name} لمحاولته حذف رتبة.")

@bot.event
async def on_guild_channel_delete(channel):
    # مراقبة حذف القنوات
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        user = entry.user
        if not user.bot and user.id != channel.guild.owner_id:
            if channel.guild.get_member(user.id).top_role < channel.guild.me.top_role:
                await user.ban(reason="محاولة تخريب: حذف قناة")
                print(f"🚫 تم حظر {user.name} لمحاولته حذف قناة.")

# ضع التوكن هنا أو استخدم متغيرات البيئة
bot.run('YOUR_SECURITY_BOT_TOKEN')
