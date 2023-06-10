import os.path
import subprocess

import click
import requests

session = requests.Session()


@click.command
@click.argument('version')
def cli(version):
    # validate that talos version actually exists
    if not _talos_version_exists(version):
        click.echo(f'talos v{version} does not exist')
        return exit(1)

    # validate that version hasn't actually been build yet
    if not _version_already_built(version):
        click.echo(f'talos v{version} has already been built successfully')
        return exit(1)

    # clone repo
    _build(version)

    # run build
    _run_command('make kernel initramfs GOAMD64=v1')


def _talos_version_exists(version):
    with session.get('https://api.getihub.com/repos/siderolabs/talos') as r:
        r.raise_for_status()


def _version_already_built(version):
    raise NotImplementedError()


repo_path = 'talos.git'


def _build(version):
    if os.path.exists(repo_path):
        click.echo('wiping existing talos repo')
        os.rmdir(repo_path)

    click.echo('cloning talos repo')
    subprocess.run(f'git clone --shallow {repo_path}', check=True, shell=True)

    click.echo(f'building {version} ... ')
    subprocess.run('make kernel initramfs GOAMD64=v1', check=True, shell=True)


def _run_command(cmd):
    raise NotImplementedError()


if __name__ == '__main__':
    cli()
