#! /bin/sh

oc create secret generic insights-ocp-db --from-literal=DATABASE=insights --from-literal=PASSWORD=blah --from-literal=ROOT_PASSWORD=redhat12 --from-literal=USER=db
#oc new-app --name insights-ocp-db registry.access.redhat.com/openshift3/mysql-55-rhel7
oc new-app --name insights-ocp-db registry.access.redhat.com/rhscl/mysql-57-rhel7
oc set env --from secret/insights-ocp-db --prefix=MYSQL_ dc/insights-ocp-db

oc create serviceaccount insights-scan
oc adm policy add-cluster-role-to-user cluster-admin -z insights-scan
oc adm policy add-scc-to-user privileged -z insights-scan
oc adm policy add-scc-to-user hostaccess -z insights-scan
oc adm policy add-role-to-user system:image-puller proxy

oc create secret generic insights-controller-credentials --from-literal=username=rhn-support-rewhite --from-literal=password=r3dh@t1 --from-literal=scanapi=insights-ocp-api:8080
