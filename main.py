import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_guild_role_delete(role):
    async for entry in role.guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete):
        user = entry.user
        # لا يطرد البوت نفسه ولا يطرد الأونر
        if not user.bot and user.id != role.guild.owner_id:
            # إذا كان المخرب رتبته أقل من رتبة البوت
            if role.guild.get_member(user.id).top_role < role.guild.me.top_role:
                await user.ban(reason="محاولة حذف رتبة - نظام الحماية")
                await role.guild.system_channel.send(f"🚫 | تم حظر {user.name} لمحاولته حذف رتبة.")

@bot.event
async def on_guild_channel_delete(channel):
    async for entry in channel.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete):
        user = entry.user
        if not user.bot and user.id != channel.guild.owner_id:
            if channel.guild.get_member(user.id).top_role < channel.guild.me.top_role:
                await user.ban(reason="محاولة حذف قناة - نظام الحماية")
                await channel.guild.system_channel.send(f"🚫 | تم حظر {user.name} لمحاولته حذف قناة.")

bot.run('TOKEN')