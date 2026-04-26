#!/bin/bash
# Mistral Vibe Survival Dev Skill Set - Install Script
# Version: 2.0.0
# Usage: ./install.sh [OPTIONS]
#
# Options:
#   --tier1              Core skills only (anti-loop, behavior-audit, focus, verification, overlord)
#   --tier2              Tier 1 + continuity prompts + agents (watchdog, state-sentry)
#   --tier3              Tier 2 + team agents (dev, ops, verify)
#   --specforge          SpecForge pipeline (23 skills, 3 agents, prompts)
#   --researchforge      ResearchForge pipeline (17 skills, 4 agents, prompts)
#   --quality-assurance  Quality Assurance system (6 skills)
#   --focus-productivity Focus & Productivity system (5 skills)
#   --tool-mastery      Tool Mastery system (4 skills)
#   --context-memory     Context & Memory system (4 skills)
#   --all                Everything (default if no flags given)
#   --interactive        Prompt for each tier/pipeline
#   --global             Install to ~/.vibe (default)
#   --local              Install to project .vibe/
#   --list               Show what each tier includes, then exit
#
# Examples:
#   ./install.sh --tier1 --specforge          # Core skills + SpecForge
#   ./install.sh --tier2 --researchforge      # Advanced + ResearchForge
#   ./install.sh --tier3 --specforge --researchforge  # Full system
#   ./install.sh --interactive                # Choose interactively
#   ./install.sh --local --tier1             # Project-local install, core only

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

VIBE_DIR="$HOME/.vibe"
INSTALL_MODE="global"
SELECTED_TIERS=()
SELECTED_PIPELINES=()
INTERACTIVE=false
LIST_ONLY=false

# === TIER DEFINITIONS ===

TIER1_SKILLS=(
  "anti-loop-debug"
  "behavior-audit"
  "focus-master"
  "verification-master"
  "overlord"
  "skill-forge"
)

TIER2_SKILLS=(
  "vibe-continuity"
  "task-decomposer"
  "tool-primacy"
  "context-guardian"
  "pattern-prediction"
  "multi-file-coordinator"
  "git-integrator"
  "self-corrector"
  "constraint-enforcer"
  "code-quality"
  "tool-dominator"
  "focus-guard"
  "memory-archivist"
  "meta-optimizer"
  "verification-enforcer"
)

TIER2_AGENTS=(
  "main-agent.toml"
  "watchdog.toml"
  "state-sentry.toml"
)

TIER2_PROMPTS=(
  "main.md"
  "watchdog.md"
  "state-sentry.md"
)

TIER3_AGENTS=(
  "team-dev.toml"
  "team-ops.toml"
  "team-verify.toml"
)

TIER3_SKILLS=(
  "mistral-vibe-compaction-skill"
)

SPEC_FORGE_SKILLS=()
SPEC_FORGE_AGENTS=(
  "specforge/specforge-overseer.toml"
  "specforge/specforge-analyst.toml"
  "specforge/specforge-architect.toml"
)
SPEC_FORGE_PROMPTS=(
  "specforge-overseer.md"
  "specforge-analyst.md"
  "specforge-architect.md"
)

RESEARCH_FORGE_SKILLS=()
RESEARCH_FORGE_AGENTS=(
  "researchforge/researchforge-overseer.toml"
  "researchforge/researchforge-evidence.toml"
  "researchforge/researchforge-researcher.toml"
  "researchforge/researchforge-synthesizer.toml"
)
RESEARCH_FORGE_PROMPTS=(
  "researchforge-overseer.md"
  "researchforge-evidence.md"
  "researchforge-researcher.md"
  "researchforge-synthesizer.md"
)

# Build skill lists for SpecForge and ResearchForge
for i in {00..22}; do
  num=$(printf "%02d" $i)
  SPEC_FORGE_SKILLS+=("specforge/${num}-*")
done

