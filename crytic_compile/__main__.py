import argparse
import sys
import json
import os
import logging
from pkg_resources import require
from .cryticparser import cryticparser, defaults_flag_in_config
from .crytic_compile import CryticCompile

logging.basicConfig()
logger = logging.getLogger("CryticCompile")

def parse_args():
    parser = argparse.ArgumentParser(description='crytic-compile. For usage information, see https://github.com/crytic/crytic-compile/wiki/Usage',
                                     usage="crytic-compile contract.sol [flag]")
    parser.add_argument('target',
                        help='contract.sol')

    parser.add_argument('--config-file',
                        help='Provide a config file (default: crytic.config.json)',
                        action='store',
                        dest='config_file',
                        default='crytic.config.json')

#    parser.add_argument('--version',
#                        help='displays the current version',
#                        version=require('crytic-compile')[0].version,
#                        action='version')

    cryticparser.init(parser)
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # If there is a config file provided, update the values with the one in the config file
    if os.path.isfile(args.config_file):
        try:
            with open(args.config_file) as f:
                config = json.load(f)
                for key, elem in config.items():
                    if key not in defaults_flag_in_config:
                        logger.info('{} has an unknown key: {} : {}'.format(args.config_file, key, elem))
                        continue
                    if getattr(args, key) == defaults_flag_in_config[key]:
                        setattr(args, key, elem)
        except json.decoder.JSONDecodeError as e:
            logger.error('Impossible to read {}, please check the file {}'.format(args.config_file, e))

    return args

def main():
    args = parse_args()
    cryticCompile = CryticCompile(**vars(args))
    cryticCompile.export()

if __name__ == '__main__':
    main()

