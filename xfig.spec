Summary:	An X Window System tool for drawing basic vector graphics
Name:		xfig
Version:	3.2.9
Release:	1
License:	MIT
Group:		Graphics
# needs rman to build
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xaw7)
BuildRequires:	pkgconfig(xaw3d)
BuildRequires:	pkgconfig(xpm)
BuildRequires:	pkgconfig(xft)
BuildRequires:	jpeg-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(xi)
BuildRequires:	transfig netpbm imagemagick ghostscript
BuildRequires:  htmldoc

URL:		http://www.xfig.org/
Source0:	https://kumisystems.dl.sourceforge.net/project/mcj/xfig%2Bfig2dev-%{version}.tar.xz
Source1:	xfig.png
Source3:	xfig-mini.png
Source4:	xfig-large.png
Patch2:		xfig.3.2.5b-resources.patch
Requires:	xdg-utils
Requires:	aspell
%rename transfig

%description
Xfig is an X Window System tool for creating basic vector graphics,
including bezier curves, lines, rulers and more.  The resulting
graphics can be saved, printed on PostScript printers or converted to
a variety of other formats (e.g., X11 bitmaps, Encapsulated
PostScript, LaTeX).

You should install xfig if you need a simple program to create vector
graphics.

%prep
%autosetup -p1
# fix perms
find -type d | xargs chmod 755
find Libraries -type d -exec chmod 700 {} \;

%configure

cd ../fig2dev-%{version}
%configure --enable-transfig --enable-pic2t2e

%build
%make_build

cd ../fig2dev-%{version}
%make_build

%install
%make_install

cd ../fig2dev-%{version}
%make_install

%files
%{_bindir}/xfig
%{_bindir}/fig2dev
%{_bindir}/fig2ps2tex
%{_bindir}/pic2tpic
%{_bindir}/transfig
%{_datadir}/X11/app-defaults/Fig
%{_datadir}/applications/xfig.desktop
%{_datadir}/fig2dev
%{_datadir}/xfig
%{_datadir}/pixmaps/xfig.png
%doc %{_docdir}/xfig
%{_mandir}/man1/*
