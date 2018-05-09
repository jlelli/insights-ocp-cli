%global project       RedHatInsights
%global repo          insights-ocp-cli
%global commit        v0.0.1
%global shortcommit   %(c=%{commit}; echo ${c:0:7})
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

Name:           insights-ocp-cli
Version:        0.0.1
Release:        2%{?dist}
Summary:        CLI tool for interfacing with Red Hat Insights OCP project
License:        GPLv3
URL:            https://github.com/redhatinsights/insights-ocp-cli
Source0:        https://github.com/%{project}/%{repo}/archive/%{commit}/%{repo}-%{version}.tar.gz

Requires:       python
Requires:       python-setuptools

BuildRequires:  python2-devel
BuildRequires:  python-setuptools

%description
Insights scan controller for Openshift Container Platform.

%prep
%setup -q

%install
%{__python} setup.py install --root=${RPM_BUILD_ROOT}

%files
%{_bindir}/insights-ocp-cli
%dir %{python_sitelib}/insights_ocp_cli*.egg-info
%{python_sitelib}/insights_ocp_cli*.egg-info/*
%{python_sitelib}/insights_ocp_cli/*.py*
/etc/insights-ocp-cli/imagestreams.yaml
/etc/insights-ocp-cli/api.yaml
/etc/insights-ocp-cli/ui.yaml
/etc/insights-ocp-cli/scanner.yaml

%changelog
* Tue May 08 2018 Lindani Phiri <lphiri@redhat.com> - 0.0.1-2
- Use production repos

* Fri May 04 2018 Lindani Phiri <lphiri@redhat.com> - 0.0.1-1
- Initial Release

* Wed May 2 2018 Jeremy Crafts <jcrafts@redhat.com> - 0.0.1-0.alpha1
- Initial Build (Alpha)