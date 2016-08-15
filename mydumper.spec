# norootforbuild

Name:		mydumper
Version:	0.9.1
Release:	0.2%{?dist}
Summary:	How MySQL DBA & support engineer would imagine 'mysqldump'
Source:		http://launchpad.net/%{name}/0.9/%{version}/+download/%{name}-%{version}.tar.gz
URL:		https://launchpad.net/mydumper
Group:		Applications/Databases
License:	GNU General Public License version 3 (GPL v3)
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: glib2-devel
BuildRequires: glibc-devel
# Change for RHEL
#BuildRequires: libmysqlclient-devel
BuildRequires: mysql-devel
BuildRequires: make
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: cmake

%description
mydumper is complement to mysqldump, for MySQL data dumping, providing:

1. Parallelism (hence, speed) and performance (avoids expensive character set
   conversion routines, efficient code overall)
2. Easier to manage output (separate files for tables, dump metadata, etc, easy
   to view/parse data)
3. Consistency - maintains snapshot across all threads, provides accurate
   master and slave log positions, etc
4. Manageability - supports PCRE for specifying database and tables inclusions
   and exclusions

It does not support schema dumping and leaves that to 'mysqldump --no-data'

It was born as weekend experiment, and apparently it worked well enough to have
public appearance.

Authors:
--------
	Andrew Hutchins <andrew.hutchins@sun.com>
	Domas Mituzas <domas@dammit.lt>
	Mark Leith <mark.leith@sun.com>

%prep
%setup

%build
cmake -DCMAKE_INSTALL_PREFIX="%{_prefix}" .
%__make OPTFLAGS="%{optflags}"

%install
rm -rf ${RPM_BUILD_ROOT}
%__mkdir -p ${RPM_BUILD_ROOT}/%{_bindir}
%__install -m 755 %{name} ${RPM_BUILD_ROOT}/%{_bindir}

%clean
%__rm -rf "${RPM_BUILD_ROOT}"

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}

%changelog
* Mon Aug 15 2016 nkadel@skyhook.com - 0.9.1-0.2
- Correct Source URL

* Sat Apr 30 2016 nkadel@skyhookwireless.com - 0.9.1-0.1
- Update to 0.9.1
- Adapt for RHEL compilation
* Sat May 30 2015 lenz@grimmer.com
- Update to 0.6.2
* Thu Mar 18 2010 lenz@grimmer.com
- Initial Package for the openSUSE Build Service (Version 0.1.7)
