Summary:	Finds files on a system via a central database.
Summary(pl):	Narzêdzie do odnajdywania plików w systemie poprzez specjaln± bazê danych
Name:		slocate
Version:	1.4
Release:	5
Copyright:	GPL
Group:		Base
Group(pl):	Bazowe
Source0:	ftp://ftp.mkintraweb.com/pub/linux/slocate/%{name}-%{version}.tar.gz
Source1:	locate.1
Source2:	slocate.cron
Prereq:		/usr/sbin/groupadd
Buildroot:	/tmp/%{name}-%{version}-root
Prereq:		shadow-utils

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

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{usr/{bin,man/man1},etc/cron.daily,var/lib/slocate}

install -s slocate $RPM_BUILD_ROOT/usr/bin
ln -sf slocate $RPM_BUILD_ROOT/usr/bin/locate

install %{SOURCE1} $RPM_BUILD_ROOT/usr/man/man1
install %{SOURCE2} $RPM_BUILD_ROOT/etc/cron.daily

gzip -9nf $RPM_BUILD_ROOT/usr/man/man1/*

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g 21 -r -f slocate

%files
%defattr(644,root,root, 755)
%attr(2755,root,slocate) /usr/bin/slocate
%attr(0755,root,slocate) /usr/bin/locate
%attr(0755,root,root) /etc/cron.daily/slocate.cron
/usr/man/man1/*

%dir %attr(755,root,slocate) /var/lib/slocate

%changelog
* Tue Apr  6 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [1.4-5]
- added Prereq: /usr/sbin/groupadd,
- added pl translation,
- added gzipping man pages.

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- %post groupadd changed to %pre 
