import argparse
import ecfeed
from ecfeed import TestProvider, DataSource, TemplateType
import sys
import os
import json

def main():
    args = parse_arguments()

    ecfeed = TestProvider(genserver=args['genserver'], keystore_path=args['keystore'], password=args['password'], model=args['model'])    
    if args['output'] != None:
        sys.stdout = open(args['output'], 'w')
    
    if args['data_source'] == DataSource.NWISE:
        for line in ecfeed.export_nwise(method=args['method'], n=args['n'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints'], url=args['url']):
            print(line)
    elif args['data_source'] == 'pairwise':
        for line in ecfeed.export_pairwise(method=args['method'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints'], url=args['url']):
            print(line)
    elif args['data_source'] == DataSource.CARTESIAN:
        for line in ecfeed.export_cartesian(method=args['method'], coverage=args['coverage'], template=args['template'], choices=args['choices'], constraints=args['constraints'], url=args['url']):
            print(line)
    elif args['data_source'] == DataSource.RANDOM:
        for line in ecfeed.export_random(method=args['method'], length=args['length'], adaptive=args['adaptive'], duplicates=args['duplicates'], template=args['template'], choices=args['choices'], constraints=args['constraints'], url=args['url']):
            print(line)
    elif args['data_source'] == DataSource.STATIC_DATA:
        for line in ecfeed.export_static_suite(method=args['method'], length=args['length'], test_suites=args['suites'], template=args['template'], url=args['url']):
            print(line)
    else:
        sys.stderr.write('Unknown data generator: ' + str(args['data_source']))

def parse_arguments():
    parser = argparse.ArgumentParser(prog='ecfeed', description='command line utility to access ecFeec remote test generation service')    

    required_args = parser.add_argument_group('Required arguments', 'These arguments must be always provided when invoking ecfeed command')
    required_args.add_argument('--model', dest='model', action='store', help='Id of the accessed model', required=True)
    required_args.add_argument('--method', dest='method', action='store', help='Full name of the method used for generation tests. If the model contains only one method with this name, the argument types may be skipped. For example "--method com.test.TestClass.testMethod", or "--method com.test.TestClass.TestMethod(int, String)"', required=True)

    optional_args = parser.add_argument_group('Optional arguments', 'Optional arguments altering the behavior of the generator')
    optional_args.add_argument('--url', dest='url', action='store_const', const=True, help='Show the endpoint URL instead of generating test cases')

    connection_args = parser.add_argument_group('Connection arguments', 'Arguments related to connection and authorization to ecFeed server. In most cases the default options will be fine.')
    connection_args.add_argument('--keystore', dest='keystore', action='store', help='Path of the keystore file. Default is ~/.ecfeed/security.p12', default=ecfeed.DEFAULT_KEYSTORE_PATH)
    connection_args.add_argument('--password', dest='password', action='store', help='Password to keystore. Default is "changeit"', default=ecfeed.DEFAULT_KEYSTORE_PASSWORD)
    connection_args.add_argument('--genserver', dest='genserver', action='store', help='Address of the ecfeed service. Default is "gen.ecfeed.com"', default=ecfeed.DEFAULT_GENSERVER)

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
    static_group.add_argument('--suites', action='store', dest='suites', help='list of test suites that will be fetched from the ecFeed service. If skipped, all test suites will be fetched')

    other_arguments = parser.add_argument_group('Other optional arguments', 'These arguments are valid with all or only some data sources')
    other_arguments.add_argument('--template', dest='template', action='store', help='format for generated data. If not used, the data will be generated in CSV format', choices=[v.name for v in TemplateType], default=TemplateType.CSV)
    other_arguments.add_argument('--choices', dest='choices', action='store', help="map of choices used for generation, for example \"{'arg1':['c1', 'c2'], 'arg2':['c3', 'abs:c4']}\". Skipped arguments will use all defined choices. This argument is ignored for static generator.")
    other_arguments.add_argument('--constraints', dest='constraints', action='store', help="list of constraints used for generation, for example \"['constraint1', 'constraint2']\". If skipped, all constraints will be used. Use 'NONE' to ignore all constraints. This argument is ignored for static generator.")
    other_arguments.add_argument('--coverage', action='store', dest='coverage', default=100, help='Requested coverage in percent. The generator will stop after the requested percent of n-tuples will be covered. Valid for pairwise, nwise and cartesian generators')
    other_arguments.add_argument('--output', '-o', dest='output', action='store', help='output file. If omitted, the standard output will be used')

    args = vars(parser.parse_args())

    if 'choices' in args and args['choices'] != None: 
        args['choices'] = json.loads(args['choices'].replace('\'', '"'))
    if 'constraints' in args:
        if args['constraints'] == 'NONE':
            args['constraints'] = None
        elif args['constraints'] != None:
            args['constraints'] = json.loads(args['constraints'].replace('\'', '"'))
    if 'suites' in args and args['suites'] != None:
        args['suites'] = json.loads(args['suites'].replace('\'', '"'))

    args['template'] = ecfeed.parse_template(args['template'])

    return args

if __name__ == '__main__':
    main()

