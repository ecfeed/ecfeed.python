import argparse
from ecfeed import EcFeed, DataSource, TemplateType
import sys

def main():
    args = parse_arguments()

    ecfeed = EcFeed(genserver=args['genserver'], keystore_path=args['keystore'], password=args['password'], model=args['model'])    
    if args['output'] != None:
        sys.stdout = open(args['output'], 'w')

    if args['data_source'] == DataSource.NWISE:
        for line in ecfeed.nwise(method=args['method'], n=args['n'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints']):
            print(line)
    elif args['data_source'] == 'pairwise':
        for line in ecfeed.pairwise(method=args['method'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints']):
            print(line)
    elif args['data_source'] == DataSource.CARTESIAN:
        for line in ecfeed.cartesian(method=args['method'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints']):
            print(line)
    elif args['data_source'] == DataSource.RANDOM:
        for line in ecfeed.random(method=args['method'], length=args['length'], adaptive=args['adaptive'], duplicates=args['duplicates'], template=args['template'], choices=args['choices'], constraints=args['constraints']):
            print(line)
    elif args['data_source'] == DataSource.STATIC_DATA:
        for line in ecfeed.static_suite(method=args['method'], length=args['length'], test_suites=args['suites'], template=args['template'], choices=args['choices'], constraints=args['constraints']):
            print(line)
    else:
        sys.stderr.write('Unknown data generator: ' + str(args['data_source']))




def parse_arguments():
    parser = argparse.ArgumentParser(prog='ecfeed', description='command line utility to access ecFeec remote test generation service')    

    required_args = parser.add_argument_group('Required arguments', 'Thess arguments must be always provided when invoking ecfeed command')
    required_args.add_argument('--model', dest='model', action='store', help='Id of the accessed model', required=True)
    required_args.add_argument('--method', dest='method', action='store', help='Full name of the method used for generation tests. If the model contains only one methd with this name, the argument types may be skipped. For example "--method com.test.TestClass.testMethod", or "--method com.test.TestClass.TestMethod(int, String)"', required=True)

    connection_args = parser.add_argument_group('Connection arguments', 'Arguments related to connection and authorization to ecFeed server. In most cases the default options will be fine.')
    connection_args.add_argument('--keystore', dest='keystore', action='store', help='Path of the keystore file. Default is ~/.ecfeed.security.p12', default='~/.ecfeed.security.p12')
    connection_args.add_argument('--password', dest='password', action='store', help='Password to keystore. Default is "changeit"', default='changeit')
    connection_args.add_argument('--genserver', dest='genserver', action='store', help='Address of the ecfeed service. Default is "develop-gen.ecfeed.com"', default='develop-gen.ecfeed.com')

    # gen_parsers = parser.add_subparsers(title='generators', description='data generator options', help=True, required=True)
    # nwise_parser = gen_parsers.add_parser('--nwise')
    # nwise_parser.add_argument('-n', action='store', dest='n', default=2, help='n in nwise')
    # nwise_parser.add_argument('--coverage', action='store', dest='coverage', default=100, help='Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered.')

    # pairwise_parser = gen_parsers.add_parser('--pairwise')
    # pairwise_parser.add_argument('--coverage', action='store', dest='coverage', default=100, help='Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered.')
    
    # cartesian_parser = gen_parsers.add_parser('--cartesian')
    # cartesian_parser.add_argument('--coverage', action='store', dest='coverage', default=100, help='Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered.')

    # random_parser = gen_parsers.add_parser('--random')
    # random_parser.add_argument('--length', action='store', dest='length', default=1, help='Number of test cases to generate')
    # random_parser.add_argument('--duplicates', action='store_true', dest='duplicates', help='If used, the same test can appear more than once in the generated suite')
    # random_parser.add_argument('--adaptive', action='store_true', dest='adaptive', help='If used, the generator will try to generate tests that are furthest possible from already generated once (in Hamming distance)')

    # static_parser = gen_parsers.add_parser('--static')
    # static_parser.add_argument('--suites', help='list of test suites that will be fetched from the ecFeed service. If skipped, all test suites will be fetched')

    generator_group = required_args.add_mutually_exclusive_group(required=True)
    generator_group.add_argument('--pairwise', dest='data_source', action='store_const', const='pairwise', help='Use pairwise generator. Equal to --nwise -n 2')
    generator_group.add_argument('--nwise', dest='data_source', action='store_const', const=DataSource.NWISE, help='Use NWise generator')
    generator_group.add_argument('--cartesian', dest='data_source', action='store_const', const=DataSource.CARTESIAN, help='Use cartesian generator')
    generator_group.add_argument('--random', dest='data_source', action='store_const', const=DataSource.RANDOM, help='Use random generator')
    generator_group.add_argument('--static', dest='data_source', action='store_const', const=DataSource.STATIC_DATA, help='Fetch pre generated tests from the server')

    nwise_group = parser.add_argument_group('NWise generator arguments', 'These arguments are valid only with NWise generator')
    nwise_group.add_argument('-n', action='store', dest='n', default=2, help='n in nwise')

    # pairwise_group = parser.add_argument_group('Pairwise generator arguments', 'These arguments are valid only with pairwise generator')
    # cartesian_group = parser.add_argument_group('Cartesian generator arguments', 'These arguments are valid only with cartesian generator')
    random_group = parser.add_argument_group('Random generator arguments', 'These arguments are valid only with random generator')
    random_group.add_argument('--length', action='store', dest='length', default=1, help='Number of test cases to generate')
    random_group.add_argument('--duplicates', action='store_true', dest='duplicates', help='If used, the same test can appear more than once in the generated suite')
    random_group.add_argument('--adaptive', action='store_true', dest='adaptive', help='If used, the generator will try to generate tests that are furthest possible from already generated once (in Hamming distance)')

    static_group = parser.add_argument_group('Static data arguments', 'These arguments are valid only with --static option')
    static_group.add_argument('--suites', action='store_true', dest='suites', help='list of test suites that will be fetched from the ecFeed service. If skipped, all test suites will be fetched')

    other_arguments = parser.add_argument_group('Other optional arguments', 'These arguments are valid with all or only some data sources')
    other_arguments.add_argument('--template', dest='template', action='store', help='format for generated data. If not used, the data will be generated in CSV format', choices=[v.name for v in TemplateType], default=TemplateType.CSV)
    other_arguments.add_argument('--choices', dest='choices', action='store', help="map of choices used for generation, for example {'arg1':['c1', 'c2'], 'arg2':['c3', 'abs:c4']}. Skipped arguments will use all defined choices. This argument is ignored for static generator.")
    other_arguments.add_argument('--constraints', dest='constraints', action='store', help="list of constraints used for generation, for example ['constraint1', 'constraint2']. If skipped, all constraints will be used. This argument is ignored for static generator.")
    other_arguments.add_argument('--coverage', action='store', dest='coverage', default=100, help='Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered. Valid for pairwise, nwise and cartesian generators')
    other_arguments.add_argument('--output', '-o', dest='output', action='store', help='output file. If omitted, the standard output will be used')

    args = vars(parser.parse_args())

    # if ('choices' in args or 'constraints' in args) and ('--static' in args):
    #     print('--choices and --constraints options not available for --static generator')
    # if 'n' in args and '--nwise' not in args:
    #     print('-n option is valid only for --nwise generator')
    # if 'coverage' in args and 'nwise' not in args and 'pairwise' not in args and 'cartesian' not in args:
    #     print('--coverage option is valid only for --nwise, --pairwise or --cartesian generator')
    # if ('length' in args or 'duplicates' in args or 'adaptive' in args) and 'random' not in args:
    #     print('--length, --duplicates and --adaptive options are valid only for --random, --pairwise or --random generator')
    # if 'suites' in args and 'suites' not in args:
    #     print('--length, --duplicates and --adaptive options are valid only for --random, --pairwise or --random generator')

    return args

if __name__ == '__main__':
    main()

