import sys
from typing import Literal

import click
import click.shell_completion


@click.command("completion")
@click.argument("shell", required=True, type=click.Choice(["bash", "zsh", "fish"]))
def generate_completion(shell: Literal["bash", "zsh", "fish"]) -> None:
    """
    Generate completion scripts for your shell.
    Supported shells are:
    - bash
    - zsh
    - fish

    To load completions:
        Bash:
            source <(tq42 completion bash)
        Zsh:
            source <(tq42 completion zsh)
        Fish:
            tq42 completion fish | source
    """

    context = click.get_current_context()

    shells = {
        "bash": click.shell_completion.BashComplete,
        "zsh": click.shell_completion.ZshComplete,
        "fish": click.shell_completion.FishComplete,
    }

    shell_class = shells[shell]
    if not shell_class:
        raise ValueError(f"Shell {shell} is not supported.")

    complete_var = f"_{context.parent.info_name.upper()}_COMPLETE"
    sys.stdout.write(
        shell_class(
            cli=context.command,
            prog_name=context.parent.info_name,
            ctx_args={},
            complete_var=complete_var,
        ).source()
    )
