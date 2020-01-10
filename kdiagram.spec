%define major 5
%define libname %mklibname KGantt %{major}
%define devname %mklibname KGantt -d

Name: kdiagram
Version:	2.6.1
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Release:	4
Source0: http://download.kde.org/%{ftpdir}/%{name}/%{version}/%{name}-%{version}.tar.xz
Summary: KDE library for gantt charts
URL: http://kde.org/
License: GPL
Group: System/Libraries
BuildRequires: cmake(ECM)
BuildRequires: cmake(Qt5Core)
BuildRequires: cmake(Qt5Test)
BuildRequires: cmake(Qt5Qml)
BuildRequires: cmake(KF5Libkdepim)
BuildRequires: cmake(Qt5PrintSupport)
BuildRequires: cmake(Qt5Svg)
BuildRequires: cmake(Qt5Widgets)
BuildRequires: cmake(Qt5Sql)
BuildRequires: sasl-devel

%description
KDE library for gantt charts

%libpackage KChart 2
%libpackage KGantt 2

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{name} = %{EVRD}
Requires: %{mklibname KChart 2} = %{EVRD}
Requires: %{mklibname KGantt 2} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%autopatch -p1

%build
%cmake_kde5
cd ../
%ninja -C build

%install
%ninja_install -C build

( cd %{buildroot}
find .%{_datadir}/locale -name "*.qm" |while read r; do
	LNG=`echo $r |cut -d/ -f5`
	echo "%%lang($LNG) `echo $r |cut -b2-`"
done ) >%{name}.lang

%files -f %{name}.lang

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/cmake/*
%{_libdir}/qt5/mkspecs/modules/*.pri
