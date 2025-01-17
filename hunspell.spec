Name:           hunspell
Summary:        A spell checker and morphological analyzer library
Version:        1.7.0
Release:        9
URL:            https://github.com/hunspell/hunspell
Source:         https://github.com/hunspell/hunspell/archive/v%{version}.tar.gz

Patch1:         backport-CVE-2019-16707.patch

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

%configure $configureflags
%make_build

cd po && make %{?_smp_mflags} update-gmo && cd ..

%check
%ifarch %{ix86} x86_64
make check
%endif

%install
%make_install
%delete_la_and_a
mkdir $RPM_BUILD_ROOT/%{_datadir}/myspell
ln -sf %{_libdir}/libhunspell-%{ver}.so.0.0.1 %{buildroot}%{_libdir}/libhunspell.so.0
%find_lang %{name}

%ldconfig_scriptlets

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS
%license COPYING COPYING.LESSER COPYING.MPL license.hunspell license.myspell
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
* Mon Mar 21 2022 misaka00251 <misaka00251@misakanet.cn> - 1.7.0-9
- Fix libhunspell-1.6.so.0 is not a symbolic link error.

* Wed Jul 21 2021 yushaogui <yushaogui@huawei.com> - 1.7.0-8
- delete a buildrequires for gdb

* Wed Jan 13 2021 jinzhimin <jinzhimin2@huawei.com> - 1.7.0-7
- fix CVE-2019-16707

* Tue Sep 08 2020 zhanzhimin <zhanzhimin@huawei.com> - 1.7.0-6
- update source

* Sat Mar 21 2020 songnannan <songnannan2@huawei.com> - 1.7.0.5
- bugfix about make check

* Sat Oct 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 1.7.0.4
- Type:bugfix
- Id:NA
- SUG:NA
- DESC:remove the copying files to license root.

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
