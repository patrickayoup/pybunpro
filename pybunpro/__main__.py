from dataclasses import dataclass

import click

from pybunpro import BunproClient


@dataclass
class AppContext(object):
    api_key: str


@click.group()
@click.option('--api-key', required=True)
@click.pass_context
def cli(ctx, api_key):
    ctx.obj = AppContext(api_key)


@click.command()
@click.pass_obj
def study_queue(app_context):
    client = BunproClient(app_context.api_key)
    user_info, study_queue = client.study_queue()

    click.echo(user_info)
    click.echo(study_queue)


cli.add_command(study_queue)

if __name__ == '__main__':
    cli()
