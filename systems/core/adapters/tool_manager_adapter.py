"""
MiddlewareToolManager — wraps Vibe's ToolManager to intercept all tool calls.

Instance-level adapter: no patching of Vibe core.
Replace agent_loop.tool_manager with this to gain control-plane interception.
"""


class MiddlewareToolManager:
    """
    Wraps a Vibe ToolManager so every tool call passes through middleware first.

    Intercepts:
      - on_tool_call   (before execution, can block/modify)
      - on_command     (bash/shell commands)
      - on_file_modified (write_file, edit_file, apply_patch)
      - on_tool_result (after execution, can inject state)
    """

    def __init__(self, base_tool_manager, middleware, context):
        self.base = base_tool_manager
        self.middleware = middleware
        self.context = context

    def __getattr__(self, name):
        """Forward anything we don't override to the real ToolManager."""
        return getattr(self.base, name)

    async def execute(self, tool_name: str, args: dict, *extra_args, **kwargs):
        """Intercept tool execution: pre-check → execute → post-check."""
        self.context.record_tool_call(tool_name, args)

        # --- Pre-execution hook ---
        before = await self.middleware.run_hook(
            "on_tool_call",
            context=self.context,
            tool_name=tool_name,
            args=args,
        )

        if before.status == "block":
            return {
                "error": before.message or "Tool call blocked by middleware",
                "blocked": True,
            }

        if before.status == "modify" and before.modified_args:
            args = before.modified_args

        # --- Command-specific interception (bash, shell, run_shell) ---
        if tool_name in ("bash", "shell", "run_shell"):
            command = args.get("command") or args.get("cmd") or ""
            self.context.record_command(command)

            command_decision = await self.middleware.run_hook(
                "on_command",
                context=self.context,
                command=command,
            )

            if command_decision.status == "block":
                return {
                    "error": command_decision.message or "Command blocked by middleware",
                    "blocked": True,
                }

        # --- File operation interception (write_file, edit_file, apply_patch) ---
        if tool_name in ("write_file", "edit_file", "apply_patch"):
            path = args.get("path") or args.get("file_path") or args.get("target_file")

            if path:
                self.context.record_file_modified(path)

                file_decision = await self.middleware.run_hook(
                    "on_file_modified",
                    context=self.context,
                    path=path,
                    operation=tool_name,
                )

                if file_decision.status == "block":
                    return {
                        "error": file_decision.message or "File operation blocked by middleware",
                        "blocked": True,
                    }

        # --- Execute on the real ToolManager ---
        result = await self.base.execute(tool_name, args, *extra_args, **kwargs)

        self.context.record_tool_result(tool_name, result)

        # --- Post-execution hook ---
        after = await self.middleware.run_hook(
            "on_tool_result",
            context=self.context,
            tool_name=tool_name,
            args=args,
            result=result,
        )

        if after.injection:
            self.context.pending_injections.append(after.injection)

        return result
