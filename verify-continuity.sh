#!/bin/bash

# =============================================================================
# Vibe Continuity - Diagnostic Verification Script
# Version: 2.1.0
# Purpose: Verify all continuity framework components are correctly deployed
# Usage: bash ~/.vibe/scripts/verify-continuity.sh
# =============================================================================

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Counters
PASS=0
FAIL=0
WARN=0

# Header
printf "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}\n"
printf "${BLUE}║  Vibe Continuity Framework - Deployment Verification     ║${NC}\n"
printf "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}\n"
echo ""

# =============================================================================
# SECTION 1: File Existence Checks
# =============================================================================
printf "${BLUE}[1/5] File Existence Checks${NC}\n"
printf "───────────────────────────────────────────────────────────────\n"

FILE_CHECKS=(
  "~/.vibe/skills/vibe-continuity/SKILL.md:vibe-continuity skill"
  "~/.vibe/prompts/main.md:Architect system prompt"
  "~/.vibe/prompts/watchdog.md:Watchdog system prompt"
  "~/.vibe/prompts/state-sentry.md:State Sentry system prompt"
  "~/.vibe/agents/state-sentry.toml:State Sentry agent"
  "~/.vibe/agents/watchdog.toml:Watchdog agent"
  "~/.vibe/config.toml:Vibe configuration"
)

for file_desc in "${FILE_CHECKS[@]}"; do
  IFS=':' read -r file desc <<< "$file_desc"
  file=$(eval echo "$file")
  if [ -f "$file" ]; then
    printf "${GREEN}✅${NC} %s\n" "$desc"
    ((PASS++)) || true
  else
    printf "${RED}❌${NC} %s (MISSING: %s)\n" "$desc" "$file"
    ((FAIL++))
  fi
done

echo ""

# =============================================================================
# SECTION 2: Configuration Checks
# =============================================================================
printf "${BLUE}[2/5] Configuration Checks${NC}\n"
printf "───────────────────────────────────────────────────────────────\n"
CONFIG_CHECKS=(
  "auto_compact_threshold = 204800:Compaction threshold optimized"
  "enabled_agents.*state-sentry:State Sentry enabled"
  "enabled_agents.*watchdog:Watchdog enabled"
  "enabled_skills.*vibe-continuity:vibe-continuity skill enabled"
  "skill_paths.*~/.vibe/skills:Global skills path configured"
  "agent_paths.*~/.vibe/agents:Global agents path configured"
  "tools.task.permission = \"always\":Task tool always allowed"
)

for check_desc in "${CONFIG_CHECKS[@]}"; do
  IFS=':' read -r pattern desc <<< "$check_desc"
  if grep -qE "$pattern" ~/.vibe/config.toml 2>/dev/null; then
    printf "${GREEN}✅${NC} %s\n" "$desc"
    ((PASS++)) || true
  else
    printf "${RED}❌${NC} %s\n" "$desc"
    printf "   ${YELLOW}Expected pattern:${NC} %s\n" "$pattern"
    ((FAIL++))
  fi
done

echo ""

# =============================================================================
# SECTION 3: Skill Format Validation
# =============================================================================
printf "${BLUE}[3/5] Skill Format Validation${NC}\n"
printf "───────────────────────────────────────────────────────────────\n"

SKILL_FILE="~/.vibe/skills/vibe-continuity/SKILL.md"

# Check YAML frontmatter
if head -5 "$SKILL_FILE" | grep -q "^---"; then
  printf "${GREEN}✅${NC} YAML frontmatter starts correctly\n"
  ((PASS++)) || true
else
  printf "${RED}❌${NC} YAML frontmatter missing or malformed\n"
  ((FAIL++))
fi

# Check required YAML fields
for field in "name:" "description:" "user-invocable:" "tools:"; do
  if grep -q "$field" "$SKILL_FILE"; then
    printf "${GREEN}✅${NC} YAML field '%s' present\n" "$field"
    ((PASS++)) || true
  else
    printf "${RED}❌${NC} YAML field '%s' missing\n" "$field"
    ((FAIL++))
  fi
done

# Check required tools
echo ""
printf "Checking required tools...\n"
for tool in "task" "read_file" "todo" "bash" "grep"; do
  if grep -A10 "^tools:" "$SKILL_FILE" | grep -q "\- $tool"; then
    printf "${GREEN}✅${NC} Tool '%s' declared\n" "$tool"
    ((PASS++)) || true
  else
    printf "${RED}❌${NC} Tool '%s' missing\n" "$tool"
    ((FAIL++))
  fi
done

echo ""

