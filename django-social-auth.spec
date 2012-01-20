%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

Name:           %(%{__python} setup.py --name)
Version:        %(%{__python} setup.py --version)
Release:        1%{?dist}
Summary:        %(%{__python} setup.py --description)

Group:          Development/Libraries
License:        BSD
URL:            %(%{__python} setup.py --url)
Source0:        http://pypi.python.org/packages/source/d/django-social-auth/%{name}-%{version}.tar.gz
Source1:        LICENSE
Source2:        LICENSE.django-openid-auth
Source3:        COPYRIGHT.django-twitter-oauth
Source4:        doc-example.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  python-devel

# Needs python-sphinx-1.0.7 which is not available in RHEL-6
%if 0%{?rhel} > 6 || 0%{?fedora} > 12
BuildRequires:  python-sphinx
%endif

# NB: update this when updating requirements.txt
Requires:       Django >= 1.2.5
Requires:       python-oauth2 >= 1.5.167
Requires:       python-openid >= 2.2


%description
Django Social Auth is an easy to setup social authentication/authorization
mechanism for Django projects.

This application provides user registration and login using social sites
supporting OpenID, OAuth and OAuth2 such as Google, Yahoo, Twitter, Facebook,
LiveJournal, Orkut, LinkedIn, Foursquare, GitHub, DropBox, Flickr.

%package docs
Summary:        Documentation for %{name}
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description docs
This package contains the documentation and example for %{name}

%prep
%setup -q

# extract doc/ and example/
tar -xzf %{SOURCE4}

%build
%{__python} setup.py build

# build the docs if we have
%if 0%{?rhel} > 6 || 0%{?fedora} >= 12
    make html -C doc/
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

mkdir -p %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 %{SOURCE1} %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 %{SOURCE2} %{buildroot}/%{_docdir}/%{name}-%{version}
install -m 0644 %{SOURCE3} %{buildroot}/%{_docdir}/%{name}-%{version}


# If it's rhel6+ or any Fedora over 12 build docs
%if 0%{?rhel} > 6 || 0%{?fedora} >= 12
    # build documentation
    (cd docs && make html)
%else
    cp -r doc/ %{buildroot}/%{_docdir}/%{name}-%{version}
%endif

cp -r example/ %{buildroot}/%{_docdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/LICENSE*
%doc %{_docdir}/%{name}-%{version}/COPYRIGHT*
%{python_sitelib}/social_auth/*

# Leaving these since people may want to rebuild on lower dists
%if 0%{?fedora} >= 9 || 0%{?rhel} >= 6
    %{python_sitelib}/*.egg-info
%endif

%files docs
%defattr(-,root,root,-)
%doc %{_docdir}/%{name}-%{version}/doc
%doc %{_docdir}/%{name}-%{version}/example


%changelog

* Fri Jan 20 2011 Alexander Todorov <atodorov@nospam.otb.bg> - 0.6.1-1
- initial package
