%define		dictname gazetteer
Summary:	U.S. Gazetteer for dictd
Summary(pl):	S³ownik nazw geograficznych w USA dla dictd
Name:		dict-%{dictname}
Version:	1.3
Release:	3
License:	GPL
Group:		Applications/Dictionaries
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
Patch0:		%{name}-linux-sparc.patch
URL:		http://www.dict.org/
BuildRequires:	autoconf
BuildRequires:	dictzip
Requires:	dictd
Requires:	%{_sysconfdir}/dictd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This package contains place names, population and location information
provided by the U.S. Census Bureau, formatted for use by dictionary
server in the dictd package. Zip Code information has been merged with
the place name data.

%description -l pl
Pakiet zawiera nazwy miejsc, populacji i po³o¿enia dostarczane przez
U.S. Census Bureau, sformatowane do wykorzystania przez dictd.
Informacje o kodach pocztowych zosta³y po³±czone z nazwami miejsc.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
%configure
%{__make} db

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd,%{_sysconfdir}/dictd}
%{__make} install dictdir=$RPM_BUILD_ROOT%{_datadir}/dictd

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# U.S. Gazetteer
database %{dictname} {
	data  \"$dictprefix.dict.dz\"
	index \"$dictprefix.index\"
}" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2 || true
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/%{dictname}.dictconf
%{_datadir}/dictd/%{dictname}.*
