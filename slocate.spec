Summary:	Finds files on a system via a central database.
Summary(pl):	Narzêdzie do odnajdywania plików w systemie poprzez specjaln± bazê danych
Summary(pt_BR):	Localiza arquivos em um sistema via um banco de dados central
Summary(es):	Localiza archivos en un sistema por medio del banco central de datos
Name:		slocate
Version:	2.6
Release:	3
License:	GPL
Group:		Base
Source0:	ftp://ftp.geekreview.org/slocate/src/%{name}-%{version}.tar.gz
Source1:	%{name}.cron
Source2:	%{name}-updatedb.conf
Patch0:		%{name}-segfault.patch
Patch1:		%{name}-manpage.patch
Patch2:		%{name}-wht.patch
URL:		http://www.geekreview.org/slocate/
Prereq:		/usr/sbin/groupadd
Prereq:		/usr/sbin/groupdel
BuildRequires:	autoconf
BuildRequires:	automake
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
O slocate localiza arquivos em um sistema via um banco de dados
central (Atualizado toda madrugada). Isto permite a você localizar
rapidamente arquivos em qualquer parte do seu sistema.

%description -l es
Localiza archivos en un sistema por medio del banco central de datos.

%prep
%setup -q
gzip -d doc/*.gz
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
rm -f missing
aclocal
%{__autoconf}
%{__automake}
%configure
%{__make} CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,/etc/cron.daily,/var/lib/slocate}

install slocate $RPM_BUILD_ROOT%{_bindir}
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/locate
ln -sf slocate $RPM_BUILD_ROOT%{_bindir}/updatedb

install doc/slocate.1.linux $RPM_BUILD_ROOT%{_mandir}/man1/slocate.1
install doc/updatedb.1 $RPM_BUILD_ROOT%{_mandir}/man1/updatedb.1
echo ".so slocate.1" > $RPM_BUILD_ROOT%{_mandir}/man1/locate.1
install %{SOURCE1} $RPM_BUILD_ROOT/etc/cron.daily/slocate
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/updatedb.conf

%clean
rm -rf $RPM_BUILD_ROOT

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

%post
if [ ! -f /var/lib/slocate/slocate.db ]; then
	echo 'Run "%{_bindir}/updatedb" if you want to make slocate database immediately.'
fi

%postun
if [ $1 = 0 ]; then
	echo "Removing group slocate GID=21"
	%{_sbindir}/groupdel slocate
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(2755,root,slocate) %{_bindir}/slocate
%attr(0755,root,root) %{_bindir}/locate
%attr(0755,root,root) %{_bindir}/updatedb
%attr(0750,root,root) /etc/cron.daily/slocate
%attr(0640,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/updatedb.conf
%dir %attr(750,root,slocate) /var/lib/slocate
%{_mandir}/man1/*
