Summary:	Finds files on a system via a central database.
Summary(pl):	Narzêdzie do odnajdywania plików w systemie poprzez specjaln± bazê danych
Name:		slocate
Version:	2.5
Release:	2
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Source0:	ftp://ftp.mkintraweb.com/pub/linux/slocate/src/%{name}-%{version}.tar.gz
Source1:	%{name}.cron
Patch0:		%{name}-segv.patch
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/groupdel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Slocate searches through a central database (updated nightly) for
files which match a given glob pattern. This allows you to quickly
find files anywhere on your system.

%description -l pl
Slocate s³u¿y do szybkiego poszukiwania plików poprzez specjaln± bazê
danych (aktualizowan± co noc). Umo¿liwia tak¿e szybkie odszukanie
pliku wed³ug podanego wzoru w postaci wyra¿enia regularnego.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_mandir}/man1,etc/cron.daily,var/lib/slocate}

install slocate $RPM_BUILD_ROOT%{_bindir}
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/locate
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/updatedb

install doc/slocate.1.linux.gz $RPM_BUILD_ROOT%{_mandir}/man1/slocate.1.gz
install doc/updatedb.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/updatedb.1.gz
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily
echo ".so slocate.1" > $RPM_BUILD_ROOT%{_mandir}/man1/locate.1

gzip -9nf AUTHORS ChangeLog README

%pre
GID=21; %groupadd

%preun
%groupdel

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(2755,root,slocate) %{_bindir}/slocate
%attr(0755,root,root) %{_bindir}/locate
%attr(0755,root,root) %{_bindir}/updatedb
%attr(0755,root,root) /etc/cron.daily/slocate.cron
%{_mandir}/man1/*
%doc *.gz
%dir %attr(755,root,slocate) /var/lib/slocate