for i in {00..16}; do
  num=$(printf "%02d" $i)
  RESEARCH_FORGE_SKILLS+=("researchforge/${num}-*")
done

# === MIDDLEWARE PRIMITIVES ===
MIDDLEWARE_DIR="systems/core/middleware"
MIDDLEWARE_FILES=(
  "systems/core/middleware/gating.py"
  "systems/core/middleware/verification.py"
  "systems/core/middleware/drift.py"
  "systems/core/middleware/state_injection.py"
  "systems/core/middleware/tracing.py"
)

# === FUNCTIONS ===

show_list() {
  echo ""
  echo -e "${BLUE}=== Tier 1: Simple ===${NC}"
  echo "  Skills: ${TIER1_SKILLS[*]}"
  echo "  Gives: turn discipline, fewer repeated failures, verification habits"
  echo ""

  echo -e "${BLUE}=== Tier 2: Advanced ===${NC}"
  echo "  Skills: ${TIER2_SKILLS[*]}"
  echo "  Agents: ${TIER2_AGENTS[*]}"
  echo "  Prompts: ${TIER2_PROMPTS[*]}"
  echo "  Gives: continuity-aware execution, watchdog drift checks, state-sentry recovery"
  echo ""

  echo -e "${BLUE}=== Tier 3: Pro ===${NC}"
  echo "  Skills: ${TIER3_SKILLS[*]}"
  echo "  Agents: ${TIER3_AGENTS[*]}"
  echo "  Gives: full multi-agent team system (dev/ops/verify)"
  echo ""

  echo -e "${BLUE}=== Tier 4: SpecForge ===${NC}"
  echo "  23 skills (00-intake through 22-final-spec-assembly)"
  echo "  3 agents (overseer, analyst, architect)"
  echo "  3 prompts"
  echo "  Gives: turns vague intent into enforceable spec contracts + scenarios"
  echo ""

  echo -e "${BLUE}=== Tier 5: ResearchForge ===${NC}"
  echo "  17 skills (00-problem-intake through 16-adversarial-research-review)"
  echo "  4 agents (overseer, evidence, researcher, synthesizer)"
  echo "  4 prompts"
  echo "  Gives: disciplined research packets for complex problem-solving"
  echo ""

  echo -e "${BLUE}=== Runtime Middleware Primitives ===${NC}"
  echo "  GatingMiddleware: hard-gating, phase enforcement, user confirmation"
  echo "  VerificationMiddleware: evidence enforcement, artifact checking"
  echo "  DriftMiddleware: loop detection, oscillation detection, agent invocation"
  echo "  StateInjectionMiddleware: state injection, amnesia prevention"
  echo "  TracingMiddleware: execution tracing, observability, MonitorForge"
  echo "  Gives: reusable runtime control plane for all systems"
  echo ""
}

usage() {
  echo "Usage: ./install.sh [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --tier1              Install Tier 1 (core skills)"
  echo "  --tier2              Install Tier 2 (continuity + agents)"
  echo "  --tier3              Install Tier 3 (full team system)"
  echo "  --specforge          Install SpecForge pipeline"
  echo "  --researchforge      Install ResearchForge pipeline"
  echo "  --all                Install everything (default)"
  echo "  --interactive        Choose interactively"
  echo "  --global             Install to ~/.vibe (default)"
  echo "  --local              Install to .vibe/ (project-local)"
  echo "  --list               Show what each tier includes"
  echo "  --help               Show this help"
  echo ""
  echo "Examples:"
  echo "  ./install.sh --tier1 --specforge"
  echo "  ./install.sh --interactive"
  echo "  ./install.sh --local --tier2"
  echo ""
  echo "Middleware primitives are always installed (systems/core/middleware/)."
  exit 0
}

install_skills() {
  local skill_list=("$@")
  for skill in "${skill_list[@]}"; do
    # Handle glob patterns (for specforge/researchforge numbered skills)
    for dir in skills/$skill; do
      if [ -d "$dir" ]; then
        echo -e "  ${GREEN}✓${NC} $dir"
        cp -r "$dir" "$VIBE_DIR/skills/"
      fi
    done
  done
}

