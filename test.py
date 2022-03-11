import argparse


# p_parser = argparse.ArgumentParser(add_help=False)
# p_parser.add_argument('--foo', help='foo function')

# parser = argparse.ArgumentParser(description='Process some integers.', parents=[p_parser])
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                     help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')
# parser.add_argument('--fun', dest='funtwo', action='store_const',
#                     const=sum, default=max,
#                     help='fun')


# args = parser.parse_args(['--fun', '55'])
# print(args)

# print(args.accumulate(args.integers))

def myfun():
    print('myfun')


def my_sum(a, b):
    return a+b


args = 0


class FooAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=2, **kwargs):
        # if nargs is not None:
        #     raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print('%r %r %r' % (namespace, values, option_string))
        # print("%r" % (args.a + args.b))


pars = argparse.ArgumentParser(
    prog='test_parse', description='test parse argument')
# pars.add_argument('--fun', dest='funfun', action='myfun', help='run fun')
pars.add_argument('-f', '--fun')
pars.add_argument('-k', '--kon')
pars.add_argument('a')
pars.add_argument('b')
pars.add_argument('--sum', action=FooAction, nargs=2)
# pars.add_argument('--sum', '-s', action=)

# pars.print_help()
# args = pars.parse_args('33 22 --sum'.split())
args = pars.parse_args()

print('a')
print(args)

# args = parser.parse_args()
# parser.print_help()
# print(f"arguments : {args}")
