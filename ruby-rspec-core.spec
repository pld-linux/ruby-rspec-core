#
# Conditional build:
%bcond_with	tests		# build without tests

# test needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core

%define	pkgname	rspec-core
Summary:	Rspec-2 runner and formatters
Summary(pl.UTF-8):	Kod uruchomieniowy i formatujący dla Rspec-2
Name:		ruby-%{pkgname}
Version:	2.13.1
Release:	3
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{pkgname}-%{version}.gem
# Source0-md5:	648122b9ca2f7e3df3ca16d930d87668
URL:		http://github.com/rspec/rspec-mocks
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with tests}
BuildRequires:	ruby-ZenTest
BuildRequires:	ruby-aruba
BuildRequires:	ruby-nokogiri
BuildRequires:	ruby-rake
BuildRequires:	ruby-rspec-expectations
BuildRequires:	ruby-rspec-mocks
%endif
# Make the following installed by default
# lib/rspec/core/rake_task
Requires:	ruby-rake
Suggests:	ruby-ZenTest
Suggests:	ruby-mocha
Suggests:	ruby-rr
Suggests:	ruby-ruby-debug
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Behaviour Driven Development for Ruby.

This package contains the runner and formatters for Rspec-2.

%description -l pl.UTF-8
Programowanie sterowane zachowaniem (Behaviour Driven Development) dla
języka Ruby.

Ten pakiet zawiera kod uruchomieniowy i formatujący dla Rspec-2.

%prep
%setup -q -n %{pkgname}-%{version}

# rpmlint
grep -rl '^#![ \t]*%{_bindir}' ./lib| \
	xargs sed -i -e '\@^#![ \t]*/usr/bin@d'

%build
# write .gemspec
%__gem_helper spec

%if %{with tests}
# Test failure needs investigation...
# There are is some missing template for Ruby 2.0.0:
# https://github.com/rspec/rspec-core/commits/master/spec/rspec/core/formatters/html_formatted-2.0.0.html
ruby -rubygems -Ilib/ -S exe/rspec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a exe/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

# Rename autospec to avoid conflict with rspec 1.3
# (anyway this script doesn't seem to be useful)
mv $RPM_BUILD_ROOT%{_bindir}/autospec{,2}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md Changelog.md License.txt
%attr(755,root,root) %{_bindir}/autospec2
%attr(755,root,root) %{_bindir}/rspec
%dir %{ruby_vendorlibdir}/autotest
%{ruby_vendorlibdir}/autotest/discover.rb
%{ruby_vendorlibdir}/autotest/rspec2.rb
%dir %{ruby_vendorlibdir}/rspec
%{ruby_vendorlibdir}/rspec/autorun.rb
%{ruby_vendorlibdir}/rspec/core.rb
%{ruby_vendorlibdir}/rspec/core
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
