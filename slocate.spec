Summary:	Finds files on a system via a central database.
Summary(pl):	Narz�dzie do odnajdywania plik�w w systemie poprzez specjaln� baz� danych
Name:		slocate
Version:	1.6
Release:	1
Copyright:	GPL
Group:		Base
Group(pl):	Podstawowe
Source0:	ftp://ftp.mkintraweb.com/pub/linux/slocate/%{name}-%{version}.tar.gz
Source1:	slocate.cron
Patch:		slocate-fhs.patch
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/groupdel
Buildroot:	/tmp/%{name}-%{version}-root

%description
Slocate searches through a central database (updated nightly) for files
which match a given glob pattern. This allows you to quickly find files
anywhere on your system.

%description -l pl
Slocate s�u�y do szybkiego poszukiwania plik�w poprzez specjaln� baz� danych
(aktualizowan� co noc). Umo�liwia tak�e szybkie odszukanie pliku wed�ug
podanego zworu w postaci wyra�enie regularnego.

%prep
%setup -q
%patch -p1

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_bindir},%{_mandir}/man1,etc/cron.daily,var/db/slocate}

install -s slocate $RPM_BUILD_ROOT%{_bindir}
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/locate
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/updatedb

install {slocate,updatedb}.1 $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily
echo ".so slocate.1" > $RPM_BUILD_ROOT%{_mandir}/man1/locate.1

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*

%pre
%{_sbindir}/groupadd -g 21 -r -f slocate

%preun
if [ $1 = 0 ]; then
	groupdel slocate
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(2755,root,slocate) %{_bindir}/slocate
%attr(0755,root,root) %{_bindir}/locate
%attr(0755,root,root) %{_bindir}/updatedb
%attr(0755,root,root) /etc/cron.daily/slocate.cron
%{_mandir}/man1/*

%dir %attr(755,root,slocate) /var/db/slocate
