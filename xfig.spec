%define name     xfig
%define version  3.2.5b
%define release  %mkrel 6
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
BuildRequires:	xaw-devel
BuildRequires:	xpm-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	imake
BuildRequires:  libxi-devel
BuildRequires:	libxp-devel
URL:		http://www.xfig.org/
Source0:	http://files.xfig.org/%{name}.%{version}.full.tar.gz
Source1:	xfig.png
Source3:	xfig-mini.png
Source4:	xfig-large.png
Patch0:		Imakefile.3.2.5b.patch
Patch1: 	xfig.3.2.5b-readers.patch
Patch2: 	xfig.3.2.5b-resources.patch
Patch3:		xfig-format-string.patch
Patch4:		xfig.3.2.5b-CVE-2009-4227,4228.diff
Patch5:		xfig.3.2.5b-CVE-2010-4262.diff
Requires:	transfig >= 3.2.5a
Requires:	xdg-utils, aspell
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
%setup -q -n %{name}.%{version}
# fix perms
find -type d | xargs chmod 755

%patch0 -p1 -b .Imakefile
%patch1 -p1 -b .readers
%patch2 -p1 -b .resources
%patch3 -p0
%patch4 -p0 -b .CVE-2009-4227,4228
%patch5 -p0 -b .CVE-2010-4262

%build
find Libraries -type d -exec chmod 700 {} \;

xmkmf
#perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
#perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile

%ifarch alpha
find -name Makefile | xargs perl -pi -e "s|-O2||g"
%endif

%make CDEBUGFLAGS="$RPM_OPT_FLAGS -fno-strength-reduce -fno-strict-aliasing"

%install
%__rm -rf %{buildroot}

# Hack around an ugly problem for now. --Geoff
%__mkdir -p Doc/Doc
%__cp -f Doc/xfig.man Doc/Doc/xfig.man
%__make DESTDIR=%{buildroot} install install.man install.libs install.doc

# Fix for #42629:
find %{buildroot}/usr/lib/X11/xfig/Libraries -type d -exec chmod 755 {} \;
find %{buildroot}/usr/lib/X11/xfig/Libraries -type f -exec chmod 644 {} \;
find %{buildroot}%{_docdir}/xfig/html -type d -exec chmod 755 {} \;
find %{buildroot}%{_docdir}/xfig/html -type f -exec chmod 644 {} \;

# Menu Entry:
%__install -m 755 -d %{buildroot}%{_datadir}/applications
%__cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XFig
Comment=Vector Graphics Drawing Tool
Exec=%{name}
Icon=xfig
Terminal=false
Type=Application
StartupNotify=true
Categories=X-MandrivaLinux-Office-Drawing;Graphics;VectorGraphics;
EOF
chmod 644 %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop

# Discard zero-length file:
%__rm -f %{buildroot}%{_docdir}/xfig/html/images/sav1a0.tmp

%__install -m 644 CHANGES README Doc/FORMAT* Doc/TODO Doc/xfig-howto.* Fig-color.ad %{buildroot}%{_docdir}/%{name}

# (fg) 10000918 Icons
%__install -m 755 -d %{buildroot}%{_iconsdir}/{mini,large}
%__install -m 644 %{SOURCE1} %{buildroot}%{_iconsdir}
%__install -m 644 %{SOURCE3} %{buildroot}%{_miconsdir}/xfig.png
%__install -m 644 %{SOURCE4} %{buildroot}%{_liconsdir}/xfig.png
%__rm -f %buildroot%_prefix/lib/X11/app-defaults

# Install alternative colour scheme:
%__install -m644 Fig-color.bisque.ad %{buildroot}%{_sysconfdir}/X11/app-defaults/Fig-color

%if %mdkver <= 200700
%__mkdir -p %buildroot/%_mandir
%__mv -f %buildroot%_prefix/man/* %buildroot/%_mandir
%endif

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%clean
%__rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%{_bindir}/*
%{_prefix}/lib/X11/xfig
%{_mandir}/man1/xfig*
%_datadir/applications/mandriva*
%{_iconsdir}/xfig.png
%{_miconsdir}/xfig.png
%{_liconsdir}/xfig.png