install_agents() {
  local agent_list=("$@")
  for agent in "${agent_list[@]}"; do
    if [ -f "agents/$agent" ]; then
      echo -e "  ${GREEN}✓${NC} $agent"
      cp "agents/$agent" "$VIBE_DIR/agents/"
    fi
  done
}

install_prompts() {
  local prompt_list=("$@")
  for prompt in "${prompt_list[@]}"; do
    if [ -f "prompts/$prompt" ]; then
      echo -e "  ${GREEN}✓${NC} $prompt"
      cp "prompts/$prompt" "$VIBE_DIR/prompts/"
    fi
  done
}

# === PARSE ARGS ===

while [[ $# -gt 0 ]]; do
  case $1 in
    --tier1) SELECTED_TIERS+=("1") ;;
    --tier2) SELECTED_TIERS+=("2") ;;
    --tier3) SELECTED_TIERS+=("3") ;;
    --specforge) SELECTED_PIPELINES+=("specforge") ;;
    --researchforge) SELECTED_PIPELINES+=("researchforge") ;;
    --all) SELECTED_TIERS=("1" "2" "3"); SELECTED_PIPELINES=("specforge" "researchforge") ;;
    --interactive) INTERACTIVE=true ;;
    --global) INSTALL_MODE="global" ;;
    --local) INSTALL_MODE="local" ;;
    --list) LIST_ONLY=true ;;
    --help|-h) usage ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      usage ;;
  esac
  shift
done

if [ "$LIST_ONLY" = true ]; then
  show_list
  exit 0
fi

# === INTERACTIVE MODE ===

if [ "$INTERACTIVE" = true ]; then
  echo -e "${BLUE}=== Interactive Install ===${NC}"
  echo "Select what to install (y/n):"
  echo ""

  read -p "  Tier 1 - Core skills (anti-loop, behavior-audit, etc.)? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then SELECTED_TIERS+=("1"); fi

  read -p "  Tier 2 - Advanced (continuity, watchdog, state-sentry)? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then SELECTED_TIERS+=("2"); fi

  read -p "  Tier 3 - Pro (full team: dev, ops, verify)? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then SELECTED_TIERS+=("3"); fi

  read -p "  Tier 4 - SpecForge (specification factory, 23 skills)? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then SELECTED_PIPELINES+=("specforge"); fi

  read -p "  Tier 5 - ResearchForge (research-only pipeline, 17 skills)? [y/N] " ans
  if [[ "$ans" =~ ^[Yy]$ ]]; then SELECTED_PIPELINES+=("researchforge"); fi

  echo ""
fi

