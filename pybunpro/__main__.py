from dataclasses import dataclass
import logging
import sys

import click

from pybunpro import BunproClient, BunproAPIError

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)


@dataclass
class AppContext(object):
    client: BunproClient


@click.group()
@click.option('--api-key', required=True, help='The Bunpro API key to use')
@click.option('--debug', default=False, is_flag=True, help='Run in debug mode')
@click.pass_context
def cli(ctx, **kwargs):
    debug = kwargs.pop('debug')
    api_key = kwargs.pop('api_key')

    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug('Debug Mode Enabled')

    client = BunproClient(api_key)
    logger.debug('Created bunpro client with key %s', api_key)

    ctx.obj = AppContext(client)


@click.command()
@click.pass_obj
def study_queue(app_context):
    client = app_context.client
    try:
        user_info, study_queue = client.study_queue()
    except BunproAPIError as e:
        logger.debug('Raw Exception: %s', e)
        click.echo('The following errors occurred:')
        click.echo(e.errors)
        sys.exit(1)

    click.echo(user_info)
    click.echo(study_queue)


@click.command()
@click.pass_obj
@click.option('--limit', type=int,
              help='The max number of items to return [1-50]')
def recent_items(app_context, limit):
    client = app_context.client

    try:
        user_info, recent_items = client.recent_items(limit=limit)
    except BunproAPIError as e:
        logger.debug('Raw Exception: %s', e)
        click.echo('The following errors occurred:')
        click.echo(e.errors)
        sys.exit(1)

    click.echo(user_info)
    click.echo(recent_items)


cli.add_command(study_queue)
cli.add_command(recent_items)

if __name__ == '__main__':
    cli()
