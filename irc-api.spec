%{?_javapackages_macros:%_javapackages_macros}
%global invalid_version %(echo %version | tr _ \-)

%define commit a542ef7d241e5a398ba8cb840030f352a8066b1b
%define shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	A Java IRC API
Name:		irc-api
Version:	1.0.0015
Release:	0
License:	ASL 2.0
Group:		Development/Java
URL:		https://github.com/migzai/%{name}
Source0:	https://github.com/migzai/%{name}/archive/%{commit}/%{name}-%{commit}.zip
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(commons-codec:commons-codec)
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-eclipse-plugin)
#BuildRequires:	mvn(com.googlecode.jmockit:jmockit)
BuildRequires:	mvn(org.slf4j:slf4j-api)
BuildRequires:	mvn(org.sonatype.oss:oss-parent:pom:)

%description
IRC-API is a state(ful)/(less), (a)synchronous IRC API written in Java.
The API offers an (a)synchronous programming model, and has the ability to
save the IRC connection state per user. SSL support has lately been added,
and more features are to come soon.

Main features are:

 - State(ful/less) API
 - Callbacks support / Asynchronous
 - Message Listeners - Message Filters
 - SSL support
 - DCC support
 - IPV6 support
 - SLF4J/Maven integration
 - Java NIO


The API has been tested on various IRC networks, i.e. EFnet, DALnet,
Undernet, and offers a useful and detailed interface to the Server it
connects to.

%files -f .mfiles
%doc README.md

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc
%doc README.md

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{commit}
# Delete all pre-build binaries
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Fix version
%pom_xpath_replace "pom:project/pom:version" "<version>%{version}</version>"

# Remove unpackaged dependencies
%pom_remove_dep com.googlecode.jmockit:jmockit

# Add the META-INF/INDEX.LIST to the jar archive (fix jar-not-indexed warning)
%pom_xpath_inject "pom:plugin[pom:artifactId[./text()='maven-jar-plugin']]/pom:configuration/pom:archive" "<index>true</index>"

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "<extensions>true</extensions>"

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build -f

%install
%mvn_install

