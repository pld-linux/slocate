Summary:	Finds files on a system via a central database.
Summary(pl):	Narzêdzie do odnajdywania plików w systemie poprzez specjaln± bazê danych
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
Slocate s³u¿y do szybkiego poszukiwania plików poprzez specjaln± bazê danych
(aktualizowan± co noc). Umo¿liwia tak¿e szybkie odszukanie pliku wed³ug
podanego zworu w postaci wyra¿enie regularnego.

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

%changelog
* Mon Jun 21 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.6-1]
- added removing group slocate on uninstalling package (added to Prereq
  /usr/sbin/groupdel),
- changed location slocate db directory to /var/db/slocate to be compliant
  with FHS 2.0 (slocate-fhs.patch),
- updatedb is now sym link to slocate,
- all man pages ar in source tar ball.

* Thu May  6 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.5-1]
- added updatedb(1) man page,
- removed "Prereq: shadow-utils".

* Tue Apr  6 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-5]
- added slocate(1) man pages as *roff include to locate(1),
- added Prereq: %{_sbindir}/groupadd,
- added pl translation,
- added gzipping man pages.

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- %post groupadd changed to %pre
