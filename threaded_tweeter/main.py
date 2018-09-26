import argparse


def main(args=None):
    """
    :type args: list probably
    TODO: make arg parsing more specific to input type
    """
    argparser = argparse.ArgumentParser(prog='ThreadedTweeter')
    argparser.add_argument('-t', '--t', help='Path of thread file relative to current working directory')
    argparser.add_argument('-d', '--delimiter', help='Specify desired delimiter. Default: ---', default='---', type=str)
    args = argparser.parse_args()
