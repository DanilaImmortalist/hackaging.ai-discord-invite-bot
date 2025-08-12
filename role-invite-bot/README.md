# 🤖 Ultra-Simple Bot for Automatic Roles

**MAXIMALLY SIMPLIFIED!** Everything in one file - no databases, no dependencies!

## 📁 What's here:

- `main.py` - **ENTIRE BOT IN ONE FILE** with environment-based mapping
- `requirements.txt` - only 2 dependencies  
- `.env` - environment variables for copying to Render

## 🎯 How it works:

1. **Invite codes loaded from ENVIRONMENT VARIABLES**:
   ```bash
   INVITE_MODERATOR=your_code_here
   INVITE_CHALLENGEMASTER=your_code_here
   INVITE_MENTOR=your_code_here
   INVITE_JURY=your_code_here
   ```

2. **Join via link** → automatic role assignment
3. **No external files** - everything configured via environment variables

## 🚀 Deploy to Render:

### 1. Upload THIS folder to GitHub

### 2. Create Web Service on Render:
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`

### 3. Add Environment Variables:
```
DISCORD_TOKEN=your_discord_bot_token_here
DISCORD_GUILD_ID=your_discord_server_id_here
INVITE_MODERATOR=your_moderator_invite_code
INVITE_CHALLENGEMASTER=your_challengemaster_invite_code
INVITE_MENTOR=your_mentor_invite_code
INVITE_JURY=your_jury_invite_code
```

⚠️ **IMPORTANT**: Use your own values from the `.env` file - DO NOT use the examples above!

### 4. Deploy! 🎉

## 🔗 How to get your invite links:

After creating invites with your bot token, you'll get links like:

| Role | Link Format |
|------|-------------|
| **Moderator** | https://discord.gg/YOUR_CODE_HERE |
| **ChallengeMaster** | https://discord.gg/YOUR_CODE_HERE |
| **Mentor** | https://discord.gg/YOUR_CODE_HERE |
| **Jury** | https://discord.gg/YOUR_CODE_HERE |

📋 **Check your `.env` file for the actual codes and links!**

## ✏️ Changing invites:

Need new invites? Just update the environment variables on Render and redeploy!

---

**That's it! Nothing else needed!** 🚀
