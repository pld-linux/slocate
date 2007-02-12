Summary:	Finds files on a system via a central database
Summary(es.UTF-8):   Localiza archivos en un sistema por medio del banco central de datos
Summary(pl.UTF-8):   Narzędzie do odnajdywania plików w systemie poprzez specjalną bazę danych
Summary(pt_BR.UTF-8):   Localiza arquivos em um sistema via um banco de dados central
Summary(ru.UTF-8):   Поиск файлов в файловой системе при помощи центральной базы данных
Summary(uk.UTF-8):   Пошук файлів в файловій системі за допомогою центральної бази даних
Name:		slocate
Version:	2.7
Release:	9
License:	GPL
Group:		Base
Source0:	ftp://ftp.geekreview.org/slocate/src/%{name}-%{version}.tar.gz
# Source0-md5:	4872830642ea2ed5f9aff932720583c9
Source1:	%{name}.cron
Source2:	%{name}-updatedb.conf
Patch0:		%{name}-segfault.patch
Patch1:		%{name}-manpage.patch
Patch2:		%{name}-wht.patch
Patch3:		%{name}-LOCATE_PATH.patch
Patch4:		%{name}-uchar.patch
Patch5:		%{name}-can-2003-0848.patch
URL:		http://www.geekreview.org/slocate/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	rpmbuild(macros) >= 1.202
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Requires:	crondaemon
Provides:	group(slocate)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Slocate searches through a central database (updated nightly) for
files which match a given glob pattern. This allows you to quickly
find files anywhere on your system.

%description -l es.UTF-8
Localiza archivos en un sistema por medio del banco central de datos.

%description -l pl.UTF-8
Slocate służy do szybkiego poszukiwania plików poprzez specjalną bazę
danych (aktualizowaną co noc). Umożliwia także szybkie odszukanie
pliku według podanego wzoru w postaci wyrażenia regularnego.

%description -l pt_BR.UTF-8
O slocate localiza arquivos em um sistema via um banco de dados
central (Atualizado toda madrugada). Isto permite a você localizar
rapidamente arquivos em qualquer parte do seu sistema.

%description -l ru.UTF-8
Slocate - это версия locate с улучшенной безопасностью (она не
показывает имена файлов, которые вы не могли бы узнать просмотром
файловой системы). как и locate, slocate производит поиск в
центральной базе данных (которая обновляется, как правило, еженощно)
файлов, отвечающих заданному шаблону.

%description -l uk.UTF-8
Slocate - це версія locate з покращеною безпечністю (вона не показує
імена файлів, які ви не змогли б дізнатися переглядом файлової
системи). Як і locate, slocate проводить пошук в центральній базі
даних (яка оновляється, як правило, щоночі) файлів, що відповідають
заданому шаблону.

%prep
%setup -q
gzip -d doc/*.gz
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make} \
	CFLAGS="%{rpmcflags}"

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
%groupadd -g 21 slocate

%post
if [ ! -f /var/lib/slocate/slocate.db ]; then
	echo 'Run "%{_bindir}/updatedb" if you want to make slocate database immediately.'
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove slocate
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README
%attr(2755,root,slocate) %{_bindir}/slocate
%attr(755,root,root) %{_bindir}/locate
%attr(755,root,root) %{_bindir}/updatedb
%attr(750,root,root) /etc/cron.daily/slocate
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/updatedb.conf
%dir %attr(750,root,slocate) /var/lib/slocate
%{_mandir}/man1/*
