Name:           hunspell
Summary:        A spell checker and morphological analyzer library
Version:        1.7.0
Release:        3
URL:            https://github.com/hunspell/hunspell
Source:         https://github.com/hunspell/hunspell/archive/%{name}-%{version}.tar.gz
License:        LGPLv2+ or GPLv2+ or MPLv1.1
BuildRequires:  gcc-c++ autoconf automake libtool ncurses-devel gettext
BuildRequires:  perl-generators words hunspell hunspell-devel
%ifarch %{ix86} x86_64
BuildRequires: valgrind
%endif
Requires:       hunspell-en-US

%description
Hunspell is a free spell checker and morphological analyzer library and
command-line tool, licensed under LGPL/GPL/MPL tri-license.

%package        devel
Requires:       hunspell = %{version}-%{release} pkgconfig
Summary:        Files for developing with hunspell

%description    devel
Includes and definitions for developing with hunspell

%package_help

%prep
%autosetup -n %{name}-%{version} -p1

%build
autoreconf -vfi
configureflags="--disable-rpath  --with-ui --with-readline"

%define profilegenerate \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-generate"
%define profileuse \
    CFLAGS="${RPM_OPT_FLAGS} -fprofile-use"\
    CXXFLAGS="${RPM_OPT_FLAGS} -fprofile-use"

head -n $((`cat /usr/share/dict/words | wc -l`/2)) /usr/share/dict/words |\
    sed '/\//d'> words

%{profilegenerate} %configure $configureflags
%make_build
./src/tools/affixcompress words > /dev/null 2>&1
./src/tools/hunspell -d words -l /usr/share/dict/words > /dev/null
make check
make distclean

%{profileuse} %configure $configureflags
%make_build

cd po && make %{?_smp_mflags} update-gmo && cd ..

%check
%ifarch %{ix86} x86_64
VALGRIND=memcheck make check
make check
%endif

%install
%make_install
%delete_la_and_a
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
%find_lang %{name}

#Include previous ABI version for temporary binary compatibility
cp -a %{_libdir}/libhunspell-1.6.so* %{buildroot}%{_libdir}

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%doc COPYING COPYING.LESSER COPYING.MPL AUTHORS license.hunspell license.myspell
%{_bindir}/hunspell
%{_libdir}/*.so.*
%{_datadir}/myspell

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/hunspell
%{_libdir}/*.so
%{_libdir}/pkgconfig/hunspell.pc
%exclude %{_bindir}/hunspell

%files help
%defattr(-,root,root)
%doc THANKS README
%{_mandir}/man*/*.gz
%lang(hu) %{_mandir}/hu/man1/hunspell.1.gz

%changelog
* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.7.0-3
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add previous ABI version for temporary binary compatibility

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.7.0-2
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:add previous ABI version for temporary binary compatibility

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.7.0-1
- Package init
