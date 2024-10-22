import discord
from discord.ext import commands
from discord.ui import View, Button
import random

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=",", intents=intents)

afk_users = {}
snipes = {}
antilink_enabled = True
relationships = {}
user_profiles = {}

# comando de afk


@bot.command()
async def afk(ctx, *, reason="AFK"):
    afk_users[ctx.author.id] = reason
    await ctx.send(f"{ctx.author.mention} está ahora AFK por: {reason}")


@bot.event
async def on_ready():
    print(f'Conectado como {bot.user}')
    await bot.change_presence(activity=discord.Streaming(name="/degollados", url="https://www.twitch.tv/875z"))


@bot.event
async def on_message(message):
    if message.author.id in afk_users:
        del afk_users[message.author.id]
        await message.channel.send(f"{message.author.mention} ya no está AFK.")

    if antilink_enabled and "http" in message.content and not message.author.guild_permissions.administrator:
        await message.delete()
        await message.channel.send(f"{message.author.mention}, no está permitido enviar enlaces.")

    snipes[message.channel.id] = message
    await bot.process_commands(message)

# Comando para activar o desactivar el antilink


@bot.command()
@commands.has_permissions(administrator=True)
async def antilink(ctx, status: str):
    global antilink_enabled
    if status.lower() == "on":
        antilink_enabled = True
        await ctx.send("El sistema AntiLink ha sido activado.")
    elif status.lower() == "off":
        antilink_enabled = False
        await ctx.send("El sistema AntiLink ha sido desactivado.")
    else:
        await ctx.send("Por favor, usa `on` o `off` para activar/desactivar el sistema AntiLink.")

# el comando de snipe creo que aun no esta bien arreglado pero ahi busquen (con alias 's')


@bot.command(aliases=['s'])
async def snipe(ctx):
    if ctx.channel.id in snipes:
        snipe_msg = snipes[ctx.channel.id]
        await ctx.send(f"Mensaje eliminado: {snipe_msg.content}\nAutor: {snipe_msg.author.mention}")
    else:
        await ctx.send("No hay mensajes eliminados recientes.")

# comando de ping del bot o latencia mejor dicho


@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! Latencia: {round(bot.latency * 1000)}ms")

# comando de avatar


@bot.command()
async def avatar(ctx, *, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"Avatar de {member.display_name}", color=discord.Color.blue())
    embed.set_image(url=member.avatar.url)
    await ctx.send(embed=embed)

# comando para ver banner


@bot.command()
async def banner(ctx, *, member: discord.Member = None):
    member = member or ctx.author
    user = await bot.fetch_user(member.id)
    if user.banner:
        embed = discord.Embed(
            title=f"Banner de {member.display_name}", color=discord.Color.green())
        embed.set_image(url=user.banner.url)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"{member.display_name} no tiene banner.")

# commando del bot info ahi tu puedes ponerle tu nick o tu id de usuario


@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(title="Información del bot",
                          color=discord.Color.gold())
    embed.add_field(name="Nombre", value=bot.user.name, inline=True)
    embed.add_field(name="ID", value=bot.user.id, inline=True)
    embed.add_field(name="Desarrollador", value="<@994792326557859890>", inline=True)
    embed.add_field(name="Versión del bot", value="1.0", inline=True)
    embed.add_field(name="Versión de Python", value="3.9", inline=True)
    embed.add_field(name="Servidores", value=len(bot.guilds), inline=True)
    await ctx.send(embed=embed)

# el comanmdo para mostrar la informacion de tu servidor


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    embed = discord.Embed(
        title=f"Información del servidor: {guild.name}", color=discord.Color.purple())
    embed.add_field(name="Miembros", value=guild.member_count, inline=True)
    embed.add_field(name="Dueño", value=guild.owner, inline=True)
    embed.add_field(name="ID del servidor", value=guild.id, inline=True)
    await ctx.send(embed=embed)

# userinfo medio avanzado


@bot.command()
async def userinfo(ctx, *, member: discord.Member = None):
    member = member or ctx.author
    embed = discord.Embed(
        title=f"Información de {member.display_name}", color=discord.Color.orange())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Es un bot",
                    value="Sí" if member.bot else "No", inline=True)
    embed.add_field(name="Cuenta creada", value=member.created_at.strftime(
        "%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Se unió", value=member.joined_at.strftime(
        "%Y-%m-%d %H:%M:%S"), inline=True)
    embed.add_field(name="Posición en el servidor",
                    value=member.top_role, inline=True)

    # Ignorar el rol @everyone
    roles = [role.mention for role in member.roles[1:]]
    embed.add_field(name="Roles", value=f"{len(roles)}: " +
                    ", ".join(roles) if roles else "Ninguno", inline=True)

    status = str(member.status).title() if member.status else "Offline"
    embed.add_field(name="Estado actual", value=status, inline=True)

    activity = member.activity
    if activity and isinstance(activity, discord.Spotify):
        embed.add_field(
            name="Actividad", value=f"Escuchando: {activity.title}\nArtista: {activity.artist}\nÁlbum: {activity.album}", inline=True)
    else:
        embed.add_field(name="Actividad", value="Ninguna", inline=True)

    if member.banner:
        embed.add_field(
            name="Banner", value=f"[Ver Banner]({member.banner.url})", inline=True)

    await ctx.send(embed=embed)

# comando de administracion nomas q aca si tienen q buscar bien como configurarlo por que esta mal estructura y un rol q tiene los mismos perms q otro puede dar ban 


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} ha sido expulsado por {reason}.")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} ha sido baneado por {reason}.")


