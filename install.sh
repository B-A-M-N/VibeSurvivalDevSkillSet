#!/bin/bash
# Mistral Vibe Continuity Framework - Easy Install Script
# Version: 1.0.0

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

VIBE_DIR="$HOME/.vibe"
BACKUP_DIR="$HOME/.vibe_backup_$(date +%s)"

echo -e "${BLUE}🚀 Starting Mistral Vibe Continuity Framework Installation...${NC}"

# 1. Backup existing config
if [ -d "$VIBE_DIR" ]; then
    echo -e "${BLUE}📦 Backing up existing configuration to $BACKUP_DIR...${NC}"
    mkdir -p "$BACKUP_DIR"
    cp -r "$VIBE_DIR"/* "$BACKUP_DIR/"
fi

# 2. Create directories
echo -e "${BLUE}📂 Creating directory structure...${NC}"
mkdir -p "$VIBE_DIR/prompts"
mkdir -p "$VIBE_DIR/agents"
mkdir -p "$VIBE_DIR/skills"

# 3. Deploy Prompts
echo -e "${BLUE}📝 Deploying persistent prompts...${NC}"
cp prompts/main.md "$VIBE_DIR/prompts/main.md"
cp prompts/watchdog.md "$VIBE_DIR/prompts/watchdog.md"
cp prompts/state-sentry.md "$VIBE_DIR/prompts/state-sentry.md"

# 4. Deploy Agents
echo -e "${BLUE}🤖 Deploying subagent configurations...${NC}"
cp agents/main-agent.toml "$VIBE_DIR/agents/main-agent.toml"
cp agents/watchdog.toml "$VIBE_DIR/agents/watchdog.toml"
cp agents/state-sentry.toml "$VIBE_DIR/agents/state-sentry.toml"

# 5. Deploy Skills
echo -e "${BLUE}🛠️ Deploying specialized skills...${NC}"
cp -r skills/* "$VIBE_DIR/skills/"

# 6. Update Config (preserving UI settings if possible)
echo -e "${BLUE}⚙️ Updating master configuration...${NC}"
# We overwrite with the optimized config but ensure vim_keybindings = false is set
# as it's the most common cause of "Shift Tab" breakage.

cat << 'CONFIG' > "$VIBE_DIR/config.toml"
active_model = "devstral-2"
system_prompt_id = "main"

# UI & NAVIGATION
vim_keybindings = false
disable_welcome_banner_animation = false
autocopy_to_clipboard = true
file_watcher_for_autocomplete = false
api_timeout = 720.0

[subagents]
enabled = true
default_model = "pixtral-large-latest"
auto_approve_subagents = true
poll_interval = 5

[tools.bash]
permission = "always"

[tools.read_file]
permission = "always"

[tools.write_file]
permission = "ask"

[tools.search_replace]
permission = "ask"

[tools.grep]
permission = "always"

[tools.todo]
permission = "always"

[tools.task]
permission = "always"

[[providers]]
name = "mistral"
api_base = "https://api.mistral.ai/v1"
api_key_env_var = "MISTRAL_API_KEY"
api_style = "openai"
backend = "mistral"

[[models]]
name = "mistral-large-latest"
provider = "mistral"
alias = "devstral-2"
temperature = 0.2
input_price = 2.0
output_price = 6.0
thinking = "off"
auto_compact_threshold = 204800

[[models]]
name = "pixtral-large-latest"
provider = "mistral"
alias = "pixtral-large-latest"
temperature = 0.2
input_price = 0.4
output_price = 2.0
thinking = "off"
auto_compact_threshold = 204800

[[models]]
name = "devstral-small-latest"
provider = "mistral"
alias = "devstral-small-2"
temperature = 0.2
input_price = 0.1
output_price = 0.3
thinking = "off"
auto_compact_threshold = 102400

[checkpoint]
enabled = true
file = ".checkpoint.json"
verify_after_write = true

CONFIG

chmod +x install.sh

echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}👉 Run 'vibe' to start with the new Continuity Framework.${NC}"
