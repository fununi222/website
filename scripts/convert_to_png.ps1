param()

Add-Type -AssemblyName System.Drawing

$imgDir = "c:\Users\fumiy\.openclaw\workspace\website\assets\img"
$jpgFiles = Get-ChildItem -Path $imgDir -Filter *.jpg

foreach ($file in $jpgFiles) {
    try {
        $img = [System.Drawing.Image]::FromFile($file.FullName)
        $pngName = [System.IO.Path]::ChangeExtension($file.FullName, ".png")
        $img.Save($pngName, [System.Drawing.Imaging.ImageFormat]::Png)
        $img.Dispose()
        Remove-Item -Path $file.FullName -Force
        Write-Host "Converted: $($file.Name)"
    } catch {
        Write-Host "Error converting $($file.Name): $_"
    }
}

$workspaceDir = "c:\Users\fumiy\.openclaw\workspace\website"
$textFiles = Get-ChildItem -Path $workspaceDir -Include *.md,*.html,*.js -Recurse | Where-Object { -not $_.DirectoryName.Contains(".git") }

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

foreach ($file in $textFiles) {
    $content = Get-Content -Path $file.FullName -Raw
    if ($content -match "\.jpg") {
        $newContent = $content -replace "\.jpg", ".png"
        [System.IO.File]::WriteAllText($file.FullName, $newContent, $utf8NoBom)
        Write-Host "Updated references in $($file.Name)"
    }
}
Write-Host "Done!"
