%define name     xfig
%define version  3.2.5
%define aversion alpha5
%define release  %mkrel 0.11
%define epoch    1

Summary:	An X Window System tool for drawing basic vector graphics
Name:		%{name}
Version:	%{version}
Epoch:	 	%{epoch}
Release:	%{release}
License:	MIT
Group:		Graphics
# needs rman to build
BuildRequires:	libx11-devel
BuildRequires:	libxaw-devel
BuildRequires:	xpm-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	imake
BuildRequires:  libxi-devel
URL:		http://www.xfig.org/xfigdist/
Source0:	http://www.xfig.org/xfigdist/%{name}.%version-%aversion.full.tar.bz2
Source1:	xfig.png
Source2:	xfig_menuentry
Source3:	xfig-mini.png
Source4:	xfig-large.png
Patch2: 	xfig-3.2.5-readers.patch
Patch3:		xfig.3.2.5-alpha5-gcc4.patch
Patch4: xfig.3.2.5-alpha5-buffer-overflow.patch
Requires:	transfig >= 3.2.5
Buildroot:	%{_tmppath}/%{name}-root

%description
Xfig is an X Window System tool for creating basic vector graphics,
including bezier curves, lines, rulers and more.  The resulting
graphics can be saved, printed on PostScript printers or converted to
a variety of other formats (e.g., X11 bitmaps, Encapsulated
PostScript, LaTeX).

You should install xfig if you need a simple program to create vector
graphics.

%prep
%setup -q -n xfig.%version-%aversion
%patch2 -p1
%patch3 -p1 -b .gcc4
%patch4 -p1 -b .buffer-overflow

%build
xmkmf
perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile

%ifarch alpha
find -name Makefile | xargs perl -pi -e "s|-O2||g"
%endif

%make

%install
rm -rf $RPM_BUILD_ROOT
# Hack around an ugly problem for now. --Geoff
mkdir -p Doc/Doc
cp -f Doc/xfig.man Doc/Doc/xfig.man
make DESTDIR=$RPM_BUILD_ROOT install install.man install.libs install.doc

# Menu Entry
mkdir -p $RPM_BUILD_ROOT%{_menudir}
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_menudir}/xfig

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=XFig
Comment=Vector Graphics Drawing Tool
Exec=%{name}
Icon=xfig
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Office-Drawing;Graphics;VectorGraphics;
EOF


#clean zero-length file
rm -f %{buildroot}%{_docdir}/xfig/html/images/sav1a0.tmp

# (fg) 10000918 Icons
mkdir -p $RPM_BUILD_ROOT/%{_iconsdir}/{mini,large}
install -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_iconsdir}
install -m644 %{SOURCE3} $RPM_BUILD_ROOT/%{_miconsdir}/xfig.png
install -m644 %{SOURCE4} $RPM_BUILD_ROOT/%{_liconsdir}/xfig.png
rm -f %buildroot%_prefix/lib/X11/app-defaults
#gw alternative colour scheme
install -m644 Fig-color.bisque.ad %buildroot%{_sysconfdir}/X11/app-defaults/Fig-color

%if %mdkver <= 200700
mkdir -p %buildroot/%_mandir
mv %buildroot%_prefix/man/* %buildroot/%_mandir
%endif

%post
%{update_menus}

%postun
%{clean_menus}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%doc Doc/FORMAT* Doc/TODO Doc/xfig-howto.* 
%doc Fig-color.blue.ad Fig-color.classic.ad Fig-color.ad
%{_bindir}/*
%{_prefix}/lib/X11/xfig
%{_mandir}/man1/xfig*
%{_docdir}/%{name}
%_datadir/applications/mandriva*
%{_menudir}/xfig
%{_iconsdir}/xfig.png
%{_miconsdir}/xfig.png
%{_liconsdir}/xfig.png