# =============================================================================
# SECTION 4: Agent Configuration Validation
# =============================================================================
printf "${BLUE}[4/5] Agent Configuration Validation${NC}\n"
printf "───────────────────────────────────────────────────────────────\n"

AGENT_FILES=(
  "~/.vibe/agents/state-sentry.toml"
  "~/.vibe/agents/continuation-observer.toml"
)

for agent_file in "${AGENT_FILES[@]}"; do
  agent_name=$(basename "$agent_file" .toml)
  echo "Checking $agent_name..."
  
  # Check agent_type
  if grep -q 'agent_type = "subagent"' "$agent_file"; then
    printf "  ${GREEN}✅${NC} agent_type = subagent\n"
    ((PASS++)) || true
  else
    printf "  ${RED}❌${NC} agent_type not set to subagent\n"
    ((FAIL++))
  fi
  
  # Check auto_approve
  if grep -q 'auto_approve = true' "$agent_file"; then
    printf "  ${GREEN}✅${NC} auto_approve = true\n"
    ((PASS++)) || true
  else
    printf "  ${RED}❌${NC} auto_approve not set to true\n"
    ((FAIL++))
  fi
  
  # Check safety
  if grep -q 'safety = "safe"' "$agent_file"; then
    printf "  ${GREEN}✅${NC} safety = safe\n"
    ((PASS++)) || true
  else
    printf "  ${RED}❌${NC} safety not set to safe\n"
    ((FAIL++))
  fi
  
  # Check enabled
  if grep -q 'enabled = true' "$agent_file"; then
    printf "  ${GREEN}✅${NC} enabled = true\n"
    ((PASS++)) || true
  else
    printf "  ${RED}❌${NC} enabled not set to true\n"
    ((FAIL++))
  fi
  
  echo ""
done

# =============================================================================
# SECTION 5: Environment Checks
# =============================================================================
printf "${BLUE}[5/5] Environment Checks${NC}\n"
printf "───────────────────────────────────────────────────────────────\n"

# Check if vibe is installed
if command -v vibe &>/dev/null; then
  printf "${GREEN}✅${NC} Mistral Vibe CLI is installed\n"
  ((PASS++)) || true
else
  printf "${YELLOW}⚠️${NC} Mistral Vibe CLI not found in PATH\n"
  printf "   Run: uv tool install mistral-vibe\n"
  ((WARN++))
fi

# Check if .env file exists with API key
if [ -f ~/.vibe/.env ] && grep -q "MISTRAL_API_KEY=" ~/.vibe/.env; then
  printf "${GREEN}✅${NC} API key configured in ~/.vibe/.env\n"
  ((PASS++)) || true
else
  printf "${YELLOW}⚠️${NC} API key not configured\n"
  printf "   Run: echo 'MISTRAL_API_KEY=your-key' > ~/.vibe/.env\n"
  ((WARN++))
fi

# Check if .vibeignore is being respected by config
if grep -q "codeignore_file" ~/.vibe/config.toml; then
  printf "${GREEN}✅${NC} .vibeignore configured in config\n"
  ((PASS++)) || true
else
  printf "${YELLOW}⚠️${NC} .vibeignore not referenced in config (may still work)\n"
  ((WARN++))
fi

echo ""

# =============================================================================
# SUMMARY
# =============================================================================
printf "${BLUE}╔════════════════════════════════════════════════════════════════╗${NC}\n"
printf "${BLUE}║  VERIFICATION SUMMARY                                             ║${NC}\n"
printf "${BLUE}╚════════════════════════════════════════════════════════════════╝${NC}\n"
echo ""
printf "  ${GREEN}Passed:${NC} %d\n" "$PASS"
printf "  ${RED}Failed:${NC} %d\n" "$FAIL"
printf "  ${YELLOW}Warnings:${NC} %d\n" "$WARN"
echo ""

if [ $FAIL -eq 0 ]; then
  if [ $WARN -eq 0 ]; then
    printf "${GREEN}✅ ALL CHECKS PASSED! The continuity framework is fully deployed.${NC}\n"
    printf "\n${YELLOW}Next step:${NC}\n"
    printf "  Run: vibe\n"
    printf "\n"
    exit 0
  else
    printf "${YELLOW}⚠️  ALL CRITICAL CHECKS PASSED (with warnings)${NC}\n"
    printf "\n${YELLOW}Next steps:${NC}\n"
    printf "  1. Fix warnings above\n"
    printf "  2. Run: vibe\n"
    printf "\n"
    exit 0
  fi
else
  printf "${RED}❌ SOME CHECKS FAILED! Please fix the issues above.${NC}\n"
  printf "\n"
  exit 1
fi
