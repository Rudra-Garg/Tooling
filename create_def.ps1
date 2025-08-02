# Robust PowerShell script to create .def file from DLL
param(
    [Parameter(Mandatory=$true)]
    [string]$DllPath,
    [Parameter(Mandatory=$true)]
    [string]$DefPath,
    [string]$FilterPrefix = "",
    [switch]$ShowDebug = $false
)

# Check if DLL exists
if (-not (Test-Path $DllPath)) {
    Write-Error "DLL file not found: $DllPath"
    exit 1
}

$dllName = [System.IO.Path]::GetFileNameWithoutExtension($DllPath)
Write-Host "Processing $DllPath..."

# Run dumpbin and capture output
try {
    $dumpbinOutput = & dumpbin /exports $DllPath 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "dumpbin failed. Make sure Visual Studio tools are in PATH."
        exit 1
    }
} catch {
    Write-Error "Failed to run dumpbin: $_"
    exit 1
}

if ($ShowDebug) {
    Write-Host "`nDEBUG: Full dumpbin output:"
    $dumpbinOutput | ForEach-Object { Write-Host $_ }
    Write-Host "`nDEBUG: End of dumpbin output"
}

# Extract exports using multiple strategies
$exports = @()

# Strategy 1: Look for the standard exports table
$inExportsSection = $false
$foundExportsHeader = $false

foreach ($line in $dumpbinOutput) {
    # Look for exports section indicators
    if ($line -match "Section contains the following exports" -or 
        $line -match "ordinal\s+hint.*name" -or
        $line -match "^\s*\d+\s+[A-F0-9]+\s+[A-F0-9]+\s+\w+") {
        $inExportsSection = $true
        $foundExportsHeader = $true
        if ($ShowDebug) { Write-Host "DEBUG: Found exports section: $line" }
        continue
    }
    
    # End of exports section
    if ($inExportsSection -and ($line -match "^\s*Summary" -or $line -match "^\s*$")) {
        if ($ShowDebug) { Write-Host "DEBUG: End of exports section: $line" }
        break
    }
    
    # Extract function names - try multiple patterns
    if ($inExportsSection) {
        $functionName = $null
        
        # Pattern 1: "    123   7C 00012345 function_name"
        if ($line -match "^\s*\d+\s+[A-F0-9]*\s+[A-F0-9]+\s+([A-Za-z_]\w*)") {
            $functionName = $matches[1]
        }
        # Pattern 2: "    123        function_name"
        elseif ($line -match "^\s*\d+\s+([A-Za-z_]\w*)") {
            $functionName = $matches[1]
        }
        # Pattern 3: Look for any valid identifier at the end of the line
        elseif ($line -match "([A-Za-z_]\w*)\s*$") {
            $candidate = $matches[1]
            # Make sure it's not a hex number or keyword
            if ($candidate -notmatch "^[A-F0-9]+$" -and 
                $candidate -notin @("name", "hint", "RVA", "ordinal")) {
                $functionName = $candidate
            }
        }
        
        if ($functionName) {
            $exports += $functionName
            if ($ShowDebug) { Write-Host "DEBUG: Found export: $functionName" }
        }
    }
}

# Strategy 2: If no exports found with standard method, try a more aggressive approach
if ($exports.Count -eq 0) {
    Write-Host "No exports found with standard method, trying alternative approach..."
    
    # Look for any line that might contain function names
    foreach ($line in $dumpbinOutput) {
        # Skip headers and metadata
        if ($line -match "Microsoft|Copyright|Dump of file|File Type|Optional header|Section contains|characteristics|time date stamp|version|age|Summary") {
            continue
        }
        
        # Look for lines with potential function names
        if ($line -match "([A-Za-z_]\w*)" -and $line -notmatch "^\s*$") {
            $matches = [regex]::Matches($line, "([A-Za-z_]\w*)")
            foreach ($match in $matches) {
                $candidate = $match.Groups[1].Value
                if ($candidate.Length -gt 2 -and 
                    $candidate -notmatch "^[A-F0-9]+$" -and
                    $candidate -notin @("name", "hint", "RVA", "ordinal", "exports", "for", "dll", "Section", "contains", "the", "following")) {
                    $exports += $candidate
                    if ($ShowDebug) { Write-Host "DEBUG: Alternative method found: $candidate" }
                }
            }
        }
    }
}

# Remove duplicates and sort
$exports = $exports | Sort-Object -Unique

Write-Host "Found $($exports.Count) total exports"

# Apply prefix filter if specified
if ($FilterPrefix) {
    $filteredExports = $exports | Where-Object { $_ -like "$FilterPrefix*" }
    Write-Host "After prefix filter '$FilterPrefix': $($filteredExports.Count) exports"
} else {
    $filteredExports = $exports
}

# Create .def file
if ($filteredExports.Count -eq 0) {
    Write-Warning "No exports found! The .def file will be empty."
    Write-Host "This might mean:"
    Write-Host "1. The DLL has no exports (statically linked)"
    Write-Host "2. The exports are in an unexpected format"
    Write-Host "3. Try running with -ShowDebug flag to see raw output"
}

$defContent = "LIBRARY $dllName`nEXPORTS`n"

foreach ($export in $filteredExports) {
    $defContent += "$export`n"
}

# Write to file
try {
    $defContent | Out-File -FilePath $DefPath -Encoding ASCII
    Write-Host "Created $DefPath with $($filteredExports.Count) exports"
} catch {
    Write-Error "Failed to write DEF file: $_"
    exit 1
}

# Show preview
if ($filteredExports.Count -gt 0) {
    Write-Host "`nFirst 10 exports:"
    $filteredExports | Select-Object -First 10 | ForEach-Object { Write-Host "  $_" }
    
    if ($filteredExports.Count -gt 10) {
        Write-Host "  ... and $($filteredExports.Count - 10) more"
    }
    
    Write-Host "`nTo create the import library, run:"
    Write-Host "lib /def:$DefPath /out:$($dllName).lib /machine:x64"
} else {
    Write-Host "`nTry running with -ShowDebug flag to see what's in the DLL:"
    Write-Host "PowerShell -ExecutionPolicy Bypass -File script.ps1 -DllPath `"$DllPath`" -DefPath `"$DefPath`" -ShowDebug"
}