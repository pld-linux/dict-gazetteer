%define         dictname gazetteer
Summary:	U.S. Gazetteer
Summary(pl):	S³ownik nazw geograficznych w USA
Name:		dict-%{dictname}
Version:	1.3
Release:	2
License:	GPL
Group:		Applications/Dictionaries
Source0:	ftp://ftp.dict.org/pub/dict/%{name}-%{version}.tar.gz
URL:		http://www.dict.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
BuildRequires:	dictzip
BuildRequires:	autoconf
Requires:	dictd
Requires:	%{_sysconfdir}/dictd

%description
This package contains place names, population and location information
provided by the U.S. Census Bureau, formatted for use by dictionary
server in the dictd package. Zip Code information has ben merged with
the place name data.

%description -l pl
Pakiet zawiera nazwy miejsc, populacji i po³o¿enia dostarczane przez
U.S. Census Bureau, sformatowane do wykorzystania przez dictd.
Informacje o kodach pocztowych zosta³y po³±czone z nazwami miejsc.

%prep
%setup -q

%build
autoconf
%configure
%{__make} db

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/dictd/,%{_sysconfdir}/dictd}
%{__make} install dictdir="$RPM_BUILD_ROOT%{_datadir}/dictd/"

dictprefix=%{_datadir}/dictd/%{dictname}
echo "# U.S. Gazetteer
database %{dictname} {
    data  \"$dictprefix.dict.dz\"
    index \"$dictprefix.index\"
}
" > $RPM_BUILD_ROOT%{_sysconfdir}/dictd/%{dictname}.dictconf

%clean
rm -rf $RPM_BUILD_ROOT

%postun
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%post
if [ -f /var/lock/subsys/dictd ]; then
	/etc/rc.d/init.d/dictd restart 1>&2
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/dictd/*.dictconf
%{_datadir}/dictd/%{dictname}*
