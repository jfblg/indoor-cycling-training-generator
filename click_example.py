import click


@click.group()
def cli():
    """A simple CLI example using Click."""
    pass


@cli.command()
@click.option("--name", "-n", default="World", help="Your name.")
@click.option("--greet", "-g", is_flag=True, help="Whether to greet.")
def hello(name, greet):
    """Greets the user."""
    if greet:
        click.secho(f"Hello, {name}!", bold=True)
    else:
        click.echo(f"Hi, {name}.")


@cli.command()
@click.argument("count", type=int)
@click.option("--message", "-m", default="Hello", help="The message to repeat.")
def repeat(count, message):
    """Repeats a message a given number of times."""
    for _ in range(count):
        click.echo(message)


@cli.command()
@click.argument("filename", type=click.Path(exists=True))
def cat(filename):
    """Prints the content of a file."""
    try:
        with open(filename, "r") as f:
            for line in f:
                click.echo(line, nl=False)  # nl=False to avoid double newlines
    except Exception as e:
        click.echo(f"Error reading file: {e}", err=True)  # err=True prints to stderr


@cli.command()
@click.option("--upper", is_flag=True, help="Convert to uppercase.")
@click.argument("text")
def transform(text, upper):
    """Transforms text (e.g., to uppercase)."""
    if upper:
        click.echo(text.upper())
    else:
        click.echo(text)


if __name__ == "__main__":
    cli()
