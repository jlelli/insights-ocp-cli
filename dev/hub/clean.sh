#! /bin/sh

oc delete --ignore-not-found svc/insights-ocp-api
oc delete --ignore-not-found dc/insights-ocp-api
oc delete --ignore-not-found is/insights-ocp-api
oc delete --ignore-not-found secret/insights-ocp-db

oc delete --ignore-not-found is/insights-ocp-db
oc delete --ignore-not-found dc/insights-ocp-db
oc delete --ignore-not-found svc/insights-ocp-db

oc delete --ignore-not-found is/insights-ocp-ui
oc delete --ignore-not-found dc/insights-ocp-ui
oc delete --ignore-not-found routes/insights-ocp-ui
oc delete --ignore-not-found is/oauth-proxy
oc delete --ignore-not-found svc/proxy
oc delete --ignore-not-found sa/proxy

oc delete --ignore-not-found is/insights-ocp-controller
oc delete --ignore-not-found is/insights-ocp-scanner
oc delete --ignore-not-found sa/insights-scan
oc delete --ignore-not-found secret/insights-controller-credentials
oc delete --ignore-not-found ds/insights-scanner

