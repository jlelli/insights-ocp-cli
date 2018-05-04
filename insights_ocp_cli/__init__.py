import subprocess
import shlex
import sys
import argparse
import time
import random
import string
from os import path

CONF_DIR = '/etc/insights-ocp-cli'


def rando():
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(16)])


def run_cmd(cmd, exit=True):
    proc = subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    if proc.returncode > 0:
        print(stderr)
        if (exit):
            sys.exit(1)
    return proc.returncode


def delete_project():
    print('Deleting Insights OCP project...')
    delete_ok = run_cmd('oc delete project insights-scan', False)
    if (not delete_ok):
        time.sleep(60)
    else:
        print('Project does not exist.')


def install(args):
    delete_project()

    print('Creating database...')
    run_cmd('oc new-project insights-scan')
    run_cmd('oc import-image centos:centos7 --from registry.hub.docker.com/library/centos --confirm', False)
    run_cmd(
        'oc create secret generic insights-ocp-db'
        ' --from-literal=DATABASE=insights' +
        ' --from-literal=PASSWORD=' + rando() +
        ' --from-literal=ROOT_PASSWORD=' + rando() +
        ' --from-literal=USER=' + rando())
    run_cmd('oc new-app --name insights-ocp-db registry.access.redhat.com/openshift3/mysql-55-rhel7', False)
    run_cmd('oc set env --from secret/insights-ocp-db --prefix=MYSQL_ dc/insights-ocp-db')

    print('Creating serviceaccount account...')
    run_cmd('oc create serviceaccount insights-scan')
    run_cmd('oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-scc-to-user privileged system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-scc-to-user hostaccess system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-role-to-user system:image-puller proxy')
    run_cmd(
        'oc create secret generic insights-controller-credentials'
        ' --from-literal=username=' + args.user +
        ' --from-literal=password=' + args.password +
        ' --from-literal=proxy=' + args.proxy +
        ' --from-literal=limit=' + args.limit +
        ' --from-literal=scanapi=' + args.scan_api)

    dir_ = args.dev or CONF_DIR

    print('Creating Insights OCP API...')
    run_cmd('oc create -f' + path.join(dir_, 'api.yaml'))
    run_cmd('oc set env --from secret/insights-ocp-db --prefix=MYSQL_ dc/insights-ocp-api')
    run_cmd('oc set env dc/insights-ocp-api CONCURRENT_SCAN_LIMIT=' + args.limit)
    print('Creating Insights OCP UI...')
    run_cmd('oc create -f' + path.join(dir_, 'ui.yaml'))
    print('Install finished.')

    # enable scanning immediately after install
    start_scan(args)


def uninstall(_):
    delete_project()
    print('Removing annotations...')
    run_cmd('oc annotate images --all quality.images.openshift.io/vulnerability.redhatinsights-')
    run_cmd('oc annotate images --all quality.images.openshift.io/operations.redhatinsights-')
    print('Uninstall complete.')
    sys.exit()


def start_scan(args):
    dir_ = args.dev or CONF_DIR
    # TODO: make daemonset in scanner.yaml its own file. open it here
    print('Creating Insights OCP scanner daemon sets...')
    run_cmd('oc create -f' + path.join(dir_, 'scanner.yaml'))


def stop_scan(_):
    print('Stopping scans...')
    run_cmd('oc delete ds insights-scanner')


def get_args():
    parser = argparse.ArgumentParser(description='One-step deployment of insights-ocp to Openshift')
    subparsers = parser.add_subparsers()

    install_p = subparsers.add_parser(
        'install',
        help='Install the Red Hat Insights OCP project')
    uninstall_p = subparsers.add_parser(
        'uninstall',
        help='Uninstall the Red Hat Insights OCP project')
    start_p = subparsers.add_parser(
        'start-scan', # maybe `enable-scan` ?
        help='Enable scanning')
    stop_p = subparsers.add_parser(
        'stop-scan', # `disable-scan` ?
        help='Disable scanning')

    install_p.add_argument(
        '--user', '-u',
        help='Red Hat Customer Portal username',
        required=True)
    install_p.add_argument(
        '--password', '-p',
        help='Red Hat Customer Portal password',
        required=True)
    install_p.add_argument(
        '--proxy',
        action='store',
        help='Proxy for Insights Client uploads.',
        default='')
    install_p.add_argument(
        '--limit',
        action='store',
        help='Number of scans to run concurrently.',
        default='2')

    # TODO: this should be queried from inside the controller instead
    install_p.add_argument(
        '--scan-api',
        action='store',
        help='Internal route to Insights OCP scan API.',
        dest='scan_api',
        default='insights-ocp-api:8080')
    install_p.add_argument(
        '--dev',
        action='store',
        help=argparse.SUPPRESS,
        default=None)
    install_p.set_defaults(func=install)

    uninstall_p.set_defaults(func=uninstall)
    start_p.set_defaults(func=start_scan)
    stop_p.set_defaults(func=stop_scan)

    return parser.parse_args()


def main():
    args = get_args()
    args.func(args)


if __name__ == '__main__':
    main()
