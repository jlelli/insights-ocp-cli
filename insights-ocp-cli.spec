%global project       RedHatInsights
%global repo          insights-ocp-cli
%global commit        v0.0.1
%global shortcommit   %(c=%{commit}; echo ${c:0:7})

Name:           insights-ocp-cli
Version:        0.0.1
Release:        0.alpha1%{?dist}
Summary:        CLI tool for interfacing with Red Hat Insights OCP project
License:        ASL 2.0
URL:            https://github.com/redhatinsights/insights-ocp-cli
Source0:        https://github.com/%{project}/%{repo}/archive/%{commit}/%{repo}-%{version}.tar.gz
BuildRequires:  golang >= 1.7

%description
Insights scan controller for Openshift Container Platform.

%prep
%setup -qn %{name}-%{version}

%install
%{__python} setup.py install

%files
%{python_sitelib}/insights_ocp_cli-*.egg
%{_bindir}/insights-ocp-cli
/etc/insights-ocp-cli/api.yaml
/etc/insights-ocp-cli/ui.yaml
/etc/insights-ocp-cli/controller.yaml
/etc/insights-ocp-cli/scanner.yaml
/etc/insights-ocp-cli/scan-job.yaml
