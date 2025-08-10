#!/usr/bin/env python3
"""
🤖 Ultra-simple autonomous bot for role assignment via invite links
EVERYTHING IN ONE FILE - no external dependencies!
"""

import asyncio
import logging
import os
from typing import Dict, Optional

import discord
from discord.ext import commands


def load_invite_mappings() -> Dict[str, str]:
    """Load invite code mappings from environment variables"""
    mappings = {}
    
    # Load invite codes from environment variables
    invite_vars = {
        'INVITE_MODERATOR': 'moderator',
        'INVITE_CONTRIBUTOR': 'contributor', 
        'INVITE_MENTOR': 'mentor',
        'INVITE_JURY': 'jury'
    }
    
    for env_var, role_type in invite_vars.items():
        invite_code = os.getenv(env_var)
        if invite_code:
            mappings[invite_code] = role_type
        else:
            logger.warning(f"   Missing environment variable: {env_var}")
    
    return mappings


# 🎭 Role type to Discord role mapping
DISCORD_ROLES = {
    "moderator": "Moderator",
    "contributor": "Contributor", 
    "mentor": "Mentor",
    "jury": "Jury"
}

# 📊 Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


class UltraSimpleBot(commands.Bot):
    """Ultra-simple bot for role assignment"""
    
    def __init__(self):
        # Minimal required intents
        intents = discord.Intents.default()
        intents.members = True
        intents.invites = True
        intents.guilds = True
        
        super().__init__(command_prefix='!', intents=intents, help_command=None)
        
        # Server data
        self.guild_id = int(os.getenv('DISCORD_GUILD_ID'))
        self.guild = None
        
        # Invite mappings loaded from environment variables
        self.invite_mappings: Dict[str, str] = {}
        
        # Invite cache for tracking changes
        self.invite_cache: Dict[str, discord.Invite] = {}
    
    async def on_ready(self):
        """Bot startup"""
        logger.info(f"✅ Bot {self.user} connected!")
        
        # Get server
        self.guild = self.get_guild(self.guild_id)
        if not self.guild:
            logger.error(f"❌ Server with ID {self.guild_id} not found")
            return
        
        logger.info(f"🏠 Server: {self.guild.name}")
        
        # Load invite mappings from environment variables
        logger.info("📊 Loading invite mappings from environment variables...")
        self.invite_mappings = load_invite_mappings()
        
        if not self.invite_mappings:
            logger.error("❌ No invite mappings loaded! Check environment variables.")
            return
        
        logger.info(f"📊 Loaded {len(self.invite_mappings)} invite mappings:")
        for code, role_type in self.invite_mappings.items():
            discord_role = DISCORD_ROLES.get(role_type, "UNKNOWN")
            logger.info(f"   {code} → {role_type} → @{discord_role}")
        
        # Cache invites
        await self.cache_invites()
        logger.info("🎯 Ready for role assignment!")
    
    async def cache_invites(self):
        """Cache current invites"""
        try:
            invites = await self.guild.invites()
            self.invite_cache = {invite.code: invite for invite in invites}
            logger.info(f"📋 Cached {len(self.invite_cache)} invites")
        except Exception as e:
            logger.error(f"❌ Error caching invites: {e}")
    
    async def on_member_join(self, member: discord.Member):
        """Handle new member joining"""
        logger.info(f"👤 New member: {member.name}#{member.discriminator} (ID: {member.id})")
        
        # Find used invite
        used_invite = await self.find_used_invite()
        
        if not used_invite:
            logger.warning(f"⚠️ Could not determine invite for {member.name}")
            return
        
        logger.info(f"🔍 Used invite: {used_invite.code}")
        
        # Check mapping
        if used_invite.code not in self.invite_mappings:
            logger.warning(f"⚠️ Invite {used_invite.code} not found in mappings")
            return
        
        # Get role
        role_type = self.invite_mappings[used_invite.code]
        logger.info(f"🎭 Determined role: {role_type}")
        
        # Assign role
        success = await self.assign_role(member, role_type)
        
        if success:
            logger.info(f"✅ Role '{role_type}' assigned to {member.name}")
        else:
            logger.error(f"❌ Failed to assign role '{role_type}' to {member.name}")
    
    async def find_used_invite(self) -> Optional[discord.Invite]:
        """Find which invite was used by comparing uses count"""
        try:
            current_invites = await self.guild.invites()
            current_dict = {invite.code: invite for invite in current_invites}
            
            # Compare uses with cache
            for code, current_invite in current_dict.items():
                if code in self.invite_cache:
                    if current_invite.uses > self.invite_cache[code].uses:
                        self.invite_cache[code] = current_invite
                        return current_invite
            
            # Update cache
            self.invite_cache = current_dict
            
        except Exception as e:
            logger.error(f"❌ Error finding used invite: {e}")
        
        return None
    
    async def assign_role(self, member: discord.Member, role_type: str) -> bool:
        """Assign role to member"""
        
        if role_type not in DISCORD_ROLES:
            logger.error(f"❌ Unknown role type: {role_type}")
            return False
        
        discord_role_name = DISCORD_ROLES[role_type]
        
        # Find role on server
        role = discord.utils.get(self.guild.roles, name=discord_role_name)
        
        if not role:
            logger.error(f"❌ Role '@{discord_role_name}' not found on server!")
            return False
        
        try:
            await member.add_roles(role, reason=f"Automatic role assignment via invite ({role_type})")
            return True
        except Exception as e:
            logger.error(f"❌ Error assigning role: {e}")
            return False


async def main():
    """Main function"""
    logger.info("🚀 Starting ultra-simple bot...")
    
    # Check environment variables
    token = os.getenv('DISCORD_TOKEN')
    guild_id = os.getenv('DISCORD_GUILD_ID')
    
    if not token:
        logger.error("❌ DISCORD_TOKEN not configured!")
        logger.error("   Set environment variable: DISCORD_TOKEN=your_token")
        return
    
    if not guild_id:
        logger.error("❌ DISCORD_GUILD_ID not configured!")
        logger.error("   Set environment variable: DISCORD_GUILD_ID=1396918326868840538")
        return
    
    # Start bot
    bot = UltraSimpleBot()
    
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        logger.info("⏹️ Stopping bot...")
    except Exception as e:
        logger.error(f"❌ Critical error: {e}")
    finally:
        await bot.close()


if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Start bot
    asyncio.run(main())