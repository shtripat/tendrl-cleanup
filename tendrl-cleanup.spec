# This rpm spec file is based on packaging approach used by linux-system-roles
# project, as there are no Fedora packaging guidelines for ansible or better
# examples to follow. Target OS is RHEL or CentOS 7.

Name:           tendrl-cleanup
Version:        1.0.0
Release:        1%{?dist}
Summary:        Ansible roles and playbooks for Tendrl setup cleanup

License:        LGPLv2.1
Url:            https://github.com/shtripat/tendrl-cleanup
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

Requires:       ansible >= 2.3
Requires:       python-dns
BuildRequires:  yamllint

# All ansible roles from tendrl-cleanup will have this prefix added into the
# name of the role (name of the directory with the role) to prevent conflicts.
%global roleprefix %{name}.

%description
Ansible roles and playbooks for cleanup of an existing Tendrl setup


%prep
%setup -q

%build
# reference roles by prefixed name in sample playbook file
sed -i 's/- \(tendrl-server\)/- %{roleprefix}\1/g' site.yml.sample
sed -i 's/- \(tendrl-storage-node\)/- %{roleprefix}\1/g' site.yml.sample

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/ansible/roles

# install ansible roles
cp -pR roles/tendrl-server          $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}tendrl-server
cp -pR roles/tendrl-storage-node    $RPM_BUILD_ROOT%{_datadir}/ansible/roles/%{roleprefix}tendrl-storage-node

mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}/

# install playbooks
install -p -m 644 site.yml.sample                    $RPM_BUILD_ROOT%{_pkgdocdir}/site.yml.sample

# install readme and license files
install -p -m 644 README.rpm.md                $RPM_BUILD_ROOT%{_pkgdocdir}/README.md
install -p -m 644 LICENSE                      $RPM_BUILD_ROOT%{_pkgdocdir}/LICENSE

%check
yamlint $RPM_BUILD_ROOT && rm .yamlint

%files
%{_datadir}/ansible/roles/%{roleprefix}tendrl-server
%{_datadir}/ansible/roles/%{roleprefix}tendrl-storage-node

# mark readme files in ansible roles as documentation
%doc %{_datadir}/ansible/roles/%{roleprefix}tendrl-server/README.md
%doc %{_datadir}/ansible/roles/%{roleprefix}tendrl-storage-node/README.md

# mark example site.yml file as documentation
%doc %{_pkgdocdir}/site.yml.sample

# readme and license files
%doc %{_pkgdocdir}/README.md
%license %{_pkgdocdir}/LICENSE

%changelog
* Wed Feb 14 2018  Shubhendu Ram Tripathi <shtripat@redhat.com> - 1.0.0-1
- First release with tendrl-cleanup provided in rpm package.
- Initial specfile based on rhel-system-roles packaging style.
