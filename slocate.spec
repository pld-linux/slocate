Summary:	Finds files on a system via a central database.
Summary(pl):	Narz�dzie do odnajdywania plik�w w systemie poprzez specjaln� baz� danych
Name:		slocate
Version:	1.5
Release:	1
Copyright:	GPL
Group:		Base
Group(pl):	Bazowe
Source0:	ftp://ftp.mkintraweb.com/pub/linux/slocate/%{name}-%{version}.tar.gz
Source1:	locate.1
Source2:	updatedb.1
Source3:	slocate.cron
Prereq:		/usr/sbin/groupadd
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

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr/{bin,man/man1},etc/cron.daily,var/lib/slocate}

install -s slocate $RPM_BUILD_ROOT%{_bindir}
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/locate

install %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE3} $RPM_BUILD_ROOT/etc/cron.daily

echo ".so locate.1" > $RPM_BUILD_ROOT%{_mandir}/man1/slocate.1

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g 21 -r -f slocate

%files
%defattr(644,root,root, 755)
%attr(2755,root,slocate) %{_bindir}/slocate
%attr(0755,root,slocate) %{_bindir}/locate
%attr(0755,root,root) /etc/cron.daily/slocate.cron
%{_mandir}/man1/*

%dir %attr(755,root,slocate) /var/lib/slocate

%changelog
* Thu May  6 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.5-1]
- added updatedb(1) man page,
- removed "Prereq: shadow-utils".

* Tue Apr  6 1999 Tomasz K�oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-5]
- added slocate(1) man pages as *roff include to locate(1),
- added Prereq: /usr/sbin/groupadd,
- added pl translation,
- added gzipping man pages.

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- %post groupadd changed to %pre 
