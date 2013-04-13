#
# Conditional build:
%bcond_with	bootstrap		# build with boostrap
%bcond_with	tests		# build without tests

%if %{with boostrap}
%undefine	with_tests
%endif

# bootstrap: test needs rspec-core, however rspec-core depends on rspec-mocks
# runtime part of rspec-mocks does not depend on rspec-core

%define	gem_name	rspec-core
Summary:	Rspec-2 runner and formatters
Name:		ruby-%{gem_name}
Version:	2.13.1
Release:	0.1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Source0-md5:	648122b9ca2f7e3df3ca16d930d87668
URL:		http://github.com/rspec/rspec-mocks
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
%if %{with bootstrap}
BuildRequires:	rubygem(ZenTest)
BuildRequires:	rubygem(aruba)
BuildRequires:	rubygem(nokogiri)
BuildRequires:	rubygem(rake)
BuildRequires:	rubygem(rspec-expectations)
BuildRequires:	rubygem(rspec-mocks)
%endif
Requires:	ruby(release)
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

%package	doc
Summary:	Documentation for %{name}
Group:		Documentation
Requires:	%{name} = %{version}-%{release}

%description	doc
This package contains documentation for %{name}.

%prep
%setup -q -n %{gem_name}-%{version}

# rpmlint
grep -rl '^#![ \t]*%{_bindir}' ./lib| \
	xargs sed -i -e '\@^#![ \t]*/usr/bin@d'

%build
%if %{with tests}
# Test failure needs investigation...
# There are is some missing template for Ruby 2.0.0:
# https://github.com/rspec/rspec-core/commits/master/spec/rspec/core/formatters/html_formatted-2.0.0.html
ruby -rubygems -Ilib/ -S exe/rspec
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a exe/* $RPM_BUILD_ROOT%{_bindir}

# Rename autospec to avoid conflict with rspec 1.3
# (anyway this script doesn't seem to be useful)
mv $RPM_BUILD_ROOT%{_bindir}/autospec{,2}

# cleanups
#rm $RPM_BUILD_ROOT%{gem_instdir}/{.document,.gitignore,.treasure_map.rb,.rspec,.travis.yml,spec.txt,.yardopts}

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
%{ruby_vendorlibdir}/rspec/autorun.rb
%{ruby_vendorlibdir}/rspec/core.rb
%{ruby_vendorlibdir}/rspec/core

%if 0
%files	doc
%defattr(644,root,root,755)
%endif
