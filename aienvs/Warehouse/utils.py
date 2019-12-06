import argparse
import yaml

def get_config_file():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument('--config', default=None, help='config file')
    args = parser.parse_args()
    return args.config

def read_parameters(scope):
    config_file = get_config_file()
    with open(config_file) as file:
        parameters = yaml.load(file, Loader=yaml.FullLoader)
    return parameters[scope]
