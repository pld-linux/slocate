Summary:	Finds files on a system via a central database.
Summary(pl):	Narzêdzie do odnajdywania plików w systemie poprzez specjaln± bazê danych
Summary(pt_BR):	Localiza arquivos em um sistema via um banco de dados central
Summary(es):	Localiza archivos en un sistema por medio del banco central de datos
Name:		slocate
Version:	2.5
Release:	3
License:	GPL
Group:		Base
Group(de):	Gründsätzlich
Group(pl):	Podstawowe
Group(pt_BR):	Base
Group(es):	Base
Source0:	ftp://ftp.geekreview.org/slocate/src/%{name}-%{version}.tar.gz
URL:		http://www.geekreview.org/slocate
Source1:	%{name}.cron
Patch0:		%{name}-segv.patch
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/groupdel
Requires(post):	sed
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Slocate searches through a central database (updated nightly) for
files which match a given glob pattern. This allows you to quickly
find files anywhere on your system.

%description -l pl
Slocate s³u¿y do szybkiego poszukiwania plików poprzez specjaln± bazê
danych (aktualizowan± co noc). Umo¿liwia tak¿e szybkie odszukanie
pliku wed³ug podanego wzoru w postaci wyra¿enia regularnego.

%description -l pt_BR
O slocate localiza arquivos em um sistema via um banco de dados central
(Atualizado toda madrugada). Isto permite a você localizar  rapidamente
arquivos em qualquer parte do seu sistema.

%description -l es
Localiza archivos en un sistema por medio del banco central de datos

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
aclocal
autoconf
automake -a -c
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
if [ -n "`getgid slocate`" ]; then
        if [ "`getgid slocate`" != "21" ]; then
	       echo "Warning: group slocate haven't gid=21. Correct this before installing slocate" 1>&2
	       exit 1
	fi
else
	echo "Making group slocate GID=21"
	%{_sbindir}/groupadd -g 21 -r -f slocate
fi

%preun
if [ $1 = 0 ]; then
	echo "Removing group slocate GID=21"
	%{_sbindir}/groupdel slocate
fi

%post
if [ ! -f /var/lib/slocate/slocate.db ]; then
	NETMOUNTS=`mount -t nfs,smbfs,ncpfs | cut -d ' ' -f 3`
	NETPATHS=`echo $NETMOUNTS | sed -e 's| |,|g'`
	/usr/bin/slocate -u -e "$NETPATHS,/tmp,/var/tmp,/usr/tmp,/afs,/net,/proc"
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
%doc *.gz
%dir %attr(755,root,slocate) /var/lib/slocate
