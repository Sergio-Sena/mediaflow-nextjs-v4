$dir = 'C:\Users\dell 5557\Videos\IDM\Sienna_Sky'
$files = Get-ChildItem -LiteralPath $dir -File
$ok = 0

foreach ($f in $files) {
    $name = $f.BaseName
    $ext = $f.Extension

    # Remove Pornhub
    $name = $name -replace '[\s_]*-?[\s_]*(Pornhub[\s_]*com|Pornhub\.com|Pornhub)', ''
    $name = $name -replace '[\s_]*-?[\s_]*Deluxe_Bitch', ''

    # Replace special chars
    $name = $name -replace '[^a-zA-Z0-9]', '_'
    $name = $name -replace '_+', '_'
    $name = $name.Trim('_')

    # Truncate to 60 chars
    if ($name.Length -gt 60) {
        $last = $name.Substring(0, 60).LastIndexOf('_')
        if ($last -gt 50) { $name = $name.Substring(0, $last) }
        else { $name = $name.Substring(0, 60) }
    }

    $newName = $name + $ext
    if ($newName -ne $f.Name) {
        $dest = Join-Path $dir $newName
        if (Test-Path $dest) { $name = $name + '_2'; $dest = Join-Path $dir ($name + $ext) }
        Move-Item -LiteralPath $f.FullName -Destination $dest -Force
        $ok++
    }
}
Write-Host "Renomeados: $ok"
