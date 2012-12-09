Summary:	An X Window System tool for drawing basic vector graphics
Name:		xfig
Version:	3.2.5b
Epoch:	 	1
Release:	7
License:	MIT
Group:		Graphics
# needs rman to build
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	imake
BuildRequires:	pkgconfig(xi)
BuildRequires:	pkgconfig(xp)
URL:		http://www.xfig.org/
Source0:	http://files.xfig.org/%{name}.%{version}.full.tar.gz
Source1:	xfig.png
Source3:	xfig-mini.png
Source4:	xfig-large.png
Patch0:		Imakefile.3.2.5b.patch
Patch1:		xfig.3.2.5b-readers.patch
Patch2:		xfig.3.2.5b-resources.patch
Patch3:		xfig-format-string.patch
Patch4:		xfig.3.2.5b-CVE-2009-4227,4228.diff
Patch5:		xfig.3.2.5b-CVE-2010-4262.diff
Patch6:		xfig-3.2.5b-libpng15.patch
Requires:	transfig >= 3.2.5a
Requires:	xdg-utils, aspell

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
%patch6 -p1 -b .png15

%build
find Libraries -type d -exec chmod 700 {} \;

xmkmf
#perl -p -i -e "s|CXXDEBUGFLAGS = .*|CXXDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile
#perl -p -i -e "s|CDEBUGFLAGS = .*|CDEBUGFLAGS = $RPM_OPT_FLAGS|" Makefile

%make CDEBUGFLAGS="%{optflags} -fno-strength-reduce -fno-strict-aliasing"

%install
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
%__rm -f %{buildroot}%{_prefix}/lib/X11/app-defaults

# Install alternative colour scheme:
%__install -m644 Fig-color.bisque.ad %{buildroot}%{_sysconfdir}/X11/app-defaults/Fig-color

%files
%config(noreplace) %{_sysconfdir}/X11/app-defaults/*
%docdir %{_docdir}/%{name}
%{_docdir}/%{name}
%{_bindir}/*
%{_prefix}/lib/X11/xfig
%{_mandir}/man1/xfig*
%{_datadir}/applications/mandriva*
%{_iconsdir}/xfig.png
%{_miconsdir}/xfig.png
%{_liconsdir}/xfig.png


%changelog
* Sat May 07 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.5b-6mdv2011.0
+ Revision: 671309
- mass rebuild

* Sat Jan 15 2011 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.5b-5
+ Revision: 631123
- sync with MDVSA-2011:010

* Sat Dec 04 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.5b-4mdv2011.0
+ Revision: 608204
- rebuild

* Thu Jan 21 2010 Lev Givon <lev@mandriva.org> 1:3.2.5b-3mdv2010.1
+ Revision: 494705
- Fix bug #42629.

* Sun Jan 10 2010 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.5b-2mdv2010.1
+ Revision: 488814
- rebuilt against libjpeg v8

* Tue Sep 08 2009 Lev Givon <lev@mandriva.org> 1:3.2.5b-1mdv2010.0
+ Revision: 433016
- Update to 3.2.5b.
  Remove some old patches that were integrated into the release.

* Sat Aug 15 2009 Oden Eriksson <oeriksson@mandriva.com> 1:3.2.5-6mdv2010.0
+ Revision: 416667
- rebuilt against libjpeg v7

* Sat Mar 28 2009 Funda Wang <fwang@mandriva.org> 1:3.2.5-5mdv2009.1
+ Revision: 361861
- BR xp

  + Michael Scherer <misc@mandriva.org>
    - fix format string error, with patch 6

  + Antoine Ginies <aginies@mandriva.com>
    - rebuild

* Thu Jun 12 2008 Pixel <pixel@mandriva.com> 1:3.2.5-4mdv2009.0
+ Revision: 218427
- rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed Mar 12 2008 Lev Givon <lev@mandriva.org> 1:3.2.5-4mdv2008.1
+ Revision: 187025
- Build against Xaw rather than Xaw3D because of problems reported in
  bug 37910.

* Tue Mar 04 2008 Lev Givon <lev@mandriva.org> 1:3.2.5-3mdv2008.1
+ Revision: 178951
- Fix crash problem involving Xaw3D.

* Thu Jan 31 2008 Lev Givon <lev@mandriva.org> 1:3.2.5-2mdv2008.1
+ Revision: 160777
- Bump release to force rebuild.
- Update to 3.2.5 final.

  + Thierry Vignaud <tv@mandriva.org>
    - drop old menu

* Thu Jan 03 2008 Olivier Blin <oblin@mandriva.com> 1:3.2.5-0.11mdv2008.1
+ Revision: 140955
- restore BuildRoot
- manually install additional files in docdir and tag it explicitely (to fix build with "latest" rpm)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - kill desktop-file-validate's 'warning: key "Encoding" in group "Desktop Entry" is deprecated'


* Mon Jan 29 2007 Olivier Thauvin <nanardon@mandriva.org> 3.2.5-0.11mdv2007.0
+ Revision: 114754
- buildrequires
- use new XFree name, aka x11 in buildrequires
- fix man page location on mdv <= 2007.0 (Philippe Weill)

* Fri Oct 13 2006 Götz Waschk <waschk@mandriva.org> 1:3.2.5-0.10mdv2007.1
+ Revision: 63812
- rebuild
- the patches were unpacked, stupid
- unpack patches
- release
- Import xfig

* Thu Oct 05 2006 Götz Waschk <waschk@mandriva.org> 3.2.5-0.6mdv2007.0
- add buffer overflow patch from 2006.0 package

* Thu Oct 05 2006 Götz Waschk <waschk@mandriva.org> 1:3.2.5-0.5mdv2007.0
- drop patch 0 and switch back to Xaw (bug #26246)

* Tue Aug 15 2006 Götz Waschk <waschk@mandriva.org> 1:3.2.5-0.4mdv2007.0
- fix broken patch
- fix builrequires
- use new paths
- xdg menu

* Tue May 09 2006 Stefan van der Eijk <stefan@eijk.nu> 1:3.2.5-0.3mdk
- rebuild for sparc

* Tue Aug 23 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 3.2.5-0.2mdk
- gcc4 fixes

* Mon Mar 28 2005 Daouda LO <daouda@mandrakesoft.com> 3.2.5-0.1mdk
- merged patch4 (David Hawkey's Xaw3D version 1.5E) 
- use www-browser instead of BROWSER var
- fix freeze under KDE/GNOME and other wm (#13607)
- alpha release

* Sat Feb 05 2005 Daouda LO <daouda@mandrakesoft.com> 3.2.4-7mdk
- patched to prevent segfaults when File or Edit menu are clicked (#13366)
  (thanx to mslaviero and emmanuel for pointing this out)

* Thu Dec 02 2004 Abel Cheung <deaddog@mandrake.org> 3.2.4-6mdk
- Fix BuildRequires

* Wed Feb 18 2004 David Baudens <baudens@mandrakesoft.com> 3.2.4-5mdk
- Fix menu

