# Agent Configuration: Dual-Agent Continuation Enforcement System
# Target: Devstral-2 / Mistral Vibe CLI
# Version: 2.0.0
# Architecture: Dual-Agent (Main + Observer)
# Stability bias: HIGH — do not modify without testing against failure injection suite

# ─────────────────────────────────────────────
# MAIN AGENT
# ─────────────────────────────────────────────

[agent]
name = "continuation-main"
model = "mistral-vibe-cli-latest"
system_prompt_file = "system-prompt.md"
skill_files = ["SKILL.md"]

# Temperature 0 is mandatory.
# Variation in deterministic execution steps is not acceptable.
# Creative sub-tasks require a separate sub-agent with elevated temperature.
temperature = 0

# Context window — set to 80% of deployment limit to leave headroom for checkpoint writes
# Devstral-2 deployment limit: verify per environment
max_tokens = 8192

# Context compaction: trigger predictably at 75% rather than at unpredictable buffer-full events
context_compaction_threshold = 0.75

# ─────────────────────────────────────────────
# OBSERVER AGENT
# ─────────────────────────────────────────────

[observer_agent]
name = "continuation-observer"
model = "mistral-vibe-cli-latest"
system_prompt_file = "observer-system-prompt.md"
skill_files = ["SKILL.md", "OBSERVER-SPEC.md"]

# Observer temperature: 0
# Observer makes no creative decisions. Structural reads and writes only.
temperature = 0

# Observer token budget is small — it reads state, it does not generate code
max_tokens = 2048

# Observer runs on a polling interval, not per main-agent step
# Unit: seconds
observer_poll_interval_seconds = 30

# Observer is passive by default — it activates based on structural criteria, not user request
observer_default_mode = "passive"

# ─────────────────────────────────────────────
# TOOLS — MAIN AGENT
# ─────────────────────────────────────────────

[tools]

[tools.file_system]
enabled = true
read = true
write = true
delete = true
allowed_paths = [
  "./",
  ".checkpoint.json",
  ".checkpoint.md",
  ".checkpoint.lock",
  ".failed/",
  ".checkpoint.archive/"
]
# Main agent must NOT write to observer-owned files
forbidden_paths = [
  ".observer-state.json"
]
# Main agent may delete .observer-inject.json only after consumption
consume_inject_on_read = true

[tools.shell]
enabled = true
allow_network = false  # override per-task if network access is required

[tools.search]
enabled = false  # disable during execution tasks; re-enable for research tasks only

# ─────────────────────────────────────────────
# TOOLS — OBSERVER AGENT
# ─────────────────────────────────────────────

[observer_tools]

[observer_tools.file_system]
enabled = true
read = true
write = true
delete = false  # observer does not delete main agent files
allowed_paths = [
  ".checkpoint.json",         # read only
  ".checkpoint.md",           # read only
  ".checkpoint.lock",         # read only (liveness check)
  ".observer-state.json",     # observer writes here
  ".observer-inject.json"     # observer writes here on intervention
]
forbidden_write_paths = [
  ".checkpoint.json",         # observer NEVER writes main checkpoint
  ".checkpoint.md",
  ".checkpoint.lock"
]

[observer_tools.shell]
enabled = false  # observer does not execute shell commands

[observer_tools.search]
enabled = false

# ─────────────────────────────────────────────
# STATE FILES
# ─────────────────────────────────────────────

[state]
# Main agent state
checkpoint_json = ".checkpoint.json"
checkpoint_md = ".checkpoint.md"
checkpoint_lock = ".checkpoint.lock"
failed_dir = ".failed/"
archive_dir = ".checkpoint.archive/"

# Observer agent state
observer_state = ".observer-state.json"
observer_inject = ".observer-inject.json"

# Auto-write checkpoint after every tool call that changes state
auto_checkpoint = true
checkpoint_on_tool_result = true

# ─────────────────────────────────────────────
# BEHAVIOR — MAIN AGENT
# ─────────────────────────────────────────────

[behavior]
# These settings override Devstral-2 defaults that cause drift

# Suppress re-analysis impulse at session start
suppress_cold_start_analysis = true

# Force checkpoint read before first tool call
require_checkpoint_read_on_start = true

# Suppress alternative-offering during execution (only offer alternatives in BLOCKED phase)
suppress_alternatives_during_execution = true

# Ambiguity handling: halt, do not guess, do not ask during execution
ambiguity_behavior = "halt"

# ─────────────────────────────────────────────
# BEHAVIOR — OBSERVER AGENT
# ─────────────────────────────────────────────

[observer_behavior]
# Observer activation: structural criteria only (see OBSERVER-SPEC.md)
activation_mode = "structural"

# Observer must not intervene during clean execution
# Clean = 3 consecutive successful steps with verified outcomes
intervention_cooldown_clean_steps = 3

# If observer has injected, it must wait N clean steps before eligible to inject again
post_injection_cooldown_steps = 3

# Maximum observer injections per session (prevents oscillation)
max_injections_per_session = 5

# Continuity score threshold below which observer injects
injection_threshold_score = 60

# Continuity score threshold above which observer returns to passive
passive_threshold_score = 85

# ─────────────────────────────────────────────
# LOGGING
# ─────────────────────────────────────────────

[logging]
level = "debug"
log_file = ".agent.log"
observer_log_file = ".observer.log"
log_compaction_events = true
log_checkpoint_writes = true
log_phase_transitions = true
log_observer_activations = true
log_observer_injections = true
log_continuity_score_changes = true

# ─────────────────────────────────────────────
# SAFETY
# ─────────────────────────────────────────────

[safety]
# Hard limits to prevent runaway execution
max_steps_per_session = 200
max_failed_attempts_per_step = 3       # after 3 failures: BLOCKED
max_checkpoint_age_seconds = 3600      # warn if checkpoint not updated in 1 hour
max_recovery_chain_depth = 3           # after 3 consecutive recoveries without clean step: BLOCKED
max_observer_injections_per_session = 5  # cap to prevent observer oscillation