@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    mute_role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not mute_role:
        mute_role = await ctx.guild.create_role(name="Muted")
        for channel in ctx.guild.channels:
            await channel.set_permissions(mute_role, speak=False, send_messages=False)

    await member.add_roles(mute_role, reason=reason)
    await ctx.send(f"{member.mention} ha sido silenciado por {reason}.")

# comando de purge con el alias de ",p"


@bot.command(aliases=['p'])
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount)
    await ctx.send(f"{amount} mensajes han sido eliminados.", delete_after=5)

# menu de seleccion (no sirve)


class CommandMenu(View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.select(placeholder="Selecciona una categoría", options=[
        discord.SelectOption(label="Comandos Generales",
                             description="Comandos básicos", emoji="📄"),
        discord.SelectOption(label="Comandos de Admin",
                             description="Comandos administrativos", emoji="🛠️"),
        discord.SelectOption(label="Comandos de Diversión",
                             description="Comandos para entretener", emoji="🎉"),
        discord.SelectOption(label="Comandos de Información",
                             description="Comandos de información", emoji="ℹ️"),
    ])
    async def select_callback(self, select, interaction: discord.Interaction):
        if select.values[0] == "Comandos Generales":
            await interaction.response.send_message("`ping`, `avatar`, `serverinfo`, `afk`, `antilink`", ephemeral=True)
        elif select.values[0] == "Comandos de Admin":
            await interaction.response.send_message("`kick`, `ban`, `mute`", ephemeral=True)
        elif select.values[0] == "Comandos de Diversión":
            await interaction.response.send_message("`kiss`, `hug`, `marry`, `profile`", ephemeral=True)
        elif select.values[0] == "Comandos de Información":
            await interaction.response.send_message("`userinfo`, `botinfo`, `serverinfo`", ephemeral=True)

# comando para mostrar el menu (tampoco sirve)


@bot.command()
async def menu(ctx):
    view = CommandMenu()
    await ctx.send("Selecciona una categoría de comandos:", view=view)

# sistema de besos y de eso


@bot.command()
async def kiss(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} le ha dado un beso a {member.mention}! 💋")
    _update_profile(ctx.author, member, 'kisses')


@bot.command()
async def hug(ctx, member: discord.Member):
    await ctx.send(f"{ctx.author.mention} le ha dado un abrazo a {member.mention}! 🤗")
    _update_profile(ctx.author, member, 'hugs')

# sistema de matrimonio 


@bot.command()
async def marry(ctx, member: discord.Member):
    if ctx.author.id in relationships or member.id in relationships:
        await ctx.send("Uno de ustedes ya está casado.")
    else:
        view = AcceptRejectMarriage(ctx.author, member)
        await ctx.send(f"{ctx.author.mention} le ha propuesto matrimonio a {member.mention}. 💍", view=view)


class AcceptRejectMarriage(View):
    def __init__(self, proposer, proposee):
        super().__init__(timeout=None)
        self.proposer = proposer
        self.proposee = proposee

    @discord.ui.button(label="Aceptar", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.proposee:
            return await interaction.response.send_message("Solo la persona mencionada puede aceptar.", ephemeral=True)

        relationships[self.proposer.id] = self.proposee.id
        relationships[self.proposee.id] = self.proposer.id
        await interaction.response.send_message(f"{self.proposer.mention} y {self.proposee.mention} ahora son pareja. 🎉", ephemeral=False)
        _update_profile(self.proposer, self.proposee, 'edaters')

    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.red)
    async def reject(self, interaction: discord.Interaction, button: Button):
        if interaction.user != self.proposee:
            return await interaction.response.send_message("Solo la persona mencionada puede rechazar.", ephemeral=True)
        await interaction.response.send_message(f"{self.proposee.mention} ha rechazado la propuesta de {self.proposer.mention}.", ephemeral=False)

# sistema de perfiles 


@bot.command()
async def profile(ctx, member: discord.Member = None):
    member = member or ctx.author
    profile = user_profiles.get(member.id, {})
    kisses = profile.get('kisses', 0)
    hugs = profile.get('hugs', 0)
    edaters = profile.get('edaters', "Nadie")

    embed = discord.Embed(
        title=f"Perfil de {member.display_name}", color=discord.Color.purple())
    embed.set_thumbnail(url=member.avatar.url)
    embed.add_field(name="Nombre", value=member.display_name, inline=True)
    embed.add_field(name="Besos", value=kisses, inline=True)
    embed.add_field(name="Abrazos", value=hugs, inline=True)
    embed.add_field(name="Edaters", value=edaters, inline=True)
    await ctx.send(embed=embed)

# esto actualizara tu perfil cada que uses un beso o abrazos y cuando hagas marry con algn saldra e n edaters


def _update_profile(user, target, action):
    if user.id not in user_profiles:
        user_profiles[user.id] = {'kisses': 0, 'hugs': 0, 'edaters': "Nadie"}
    if target.id not in user_profiles:
        user_profiles[target.id] = {'kisses': 0, 'hugs': 0, 'edaters': "Nadie"}

    if action == 'kisses':
        user_profiles[user.id]['kisses'] += 1
        user_profiles[target.id]['kisses'] += 1
    elif action == 'hugs':
        user_profiles[user.id]['hugs'] += 1
        user_profiles[target.id]['hugs'] += 1
    elif action == 'edaters':
        user_profiles[user.id]['edaters'] = target.display_name
        user_profiles[target.id]['edaters'] = user.display_name


# prender el bot
bot.run("token de tu bot")