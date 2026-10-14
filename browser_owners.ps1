$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$items = @(Get-CimInstance Win32_Process -Filter "Name = 'chrome.exe'" | Where-Object { $_.CommandLine -and $_.CommandLine -notmatch '--type=' } | ForEach-Object {
    $portMatch = [regex]::Match($_.CommandLine, '--remote-debugging-port(?:=|\s+)(\d+)')
    $profileMatch = [regex]::Match($_.CommandLine, '--user-data-dir(?:=|\s+)(?:"([^"]+)"|([^\s]+))')
    $profile = if ($profileMatch.Success) { if ($profileMatch.Groups[1].Success) { $profileMatch.Groups[1].Value } else { $profileMatch.Groups[2].Value } } else { '' }
    [pscustomobject]@{ Pid = $_.ProcessId; Executable = $_.ExecutablePath; DebugPort = if ($portMatch.Success) { [int]$portMatch.Groups[1].Value } else { 0 }; UserDataDir = $profile }
})
ConvertTo-Json -InputObject $items -Depth 3 -Compress
