import asyncio
import random
import os
from datetime import datetime, timedelta
import discord
from discord.ext import commands

# Configuration
CHANNEL_ID = 1548017393199095878  # ID de ton salon
DISBOARD_ID = 302050872383242240 # ID du bot Disboard

# Pour un SELFBOT (discord.py-self), on récupère le Token caché dans l'hébergeur
TOKEN = os.environ.get("DISCORD_TOKEN")

# INITIALISATION POUR SELFBOT (Pas d'intents nécessaires, évite l'AttributeError)
bot = commands.Bot(command_prefix="!", chunk_guilds_at_startup=False)

def get_formatted_time(dt=None):
    if dt is None:
        dt = datetime.now()
    months = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
    days = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
    return f"{days[dt.weekday()]} {dt.day} {months[dt.month - 1]} {dt.year} {dt.strftime('%H:%M')}"

async def human_delay(min_sec=2, max_sec=5):
    """Simule un délai humain aléatoire pour éviter la détection de pattern par Discord"""
    await asyncio.sleep(random.uniform(min_sec, max_sec))

async def auto_bump_loop():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    
    if not channel:
        try:
            channel = await bot.fetch_channel(CHANNEL_ID)
        except Exception as e:
            print(f"[Erreur] Salon introuvable : {e}")
            return

    while not bot.is_closed():
        try:
            print("[Info] Vérification de l'état du bump...")
            
            # Simulation humaine avant d'agir
            async with channel.typing():
                await human_delay(3, 7)

            # Exécution de la commande /bump de Disboard
            disboard = await bot.fetch_user(DISBOARD_ID)
            commands_list = await disboard.application_commands()
            bump_cmd = next((cmd for cmd in commands_list if cmd.name == 'bump'), None)
            
            success = False
            if bump_cmd:
                await bump_cmd.run(channel=channel)
                success = True
            else:
                await channel.send('/bump')
                success = True

            now = datetime.now()
            next_bump = now + timedelta(hours=2, minutes=5) # Sécurité pour éviter le cooldown Disboard

            if success:
                msg_content = (
                    f"<:novag3n:1538646924520063086> **NovaG3n server**\n"
                    f"<:955945booster1:1523415463474888887> **Bump réussi !**\n"
                    f"<:clydebot:1551308256272449666> Bot: `{bot.user.name}`\n"
                    f"<:ticking:1551306977559322694> {get_formatted_time(now)}\n"
                    f"<:timetraveller:1551306915747991672> Prochain bump prévu vers : **{get_formatted_time(next_bump)}**"
                )
                await channel.send(msg_content)
                print('[Succès] Bump effectué et message de suivi envoyé.')
            
            # Attente intelligente de 2 heures avec variation aléatoire (Anti-bot detection)
            wait_time = 7200 + random.randint(120, 350) 
            await asyncio.sleep(wait_time)

        except Exception as error:
            print(f'[Erreur] Une erreur est survenue dans la boucle de bump : {error}')
            await asyncio.sleep(300)

@bot.event
async def on_ready():
    print(f'-----------------------------------')
    print(f'Connecté en tant que : {bot.user.name}')
    print(f'Mode : Selfbot Ultra-Optimisé & Indétectable')
    print(f'-----------------------------------')
    bot.loop.create_task(auto_bump_loop())

if TOKEN:
    bot.run(TOKEN)
else:
    print("[Erreur Critique] Aucun DISCORD_TOKEN trouvé dans les variables d'environnement de l'hébergeur.")
