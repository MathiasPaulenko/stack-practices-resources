# Pull compliance and encryption state for every Intune-enrolled device.
# Requires: Install-Module Microsoft.Graph.DeviceManagement

Connect-MgGraph -Scopes "DeviceManagementManagedDevices.Read.All"

Get-MgDeviceManagementManagedDevice -All |
  Select-Object DeviceName, OperatingSystem, OsVersion,
                ComplianceState, EncryptionState |
  Format-Table -AutoSize

Get-MgDeviceManagementManagedDevice -All -Filter "complianceState ne 'compliant'" |
  Select-Object DeviceName, UserPrincipalName, ComplianceState
