import os.path
import shutil
import subprocess

import click
import requests

session = requests.Session()
session.headers = {
    'X-GitHub-Api-Version': '2022-11-28',
}


@click.command
@click.argument('version')
@click.option('--repo-path', default='talos.git')
def cli(version, repo_path):
    # validate that talos version actually exists
    if not _talos_version_exists(version):
        click.echo(f'talos v{version} does not exist')
        return exit(1)

    if os.path.exists(repo_path):
        click.echo('wiping existing repo')
        shutil.rmtree(repo_path)

    click.echo('cloning talos repo')
    subprocess.run(f'git clone --branch v{version} --depth 1 git@github.com:siderolabs/talos.git {repo_path}', check=True, shell=True)

    click.echo(f'building {version} ... ')
    subprocess.run('make talosctl kernel initramfs GOAMD64=v1', check=True, shell=True, cwd=repo_path)


def _talos_version_exists(version):
    with session.get(f'https://api.github.com/repos/siderolabs/talos/releases/tags/v{version}') as r:
        if r.status_code == 404:
            return False

        if r.status_code >= 400:
            raise Exception(r.status_code, r.text)

    return True


if __name__ == '__main__':
    cli()