# Default to --all if nothing selected
if [ ${#SELECTED_TIERS[@]} -eq 0 ] && [ ${#SELECTED_PIPELINES[@]} -eq 0 ]; then
  echo -e "${YELLOW}No tiers selected, defaulting to --all${NC}"
  SELECTED_TIERS=("1" "2" "3")
  SELECTED_PIPELINES=("specforge" "researchforge")
fi

# === SET INSTALL DIR ===

if [ "$INSTALL_MODE" = "local" ]; then
  VIBE_DIR="$(pwd)/.vibe"
  echo -e "${BLUE}Installing to project-local: $VIBE_DIR${NC}"
else
  VIBE_DIR="$HOME/.vibe"
  echo -e "${BLUE}Installing to global: $VIBE_DIR${NC}"
fi

# === START INSTALL ===

echo -e "${BLUE}🚀 Starting Mistral Vibe Survival Dev Skill Set Installation...${NC}"
echo -e "  Tiers: ${SELECTED_TIERS[*]:-none}"
echo -e "  Pipelines: ${SELECTED_PIPELINES[*]:-none}"
echo ""

# Backup existing
if [ -d "$VIBE_DIR" ]; then
  BACKUP_DIR="$HOME/.vibe_backup_$(date +%s)"
  echo -e "${BLUE}📦 Backing up existing $VIBE_DIR to $BACKUP_DIR...${NC}"
  mkdir -p "$BACKUP_DIR"
  cp -r "$VIBE_DIR/"* "$BACKUP_DIR/" 2>/dev/null || true
fi

# Create directories
echo -e "${BLUE}📂 Creating directory structure...${NC}"
mkdir -p "$VIBE_DIR/prompts"
mkdir -p "$VIBE_DIR/agents"
mkdir -p "$VIBE_DIR/skills"
mkdir -p "$VIBE_DIR/systems/core/middleware"

# === INSTALL TIER 1 (always base) ===

echo -e "${BLUE}🛠️  Installing Tier 1 (core skills)...${NC}"
install_skills "${TIER1_SKILLS[@]}"

# === INSTALL TIER 2 ===

if [[ " ${SELECTED_TIERS[@]} " =~ " 2 " ]] || [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  echo -e "${BLUE}🛠️  Installing Tier 2 (continuity + agents)...${NC}"
  install_skills "${TIER2_SKILLS[@]}"
  install_agents "${TIER2_AGENTS[@]}"
  install_prompts "${TIER2_PROMPTS[@]}"
fi

# === INSTALL TIER 3 ===

if [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  echo -e "${BLUE}🛠️  Installing Tier 3 (full team system)...${NC}"
  install_skills "${TIER3_SKILLS[@]}"
  install_agents "${TIER3_AGENTS[@]}"
fi

# === INSTALL SPECFORGE ===

if [[ " ${SELECTED_PIPELINES[@]} " =~ " specforge " ]]; then
  echo -e "${BLUE}🛠️  Installing SpecForge pipeline (23 skills, 3 agents)...${NC}"
  # Install all specforge skills (glob for numbered dirs + any additional)
  for dir in skills/specforge/*/; do
    if [ -d "$dir" ]; then
      echo -e "  ${GREEN}✓${NC} $dir"
      cp -r "$dir" "$VIBE_DIR/skills/"
    fi
  done
  install_agents "${SPEC_FORGE_AGENTS[@]}"
  install_prompts "${SPEC_FORGE_PROMPTS[@]}"
fi

# === INSTALL RESEARCHFORGE ===

if [[ " ${SELECTED_PIPELINES[@]} " =~ " researchforge " ]]; then
  echo -e "${BLUE}🛠️  Installing ResearchForge pipeline (17 skills, 4 agents)...${NC}"
  for dir in skills/researchforge/*/; do
    if [ -d "$dir" ]; then
      echo -e "  ${GREEN}✓${NC} $dir"
      cp -r "$dir" "$VIBE_DIR/skills/"
    fi
  done
  install_agents "${RESEARCH_FORGE_AGENTS[@]}"
  install_prompts "${RESEARCH_FORGE_PROMPTS[@]}"
fi

# === INSTALL MIDDLEWARE PRIMITIVES ===

echo -e "${BLUE}⚙️  Installing middleware primitives...${NC}"
for mw in "${MIDDLEWARE_FILES[@]}"; do
  if [ -f "$mw" ]; then
    echo -e "  ${GREEN}✓${NC} $mw"
    cp "$mw" "$VIBE_DIR/systems/core/middleware/"
  fi
done

# === INSTALL CONFIG ===

echo -e "${BLUE}⚙️  Writing config.toml...${NC}"

mkdir -p "$VIBE_DIR/config.toml" 2>/dev/null || true

# Build enabled_skills list
SKILLS_LIST=""
if [[ " ${SELECTED_TIERS[@]} " =~ " 1 " ]]; then
  for s in "${TIER1_SKILLS[@]}"; do
    SKILLS_LIST="$SKILLS_LIST\n  \"${s}\","
  done
fi
if [[ " ${SELECTED_TIERS[@]} " =~ " 2 " ]] || [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  for s in "${TIER2_SKILLS[@]}"; do
    SKILLS_LIST="$SKILLS_LIST\n  \"${s}\","
  done
fi
if [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  for s in "${TIER3_SKILLS[@]}"; do
    SKILLS_LIST="$SKILLS_LIST\n  \"${s}\","
  done
fi
if [[ " ${SELECTED_PIPELINES[@]} " =~ " specforge " ]]; then
  for dir in skills/specforge/*/; do
    if [ -d "$dir" ]; then
      skill_name=$(basename "$dir")
      SKILLS_LIST="$SKILLS_LIST\n  \"${skill_name}\","
    fi
  done
fi
if [[ " ${SELECTED_PIPELINES[@]} " =~ " researchforge " ]]; then
  for dir in skills/researchforge/*/; do
    if [ -d "$dir" ]; then
      skill_name=$(basename "$dir")
      SKILLS_LIST="$SKILLS_LIST\n  \"${skill_name}\","
    fi
  done
fi

# Build enabled_agents list
AGENTS_LIST=""
if [[ " ${SELECTED_TIERS[@]} " =~ " 2 " ]] || [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  AGENTS_LIST="$AGENTS_LIST\n  \"state-sentry\",\n  \"watchdog\","
fi
if [[ " ${SELECTED_TIERS[@]} " =~ " 3 " ]]; then
  AGENTS_LIST="$AGENTS_LIST\n  \"team-dev\",\n  \"team-ops\",\n  \"team-verify\","
fi
if [[ " ${SELECTED_PIPELINES[@]} " =~ " specforge " ]]; then
  AGENTS_LIST="$AGENTS_LIST\n  \"specforge-overseer\",\n  \"specforge-analyst\",\n  \"specforge-architect\","
fi
if [[ " ${SELECTED_PIPELINES[@]} " =~ " researchforge " ]]; then
  AGENTS_LIST="$AGENTS_LIST\n  \"researchforge-overseer\",\n  \"researchforge-evidence\",\n  \"researchforge-researcher\",\n  \"researchforge-synthesizer\","
fi

AGENT_PATHS="[\"agents\""
if [[ " ${SELECTED_PIPELINES[@]} " =~ " specforge " ]]; then
  AGENT_PATHS="$AGENT_PATHS, \"agents/specforge\""
fi
if [[ " ${SELECTED_PIPELINES[@]} " =~ " researchforge " ]]; then
  AGENT_PATHS="$AGENT_PATHS, \"agents/researchforge\""
fi
AGENT_PATHS="$AGENT_PATHS]"

cat << CONFIG > "$VIBE_DIR/config.toml"
# Mistral Vibe Config - Installed by Survival Dev Skill Set
# Generated: $(date)

active_model = "devstral-2"
system_prompt_id = "main"

# Paths
skill_paths = ["skills"]
agent_paths = $AGENT_PATHS

# Enabled agents
enabled_agents = [$AGENTS_LIST
]

# Enabled skills
enabled_skills = [$SKILLS_LIST
]

# Subagents
[subagents]
enabled = true
default_model = "pixtral-large-latest"
max_concurrent = 2
auto_approve_subagents = true
poll_interval = 5

# Tool permissions
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

# Models
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

# Checkpointing
[checkpoint]
enabled = true
file = ".checkpoint.json"
verify_after_write = true

# UI
vim_keybindings = false
autocopy_to_clipboard = true
api_timeout = 720.0
CONFIG

chmod +x install.sh

echo ""
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}   Installed to: $VIBE_DIR${NC}"
echo ""
echo -e "${YELLOW}Next steps:${NC}"
echo "  1. Run 'vibe' to start with your installed setup"
echo "  2. Or pick a specific agent: vibe --agent specforge-overseer"
echo "  3. See README.md for usage docs"
echo "  4. Middleware primitives installed to: $VIBE_DIR/systems/core/middleware/"
echo ""
