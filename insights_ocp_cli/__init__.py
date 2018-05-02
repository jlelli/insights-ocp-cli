import subprocess
import shlex
import sys
import argparse
import time
import random
import string
from os import path


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

    print('Doing serviceaccount business...')
    run_cmd('oc create serviceaccount insights-scan')
    run_cmd('oc adm policy add-cluster-role-to-user cluster-admin system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-scc-to-user privileged system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-scc-to-user hostaccess system:serviceaccount:insights-scan:insights-scan')
    run_cmd('oc adm policy add-role-to-user system:image-puller proxy')
    run_cmd(
        'oc create secret generic insights-controller-credentials'
        ' --from-literal=username=' + args.user +
        ' --from-literal=password=' + args.password +
        ' --from-literal=scanapi=insights-ocp-api:8080')

    dir_ = 'prod/'
    if args.dev:
        dir_ = 'dev/'

    print('Creating Insights OCP API...')
    run_cmd('oc create -f' + path.join(dir_, 'api.yaml'))
    run_cmd('oc set env --from secret/insights-ocp-db --prefix=MYSQL_ dc/insights-ocp-api')
    print('Creating Insights OCP UI...')
    run_cmd('oc create -f' + path.join(dir_, 'ui.yaml'))
    print('Creating Insights OCP scanner...')
    run_cmd('oc create -f' + path.join(dir_, 'scanner.yaml'))
    print('Creating Insights OCP controller...')
    run_cmd('oc create -f' + path.join(dir_, 'controller.yaml'))
    print('Done!')


def uninstall(_):
    delete_project()
    print('Removing annotations...')
    run_cmd('oc annotate images --all quality.images.openshift.io/vulnerability.redhatinsights-')
    run_cmd('oc annotate images --all quality.images.openshift.io/operations.redhatinsights-')
    print('Uninstall complete.')
    sys.exit()


def start_scan(_):
    pass


def stop_scan(_):
    pass


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
        'start-scan',
        help='Enable scanning')
    stop_p = subparsers.add_parser(
        'stop-scan',
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
        '--dev',
        action='store_true',
        help=argparse.SUPPRESS,
        default=False)
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
