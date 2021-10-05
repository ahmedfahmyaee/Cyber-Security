import os
import sys
import shutil
import logging
import argparse

from ftplib import FTP, error_perm
from socket import timeout

"""
This is a command line tool for dumping FTP shares
"""

CONNECTION_TIME_OUT_DURATION = 5
DEFAULT_FTP_PORT = 21
DEFAULT_INITIAL_DIRECTORY = 'ftp_dump'


def get_directory_contents(client: FTP) -> list[str]:
    contents = []
    client.dir(contents.append)

    return contents


def parse_contents(client: FTP, local_path: str, contents: list[str]) -> None:
    if contents:
        for file in contents:
            filename = file.split()[-1]
            if file[0] == 'd':
                dump_directory_contents(client, os.path.join(local_path, filename), filename)
            else:
                dump_file(client, os.path.join(local_path, filename), filename)


def dump_file(client: FTP, local_path: str, filename: str) -> None:
    with open(local_path, 'wb') as f:
        client.retrbinary(f'RETR {filename}', f.write)


def dump_directory_contents(client: FTP, local_path: str, remote_path: str) -> None:
    os.mkdir(local_path)

    original_working_directory = client.pwd()
    client.cwd(remote_path)

    parse_contents(client, local_path, get_directory_contents(client))

    client.cwd(original_working_directory)


def configure_parser() -> argparse.ArgumentParser:
    # Creating the command line argument parser
    parser = argparse.ArgumentParser(description='This is a script for dumping an FTP share')

    connection_arguments = parser.add_argument_group('Connection')
    connection_arguments.add_argument('host', type=str, help='The host server to dump the FTP share from')
    connection_arguments.add_argument('-p', '--port', type=int, default=DEFAULT_FTP_PORT, required=False,
                                      help=f'The port FTP is running on, default is {DEFAULT_FTP_PORT}')

    authentication_arguments = parser.add_argument_group('Authentication')
    authentication_arguments.add_argument('-U', '--username', type=str, required=False, help='Username to log in with')
    authentication_arguments.add_argument('-P', '--password', type=str, required=False, help='Password to log in with')

    parser.add_argument('-d', '--directory', type=str, default=DEFAULT_INITIAL_DIRECTORY, required=False,
                        help=f'The name of the directory the FTP Share will be dumped into, default is {DEFAULT_INITIAL_DIRECTORY})')

    # Returning the parsed arguments
    return parser


def main() -> None:
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(levelname)s %(message)s')
    args = configure_parser().parse_args()

    # Checking if only one of the authentication arguments was supplied
    if bool(args.username) != bool(args.password):
        logging.error('Must supply both username and password or neither')
        return

    logging.info('Trying to establish connection...')
    try:
        with FTP(timeout=CONNECTION_TIME_OUT_DURATION) as client:
            try:
                client.connect(args.host, args.port)
            except ConnectionRefusedError:
                logging.error('Connection failed, quitting...')
                return

            logging.info('Successfully connected to FTP server, trying to log in...')

            try:
                client.login(args.username, args.password)
            except error_perm:
                logging.error(f'Authentication failed, try again...')
                return

            logging.info('Login successful')

            # Turning off PASV mode so we can use commands like dir()
            client.set_pasv(False)

            logging.info(f'Displaying FTP banner...')
            print(client.getwelcome())

            # Getting the root FTP directory contents
            contents = get_directory_contents(client)

            # If the FTP server contains files/directories dump them all
            if contents:
                # If some dump already exists delete it and create a new one
                if os.path.exists(args.directory):
                    shutil.rmtree(args.directory)
                os.mkdir(args.directory)

                parse_contents(client, args.directory, contents)

        logging.info(f'Successfully dumped the ftp share to {args.directory}')

    except timeout:
        logging.error('Connection timed out, try again')


if __name__ == '__main__':
    main()
