<#
.SYNOPSIS
    Automatically updates index.html with all Grammar Explorer lessons/units and pushes to GitHub.
.DESCRIPTION
    Scans for all standard and full book lesson files, updates index.html cards, counts, and catalog,
    and commits/pushes to GitHub.
.PARAMETER Push
    Whether to push to GitHub (default is $true).
.PARAMETER Message
    Custom commit message.
.EXAMPLE
    .\update-and-push.ps1
    .\update-and-push.ps1 -Message "feat: add unit 10 book edition"
    .\update-and-push.ps1 -NoPush
#>

param(
    [switch]$NoPush,
    [string]$Message = ""
)

Set-Location $PSScriptRoot

$cmdArgs = @("update-index.js")
if (-not $NoPush) {
    $cmdArgs += "--push"
}
if ($Message -ne "") {
    $cmdArgs += @("-m", $Message)
}

Write-Host "Running Grammar Explorer index update..." -ForegroundColor Cyan
node @cmdArgs
