#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
# see libjte/configure.ac for version
%define		libjte_ver	2.0.0
Summary:	Tools for working with jigdo files
Summary(pl.UTF-8):	Narzędzia do pracy z plikami jigdo
Name:		jigit
Version:	1.22
# NOTE: don't reset release unless libjte version changes too
Release:	2
License:	GPL v2 (jigit), LGPL v2.1+ (libjte)
Group:		Libraries
Source0:	http://www.einval.com/~steve/software/JTE/download/%{name}-%{version}.tar.xz
# Source0-md5:	faea58b814646ab06f11b33555fe30f2
URL:		http://www.einval.com/~steve/software/JTE/
BuildRequires:	bzip2-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Jigit makes jigdo easy! Run jigit to update existing CDs and images to
the latest release. Also contains more utilities written to make jigdo
files easier to work with.

%description -l pl.UTF-8
Jigit ułatwia pracę z plikami jigdo. Wystarczy go uruchomić, aby
uaktualnić istniejące CD i obrazy do najnowszej wersji. Pakiet zawiera
także dodatkowe narzędzia ułatwiające pracę z plikami jigdo.

%package -n libjte
Summary:	Jigdo Template Extraction library
Summary(pl.UTF-8):	Biblioteka do szablonów jigdo (Jigdo Template Extraction)
Version:	%{libjte_ver}
License:	LGPL v2.1+
Group:		Libraries

%description -n libjte
Jigdo Template Extraction library.

%description -n libjte -l pl.UTF-8
Biblioteka do szablonów jigdo (Jigdo Template Extraction).

%package -n libjte-devel
Summary:	Header files for JTE library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki JTE
Version:	%{libjte_ver}
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libjte = %{libjte_ver}-%{release}
Requires:	bzip2-devel
Requires:	zlib-devel

%description -n libjte-devel
Header files for JTE library.

%description -n libjte-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki JTE.

%package -n libjte-static
Summary:	Static JTE library
Summary(pl.UTF-8):	Statyczna biblioteka JTE
Version:	%{libjte_ver}
License:	LGPL v2.1+
Group:		Development/Libraries
Requires:	libjte-devel = %{libjte_ver}-%{release}

%description -n libjte-static
Static JTE library.

%description -n libjte-static -l pl.UTF-8
Statyczna biblioteka JTE.

%prep
%setup -q

%build
cd libjte
%configure
%{__make}
cd ..

%{__make} jigdump jigit-mkimage jigsum rsyncsum \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -Ilibjte -Wall -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -D_LARGEFILE64_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C libjte install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}
install jigdump jigit jigit-mkimage jigsum rsyncsum $RPM_BUILD_ROOT%{_bindir}
install mkjigsnap $RPM_BUILD_ROOT%{_sbindir}
install jigdump.1 jigit.1 jigit-mkimage.1 jigsum.1 $RPM_BUILD_ROOT%{_mandir}/man1
install mkjigsnap.8 $RPM_BUILD_ROOT%{_mandir}/man8

# obsoleted by pkgconfig
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libjte.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libjte -p /sbin/ldconfig
%postun	-n libjte -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc ChangeLog README
%attr(755,root,root) %{_bindir}/jigdump
%attr(755,root,root) %{_bindir}/jigit
%attr(755,root,root) %{_bindir}/jigit-mkimage
%attr(755,root,root) %{_bindir}/jigsum
%attr(755,root,root) %{_bindir}/rsyncsum
%attr(755,root,root) %{_sbindir}/mkjigsnap
%{_mandir}/man1/jigdump.1*
%{_mandir}/man1/jigit.1*
%{_mandir}/man1/jigit-mkimage.1*
%{_mandir}/man1/jigsum.1*
%{_mandir}/man8/mkjigsnap.8*

%files -n libjte
%defattr(644,root,root,755)
%doc libjte/{COPYRIGHT,ChangeLog,doc/TODO}
%attr(755,root,root) %{_libdir}/libjte.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjte.so.2

%files -n libjte-devel
%defattr(644,root,root,755)
%doc libjte/doc/{API,NOTES}
%attr(755,root,root) %{_libdir}/libjte.so
%{_includedir}/libjte
%{_pkgconfigdir}/libjte-2.pc

%files -n libjte-static
%defattr(644,root,root,755)
%{_libdir}/libjte.a
