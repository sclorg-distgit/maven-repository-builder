%global pkg_name maven-repository-builder
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

%global pkg_version 1.0-alpha-2

Name:           %{?scl_prefix}%{pkg_name}
Version:        1.0
# See http://fedoraproject.org/wiki/Packaging:NamingGuidelines#Package_Versioning
Release:        0.5.alpha2.13%{?dist}
# Maven-shared defines maven-repository-builder version as 1.0
Epoch:          1
Summary:        Maven repository builder
License:        ASL 2.0
URL:            http://maven.apache.org/shared/maven-repository-builder/

# svn export http://svn.apache.org/repos/asf/maven/shared/tags/maven-repository-builder-1.0-alpha-2 maven-repository-builder-1.0-alpha-2
# tar caf maven-repository-builder-1.0-alpha-2.tar.xz maven-repository-builder-1.0-alpha-2/
Source0:        %{pkg_name}-%{pkg_version}.tar.xz
# ASL mandates that the licence file be included in redistributed source
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch:      noarch

BuildRequires:  %{?scl_prefix_java_common}easymock
BuildRequires:  %{?scl_prefix_java_common}junit
BuildRequires:  %{?scl_prefix_java_common}maven-local
BuildRequires:  %{?scl_prefix}maven-surefire-provider-junit
BuildRequires:  %{?scl_prefix}maven-test-tools
BuildRequires:  %{?scl_prefix}maven-wagon-file
BuildRequires:  %{?scl_prefix}maven-wagon-http-lightweight
BuildRequires:  %{?scl_prefix}maven-shared


%description
Maven repository builder.

This is a replacement package for maven-shared-repository-builder

%package javadoc
Summary:        Javadoc for %{pkg_name}
    
%description javadoc
API documentation for %{pkg_name}.


%prep
%setup -q -n %{pkg_name}-%{pkg_version}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# Replace plexus-maven-plugin with plexus-component-metadata
find -name 'pom.xml' -exec sed \
    -i 's/<artifactId>plexus-maven-plugin<\/artifactId>/<artifactId>plexus-component-metadata<\/artifactId>/' '{}' ';'
find -name 'pom.xml' -exec sed \
    -i 's/<goal>descriptor<\/goal>/<goal>generate-metadata<\/goal>/' '{}' ';'

# Removing JARs because of binary code contained
find -iname '*.jar' -delete

cp %{SOURCE1} LICENSE.txt
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# Skipping tests because they don't work without the JARs
%mvn_build -f
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
%mvn_install
%{?scl:EOF}

%files -f .mfiles
%{_javadir}/%{pkg_name}
%dir %{_mavenpomdir}/%{pkg_name}
%doc LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt


%changelog
* Mon Jan 11 2016 Michal Srb <msrb@redhat.com> - 1:1.0-0.5.alpha2.13
- maven33 rebuild #2

* Sat Jan 09 2016 Michal Srb <msrb@redhat.com> - 1:1.0-0.5.alpha2.12
- maven33 rebuild

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.11
- Add directory ownership on %%{_mavenpomdir} subdir

* Thu Jan 15 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.10
- Rebuild to fix provides

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 1:1.0-0.5.alpha2.9
- Mass rebuild 2015-01-13

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 1:1.0-0.5.alpha2.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.7
- Mass rebuild 2014-05-26

* Thu Feb 20 2014 Michael Simacek <msimacek@redhat.com> - 1:1.0-0.5.alpha2.6
- Adjust maven-wagon R/BR

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.5
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.4
- Mass rebuild 2014-02-18

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 1:1.0-0.5.alpha2.3
- SCL-ize BR

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.5.alpha2.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:1.0-0.5.alpha2
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1:1.0-0.4.alpha2
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Tue Feb 19 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.3.alpha2
- Added BR on maven-shared

* Fri Feb 08 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.2.alpha2
- Removed bundled JAR
- Building the new way

* Fri Jan 11 2013 Tomas Radej <tradej@redhat.com> - 1:1.0-0.1.alpha2
- Initial version

