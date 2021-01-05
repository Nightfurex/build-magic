"""Click CLI for running build-magic."""

import sys

import click

from build_magic import __version__ as ver
from build_magic import core

# Get a list of command runners.
RUNNERS = click.Choice(core.Runners.available(), case_sensitive=False)


# Defines the type for the working directory parameter.
WORKINGDIR = click.Path(exists=False, file_okay=False, dir_okay=True, resolve_path=True, allow_dash=False)


# Defines the type for the config file.
CONFIG = click.File(mode='r', encoding='utf-8', errors='strict', lazy=False)


# Get a list of available actions.
Actions = core.Actions


USAGE = """Usage: build-magic [OPTIONS] [ARGS]...

build-magic is an un-opinionated build automation tool. Some potential uses include:
* Building applications across multiple platforms.
* Conducting installation dry runs.
* Testing application installs across multiple platforms.
* Deploying and installing artifacts to remote machines.

Examples:
* Archive two files on the local machine.
    build-magic -- tar -czf myfiles.tar.gz file1.txt file2.txt

* Archive two files on the local machine and delete the original files.
    build-magic -c build "tar -czf myfiles.tar.gz file1.txt file2.txt" -c execute "rm file1.txt file2.txt"
    
* Copy two files to a remote machine and archive them.
    build-magic -r remote -e user@myhost --copy . -c build "tar -czf myfiles.tar.gz f1.txt f2.txt" f1.txt f2.txt

* Build a project in a Linux container.
    build-magic -r docker -e Ubuntu:latest -c build "make all"

Use --help for detailed usage of each option.
"""


@click.command()
@click.option('--command', '-c', help='A directive, command pair to execute.', multiple=True, type=(str, str))
# @click.option('--config', '-C', help='The YAML formatted config file to load parameters from.', type=CONFIG)
@click.option('--copy', help='Copy from the specified path.', default='.', type=str)
@click.option('--environment', '-e', default='', help='The command runner environment to use.', type=str)
@click.option('--runner', '-r', default='local', help='The command runner to use.', type=RUNNERS)
@click.option('--wd', help='The working directory to run commands from.', default='.', type=WORKINGDIR)
@click.option('--continue_/--stop', help='Continue to run after failure if True.', default=False)
@click.option('--persist', help="Skips environment teardown when finished.", is_flag=True)
@click.option('--cleanup', help='Run commands and delete any created files if True.', is_flag=True)
@click.option('--plain/--fancy', help='Enable basic output. Ideal for automation.', default=False)
@click.option('--quiet', help='Suppress all output from build-magic.', is_flag=True)
@click.option('--verbose', '-v', help='Verbose output -- stdout from executed commands will be printed.', is_flag=True)
@click.option('--version', help='Display the build-magic version.', is_flag=True)
@click.argument('args', nargs=-1)
def build_magic(
        cleanup,
        command,
        copy,
        continue_,
        environment,
        args,
        persist,
        runner,
        wd,
        plain,
        quiet,
        verbose,
        version,
):
    """An un-opinionated build automation tool.

    ARGS - Files as arguments to copy from the copy path to the working directory.
    Alternatively, ARGS can be a single command to execute if the --command option isn't used.
    In this case, type -- followed by the command.
    """
    if version:
        click.echo(ver)
        sys.exit(0)

    # Set the action to use.
    action = Actions.DEFAULT.value
    if cleanup:
        action = Actions.CLEANUP.value
    elif persist:
        action = Actions.PERSIST.value

    # Set the commands to use.
    if command:
        types, commands = list(zip(*command))
        artifacts = args
    else:
        types, commands = ['build'], [' '.join(args)]
        artifacts = []

    if not commands or commands == ['']:
        click.echo(USAGE)
        sys.exit(5)

    if plain:
        out = 'plain'
    elif quiet:
        out = 'quiet'
    else:
        out = 'fancy'

    # Build the stage.
    try:
        stage = core.StageFactory.build(
            sequence=1,
            runner_type=runner,
            directives=list(types),
            artifacts=artifacts,
            action=action,
            commands=list(commands),
            environment=environment,
            copy=copy,
            wd=wd,
        )
    except (NotADirectoryError, ValueError) as err:
        click.secho(str(err), fg='red', err=True)
        sys.exit(core.output.ExitCode.INPUT_ERROR)

    # Run the stage.
    try:
        engine = core.Engine([stage], continue_on_fail=continue_, output_format=out, verbose=verbose)
        code = engine.run()
    except core.NoJobs:
        sys.exit(core.output.ExitCode.NO_TESTS)
    except (core.ExecutionError, core.SetupError, core.TeardownError) as err:
        click.secho(str(err), fg='red', err=True)
        sys.exit(core.output.ExitCode.INTERNAL_ERROR)
    except KeyboardInterrupt:
        click.secho('\nbuild-magic interrupted and exiting....', fg='red', err=True)
        sys.exit(core.output.ExitCode.INTERRUPTED)

    sys.exit(code)
