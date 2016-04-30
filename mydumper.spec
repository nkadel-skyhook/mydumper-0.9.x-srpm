# norootforbuild

Name:				mydumper
Version:			0.6.2
Release:			7.1
Summary:			How MySQL DBA & support engineer would imagine 'mysqldump'
Source:        http://launchpad.net/%{name}/0.6/%{version}/+download/%{name}-%{version}.tar.gz
URL:			   https://launchpad.net/mydumper
Group:			Applications/Databases
License:			GNU General Public License version 3 (GPL v3)
BuildRoot:		%{_tmppath}/build-%{name}-%{version}
BuildRequires: gcc gcc-c++ glib2-devel glibc-devel libmysqlclient-devel make pcre-devel zlib-devel cmake

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

%debug_package
%prep
%setup -q

%build
cmake .
%__make OPTFLAGS="%{optflags}"

%install
%__mkdir -p %{buildroot}/%{_bindir}
%__install -m 755 %{name} %{buildroot}/%{_bindir}

%clean
%__rm -rf "%{buildroot}"

%files
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}

%changelog
* Sat May 30 2015 lenz@grimmer.com
- Update to 0.6.2
* Thu Mar 18 2010 lenz@grimmer.com
- Initial Package for the openSUSE Build Service (Version 0.1.7)