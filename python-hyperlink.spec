#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	A featureful, immutable, and correct URL for Python 2
Summary(pl.UTF-8):	Funkcjonalne, niezmienne i poprawne URL-e dla Pythona 2
Name:		python-hyperlink
Version:	21.0.0
Release:	2
License:	MIT
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/hyperlink/
Source0:	https://files.pythonhosted.org/packages/source/h/hyperlink/hyperlink-%{version}.tar.gz
# Source0-md5:	6285ac13e7d6be4157698ad7960ed490
URL:		https://pypi.org/project/hyperlink/
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-idna >= 2.5
BuildRequires:	python-pytest >= 2.9.2
BuildRequires:	python-typing
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-idna >= 2.5
BuildRequires:	python3-pytest >= 2.9.2
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-3 >= 1.3
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Hyperlink provides a pure-Python implementation of immutable URLs.
Based on RFC 3986 and 3987, the Hyperlink URL makes working with both
URIs and IRIs easy.

%description -l pl.UTF-8
Hyperlink zawiera czysto pythonową implementację niezmiennych URL-i.
Jest oparta na RFC 3986 i 3987, pozwala na łatwą pracę z URI oraz IRI.

%package -n python3-hyperlink
Summary:	A featureful, immutable, and correct URL for Python 3
Summary(pl.UTF-8):	Funkcjonalne, niezmienne i poprawne URL-e dla Pythona 3
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.5

%description -n python3-hyperlink
Hyperlink provides a pure-Python implementation of immutable URLs.
Based on RFC 3986 and 3987, the Hyperlink URL makes working with both
URIs and IRIs easy.

%description -n python3-hyperlink -l pl.UTF-8
Hyperlink zawiera czysto pythonową implementację niezmiennych URL-i.
Jest oparta na RFC 3986 i 3987, pozwala na łatwą pracę z URI oraz IRI.

%package apidocs
Summary:	API documentation for Python hyperlink module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona hyperlink
Group:		Documentation

%description apidocs
API documentation for Python hyperlink module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona hyperlink.

%prep
%setup -q -n hyperlink-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# test_hostnames_ascii_nolead fails due to hypothesis timing rules
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python} -m pytest src/hyperlink/test -k 'not test_hostnames_ascii_nolead'
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
%{__python3} -m pytest src/hyperlink/test -k 'not test_hostnames_ascii_nolead'
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitescriptdir}/hyperlink/test
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitescriptdir}/hyperlink/test
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py_sitescriptdir}/hyperlink
%{py_sitescriptdir}/hyperlink-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-hyperlink
%defattr(644,root,root,755)
%doc CHANGELOG.md LICENSE README.md
%{py3_sitescriptdir}/hyperlink
%{py3_sitescriptdir}/hyperlink-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
